$(document).ready(function() {
    $("#users-table").DataTable();
    $("#ideas-table").DataTable();

    function ajax_request(url, data) {
        $.ajax({
            url: url,
            type: "post",
            data: data,
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

    $(".accept-button").click(function() {
        var uid = $(this).attr("id").split("-")[1];
        ajax_request("/update-user-status", {"uid": uid, "status": 1});
    });

    $(".reject-button").click(function() {
        Swal.fire({
            "icon": "warning",
            "title": "Are you sure?",
            "text": "Sure you want to reject this wonderful person?",
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, reject!'
        }).then((result) => {
            if(result.isConfirmed) {
                var uid = $(this).attr("id").split("-")[1];
            ajax_request("/update-user-status", {"uid": uid, "status": -1});
            }
        });
    });

    $(".delete").click(function() {
        Swal.fire({
            "icon": "warning",
            "title": "Are you sure?",
            "text": "Sure you want to delete this wonderful idea?",
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if(result.isConfirmed) {
                var iid = $(this).attr("id");
                ajax_request("/delete-idea", {"iid": iid});
            }
        });
    });
});