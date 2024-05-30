$(() => {
    const socketio = io({ transport: ["websocket"] });

    socketio.on("connect", function () { socketio.emit("join", {}); });
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
    });

    $("#table *:not(#share)").draggable({
        stack: "#table *",
        cursor: "grabbing",
        containment: [20, 20, $("#table").width(), $("#table").height()],
        start: function () {
            if ($(this).hasClass("clone")) {
                $(this).removeClass("clone");
                $(this).clone().appendTo("#table")
            }
        },
        drag: function () {
            socketio.emit("play", { html: $("#table").html() });
        }
    });

    $(".card").on("click tap", function () {
        socketio.emit("turn", { id: $(this).attr("id") });
    });
});

// $("#table").on("dblclick", ".card", function () {
//     $("#hand").prepend($(this).draggable());
//     socketio.emit("hand", { room, html: $("#table").html(), position: { x: $(this).css("left"), y: $(this).css("top"), z: $(this).css("z-index") } });
// });

// $("#table").on("mousedown touchstart", ".card", function () {
//     var card = $(this);
//     timeout = setTimeout(function () {
//         var position = { x: card.css("left"), y: card.css("top"), z: card.css("z-index") };
//         $("#hand").prepend(
//             card.draggable({
//                 stack: "#table *",
//                 cursor: "grabbing",
//                 containment: "#table",
//                 stop: function () {
//                     $(this).appendTo("#table");
//                     socketio.emit("play", { room, html: $("#table").html() });
//                 }
//             })
//         );
//         socketio.emit("hand", { room, html: $("#table").html(), position: position });
//     }, 301);
// }).on("mouseup mouseleave", function () {
//     clearTimeout(timeout);
// });