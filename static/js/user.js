$(document).ready(function() {

    $("#ideas-table").DataTable();

    function ajax_request(idea) {
        $.ajax({
            url: "/add-idea",
            type: "post",
            data: {"idea": idea},
            success: function(result) {
                Swal.fire({
                    "icon": result.icon,
                    "title": result.title,
                    "text": result.text,
                }).then(function() {
                    if(result.icon == "success")
                        window.location.href = result.url;
                });
            }
        });
    }

    $("#submit-idea").click(function() {
        let idea = $("#idea").val();

        if(idea) {
            ajax_request(idea);
        } else {
            Swal.fire({
                "icon": "error",
                "title": "Error",
                "text": "All fields are required!",
            });
        }
    });

});