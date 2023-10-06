$(document).ready(function () {

    $(document).on("keypress", function (e) {
        if (e.which == 13) {
            $("#submit").click();
        }
    });

    $("form").on("submit", function () {
        $("#submit").prop("disabled", true);
    });

});