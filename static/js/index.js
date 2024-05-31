$(() => {
    let room, socketio;
    fetch("https://api.ipify.org?format=json")
        .then(response => response.json())
        .then(data => { room = data.ip; })
        .then(() => {
            socketio = io({ transport: ["websocket"] });
            socketio.on("connect", function () {
                socketio.emit("join", { room });
                socketio.on("join", function (data) { socketio.emit("play", { room, user: data.user, html: $("#table").html() }); });
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
            });
        });
});

// import Draggable from "https://cdn.jsdelivr.net/npm/@shopify/draggable/build/esm/Draggable/Draggable.mjs";

// Draggable.create("#table *", {
//     bounds: "#table",
//     activeCursor: "grabbing",
//     onDragStart: function () {
//         if ($(this.target).hasClass("clone")) {
//             $(this.target).clone().appendTo("#table");
//         }
//     },
//     onDrag: function () {
//         socketio.emit("play", { room, html: $("#table").html() });
//     },
//     onClick: function () {
//         if ($(this.target).hasClass("card")) {
//             click++
//             if (click === 1) {
//                 timer = setTimeout(() => {
//                     click = 0;
//                     socketio.emit("turn", { room, id: $(this.target).attr("id") });
//                 }, 300);
//             } else if (click === 2) {
//                 click = 0;
//                 $(this.target).appendTo("#hand");
//                 socketio.emit("hand", { room, html: $("#table").html(), position: { x: $(this.target).css("left"), y: $(this.target).css("top"), z: $(this.target).css("z-index") } });
//             }
//         }
//     }
// });

// Draggable.create("#hand .card", {
//     bounds: "#table",
//     activeCursor: "grabbing",
//     onDrag: function () {
//         socketio.emit("play", { room, html: $("#table").html() });
//     },
//     onClick: function () {
//         socketio.emit("turn", { room, id: $(this.target).attr("id") });
//     }
// });


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