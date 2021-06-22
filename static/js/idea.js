$(document).ready(function() {

    $("#comments-table").DataTable();

    function ajax_request(comment) {
        let path_name_arr = window.location.pathname.split("/");
        let iid = path_name_arr[path_name_arr.length - 1];

        $.ajax({
            url: "/add-comment",
            type: "post",
            data: {"iid": iid, "comment": comment},
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

    $("#add-comment").click(function() {
        let comment = $("#comment").val();

        if(comment) {
            ajax_request(comment);
        } else {
            Swal.fire({
                "icon": "error",
                "title": "Error",
                "text": "All fields are required!",
            });
        }
    });

});