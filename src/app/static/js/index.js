$(() => {
    let exit = {};
    fetch("https://api.ipify.org?format=json")
        .then(response => response.json())
        .then(data => { room = data.ip; })
        .then(() => {
            socketio = io();
            socketio.on("connect", function () {
                socketio.emit("join", { room });
                socketio.on("join", function (data) { socketio.emit("play", { user: data.user, html: $("#table").html() }); });
                socketio.on("play", function (data) { $("#table").html(data.html); });
                socketio.on("show", function (data) { exit[data.card] = data.exit; $(`#table img:nth-child(${data.card + 1})`).attr("src", `../static/assets/decks/${data.deck}/${data.exit}`); });
                socketio.on("hide", function (data) { $(`#table img:nth-child(${data.card + 1})`).attr("src", `../static/assets/decks/backs/${data.deck}.png`); });
                socketio.on("hand", function (data) { $("#table").html(data.html + `<img id = "hand-icon" src = "static/assets/other/hand.png" height = "50px" style = "position: absolute; left: ${data.x}; top: ${data.y}; z-index: ${data.z}" alt = "hand-icon">`); $("#hand-icon").fadeOut(1500, function () { $(this).remove(); }); });
                socketio.on("drag", function (data) { });
            });

            $("#table *").draggable({
                distance: 15,
                stack: "#table *",
                cursor: "grabbing",
                containment: [20, 20],
                drag: function (event, ui) {
                    socketio.emit("drag", { room, })
                }
            });

            interact("#table .card")
                .on("tap", (event) => {
                    item = event.target
                    card = $(item).index();
                    deck = item.classList[0];
                    $(item).attr("src").startsWith("../static/assets/decks/backs/")
                        ? socketio.emit("show", { room, card: card, deck: deck.replace(/\d+/g, ""), exit: exit[card] ?? Object.values(exit) })
                        : socketio.emit("hide", { room, card: card, deck: deck })
                })
                .on("hold", (event) => {
                    x = $(event.target).css("left");
                    y = $(event.target).css("top");
                    z = $(event.target).css("z-index");
                    $("#hand div").prepend($(event.target).removeAttr("style"));
                    socketio.emit("hand", { room, html: $("#table").html(), x: x, y: y, z: z });
                });

            // interact("#hand .card")
            //     .on("tap", (event) => {
            //         turn(event.target);
            //     })
            //     .on("hold", (event) => {
            //         $("#table").prepend($(event.target).removeAttr("style").css({
            //             "transform": `translate3d(${(($("body").width() / 2) - 34.325 + parseFloat($(event.target).css("left")))}px, ${$("#table").height() - $(event.target).height()}px, 0)`
            //         }));
            //     });
        });
});