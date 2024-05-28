$(() => {
    var timer, clicks = 0, position;
    const room = window.location.pathname.slice(1), socketio = io({ transport: ["websocket"] });

    socketio.on("connect", function () { socketio.emit("join", { room }); });
    socketio.on("join", function (data) { socketio.emit("play", { user: data.user, html: $("#table").html() }); });
    socketio.on("play", function (data) { $("#table").html(data.html); });
    socketio.on("turn", function (data) {
        $(`#${data.id}`).attr(
            "src",
            $(`#${data.id}`).attr("src").startsWith("static/assets/decks/")
                ? `static/assets/backs/${$(`#${data.id}`)[0].classList[0]}.png`
                : `static/assets/decks/${$(`#${data.id}`)[0].classList[0]}/${data.value}`
        );
    });
    socketio.on("hand", function (data) {
        $("#table").html(data.html + `<img id = "hand-icon" src = "static/assets/other/hand.png" height = "50px" style = "position: absolute; left: ${data.position.x}; top: ${data.position.y}; z-index: ${data.position.z}" alt = "hand-icon">`);
        $("#hand-icon").fadeOut(1500, function () {
            $(this).remove();
        });
    })

    $("#table").on("click", ".card", function () {
        clicks++;
        that = $(this);

        if (clicks === 1) {
            timer = setTimeout(function () {
                socketio.emit("turn", { room, id: that.attr("id") });
                clicks = 0;
            }, 300);
        } else if (clicks === 2) {
            clearTimeout(timer);
            position = { x: that.css("left"), y: that.css("top"), z: that.css("z-index") };
            $("#hand").prepend(
                $(this).draggable({
                    delay: 300,
                    stack: "#table *",
                    cursor: "grabbing",
                    containment: "#table",
                    stop: function () {
                        $(this).appendTo("#table");
                        socketio.emit("play", { room, html: $("#table").html() });
                    }
                })
            );
            socketio.emit("hand", { room, html: $("#table").html(), position: position });
            clicks = 0;
        }
    });

    $("#hand").on("click", ".card", function () { socketio.emit("turn", { id: $(this).attr("id") }); });

    $("#table *:not(#share)").draggable({
        delay: 300,
        stack: "#table *",
        cursor: "grabbing",
        containment: "#table",
        start: function () {
            if ($(this).hasClass("clonable")) {
                $(this).removeClass("clonable");
                $(this).clone().appendTo("#table");
            }
        },
        drag: function () { socketio.emit("play", { room, html: $("#table").html() }); }
    });
});