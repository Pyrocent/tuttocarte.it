$(document).ready(function () {

    const slider = $("#slider")

    var items = slider.children().toArray();
    for (var i = items.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = items[i];
        items[i] = items[j];
        items[j] = temp;
    }
    slider.empty().append(items);

    slider.slick({
        arrows: false,
        autoplay: true,
        touchMove: false,
        slidesToScroll: 1,
        focusOnSelect: true,
        pauseOnHover: false,
        pauseOnFocus: false,
        autoplaySpeed: 1000,
        responsive: [
            {
                breakpoint: 2560,
                settings: {
                    slidesToShow: 20,
                }
            },
            {
                breakpoint: 1440,
                settings: {
                    slidesToShow: 16,
                }
            },
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 14,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 12,
                }
            },
            {
                breakpoint: 425,
                settings: {
                    slidesToShow: 10,
                }
            },
            {
                breakpoint: 375,
                settings: {
                    slidesToShow: 12,
                }
            },
            {
                breakpoint: 320,
                settings: {
                    slidesToShow: 10,
                }
            }
        ]
    });

    $(document).on("keypress", function (e) {
        if (e.which == 13) {
            $("#submit").click();
        }
    });

    $("form").on("submit", function () {
        $("#submit").prop("disabled", true);
    });

});