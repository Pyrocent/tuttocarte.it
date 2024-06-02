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

            interact("#table .card")
                .on("tap", (event) => {
                    socketio.emit("turn", { room, id: $(event.target).attr("id") });
                })
                .on("hold", (event) => {
                    $("#hand").prepend(event.target);
                    socketio.emit("hand", { room, html: $("#table").html(), position: { x: $(event.target).css("left"), y: $(event.target).css("top"), z: $(event.target).css("z-index") } });
                });


            $("#table").on("touchstart mouseenter", "#table *", function () {
                $(this).draggable({
                    stack: "#table *",
                    cursor: "grabbing",
                    start: function () {
                        if ($(this).hasClass("clone")) {
                            $(this).clone().appendTo("#table");
                            $(this).removeClass("clone");
                        }
                    },
                    drag: function () {
                        socketio.emit("play", { room, html: $("#table").html() });
                    }
                });
            });

            $("#hand").on("touchstart mouseenter", ".card", function () {
                $(this).draggable({
                    stack: "#table *",
                    cursor: "grabbing",
                    containment: "#table",
                    stop: function () {
                        $(this).appendTo($("#table")).draggable("destroy").css({
                            "left": (parseFloat($(this).css("left"), 10) + ($("h5").width() + 9.800)) + "px",
                            "top": ($("#table").height() - (50 + (- parseFloat($(this).css("top"), 10) - 80.065))) + "px"
                        });
                        socketio.emit("play", { room, html: $("#table").html() });
                    }
                });
            });
        });
});

//     interact("#table .card")
//         .on("tap", (event) => {
//             socketio.emit("turn", { room, id: $(event.target).attr("id") });
//         })
//         .on("hold", (event) => {
//             $(event.target).appendTo("#hand");
//             socketio.emit("hand", { room, html: $("#table").html(), position: { x: $(event.target).css("left"), y: $(event.target).css("top"), z: $(event.target).css("z-index") } });
//         });

//     Draggable.create("#table *", {
//         bounds: "#table",
//         activeCursor: "grabbing",
//         onDragStart: function () {
//             if ($(this.target).hasClass("clone")) {
//                 $(this.target).clone().appendTo("#table");
//             }
//         },
//         onDrag: function () {
//             socketio.emit("play", { room, html: $("#table").html() });
//         }
//     });

//     Draggable.create("#hand .card", {
//         bounds: "#table",
//         activeCursor: "grabbing",
//         onDrag: function () {
//             socketio.emit("play", { room, html: $("#table").html() });
//         }
//     });

//     $("#hand").on("touchstart mouseenter", ".card", function () {
//         $(this).draggable({
//             containment: "#table",
//             start: function () {
//                 $(this).css({ "z-index": 2, "cursor": "grabbing" });
//             },
//             stop: function () {
//                 $(this).appendTo($("#table")).draggable("destroy").css({
//                     "z-index": 1,
//                     "cursor": "pointer",
//                     "left": (parseFloat($(this).css("left"), 10) + ($("h5").width() + 9.800)) + "px",
//                     "top": ($("#table").height() - (50 + (- parseFloat($(this).css("top"), 10) - 80.065))) + "px"
//                 });
//                 socketio.emit("play", { room, html: $("#table").html() });
//             }
//         });
//     });
// });



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