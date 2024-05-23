$(() => {
    var hand = {}, timer = null, clicks = 0;
    const room = window.location.pathname.slice(1), socketio = io({ transport: ["websocket"] });

    socketio.on("connect", function () {
        socketio.emit("join", { room });
    });

    socketio.on("join", function (data) {
        socketio.emit("play", { room, user: data.user, html: $("#table").html() });
    });

    socketio.on("play", function (data) {
        $("#table").html(data.html);
    });

    socketio.on("hand", function (data) {
        $("#table").html(data.html + `<img id = "hand-icon" src = "static/assets/other/hand.png" width = "50px" height = "50px" style = "position: absolute; top: ${data.hand.top}; left: ${data.hand.left};" alt="hand-icon">`);
        $("#hand-icon").fadeOut(1500);
    })

    socketio.on("turn", function (data) {
        $(`#${data.id}`).attr(
            "src",
            $(`#${data.id}`).attr("src").startsWith("static/assets/decks/")
                ? `static/assets/backs/${$(`#${data.id}`)[0].classList[0]}.jpg`
                : `static/assets/decks/${$(`#${data.id}`)[0].classList[0]}/${data.value}`
        );
    });

    $("#table, #hand").on("click", ".card", function () {
        clicks++;
        that = $(this);

        if (clicks === 1) {
            timer = setTimeout(function () {
                socketio.emit("turn", { room, id: that.attr("id") });
                clicks = 0;
            }, 300);
        } else {
            clearTimeout(timer);
            hand = { top: that.css("top"), left: that.css("left") };
            $("#hand div").prepend(that.css({ "top": "", "left": "" }));
            socketio.emit("hand", { room, html: $("#table").html(), hand: hand });
            clicks = 0;
        }
    });

    $("#table").on("touchstart mouseenter", ".card, .fiche", function () {
        $(this).draggable({
            start: function () {
                $(this).css({ "cursor": "grabbing", "z-index": 2 });
                if ($(this).hasClass("clonable")) {
                    $(this).clone().appendTo("#table");
                    $(this).removeClass("clonable");
                }
            },
            drag: function () {
                socketio.emit("play", { room, user: null, html: $("#table").html() });
            },
            stop: function () {
                $("#table").append($(this));
                $(this).css({ "cursor": "pointer", "z-index": 1 });
            }
        });
    });

    $("#hand").on("touchstart mouseenter", ".card", function () {
        $(this).draggable({
            axis: "x",
            start: function () {
                $(this).css({ "cursor": "grabbing", "z-index": 2 });
            },
            stop: function () {
                $(this).css({ "cursor": "pointer", "z-index": 1 });
            }
        });
    });
});