$(() => {
    let room, socketio;
    fetch("https://api.ipify.org?format=json")
        .then(response => response.json())
        .then(data => { room = data.ip; })
        .then(() => {
            socketio = io();
            socketio.on("connect", function () {
                socketio.emit("join", { room });
                socketio.on("join", function (data) { socketio.emit("play", { room: false, user: data.user, html: $("#table").html() }); });
                socketio.on("play", function (data) { $("#table").html(data.html); });
                socketio.on("hand", function (data) {
                    $("#table").html(data.html + `<img id = "hand-icon" src = "static/assets/other/hand.png" height = "50px" style = "position: absolute; left: ${data.position.x}; top: ${data.position.y}; z-index: ${data.position.z}" alt = "hand-icon">`);
                    $("#hand-icon").fadeOut(1500, function () {
                        $(this).remove();
                    });
                });
            });

            function turn(target) {
                $(target).attr(
                    "src",
                    $(target).attr("src").startsWith("../static/assets/decks/backs/")
                        ? `../static/assets/decks/${target.classList[0]}/${target.id}`
                        : `../static/assets/decks/backs/${target.classList[0]}/${target.classList[1]}.png`
                );
            }

            interact("#table .card")
                .on("tap", (event) => {
                    turn(event.target);
                    socketio.emit("play", { room, user: false, html: $("#table").html() });
                })
                .on("hold", (event) => {
                    var x = $(event.target).css("left");
                    var y = $(event.target).css("top");
                    var z = $(event.target).css("z-index");
                    $("#hand").prepend($(event.target).removeAttr("style"));
                    socketio.emit("hand", { room, html: $("#table").html(), position: { x: x, y: y, z: z } });
                });

            interact("#hand .card")
                .on("tap", (event) => {
                    turn(event.target);
                })
                .on("hold", (event) => {
                    $("#table").prepend($(event.target).removeAttr("style").css({
                        "transform": `translate3d(${(($("body").width() / 2) - 34.325 + parseFloat($(event.target).css("left")))}px, ${$("#table").height() - $(event.target).height()}px, 0)`
                    }));
                });
        });
});