$(() => {
    var hand, timer, clicks = 0;
    const room = window.location.pathname.slice(1), socketio = io({ transport: ["websocket"] });

    socketio.on("connect", function () { socketio.emit("join", { room }); });
    socketio.on("join", function (data) { socketio.emit("play", { user: data.user, html: $("#table").html() }); });
    socketio.on("play", function (data) { $("#table").html(data.html); });
    socketio.on("turn", function (data) {
        $(`#${data.id}`).attr(
            "src",
            $(`#${data.id}`).attr("src").startsWith("static/assets/decks/")
                ? `static/assets/backs/${$(`#${data.id}`)[0].classList[0]}.jpg`
                : `static/assets/decks/${$(`#${data.id}`)[0].classList[0]}/${data.value}`
        );
    });
    socketio.on("hand", function (data) {
        $("#table").html(data.html + `<img id = "hand-icon" src = "static/assets/other/hand.png" height = "50px" style = "position: absolute; left: ${data.hand.x}; top: ${data.hand.y}; z-index: ${data.hand.z}" alt = "hand-icon">`);
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
            hand = { x: that.css("left"), y: that.css("top"), z: that.css("z-index") };
            $("#hand div").prepend(that);
            socketio.emit("hand", { room, html: $("#table").html(), hand: hand });
            clicks = 0;
        }
    });

    $("#hand").on("click", ".card", function () { socketio.emit("turn", { id: $(this).attr("id") }); });

    $("#table *").draggable({
        delay: 150,
        cursor: "grabbing",
        stack: "#table *",
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