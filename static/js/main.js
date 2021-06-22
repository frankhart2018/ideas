$(document).ready(function() {

    function validate_email(mail) {
        if (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(mail))
            return true;

        return (false);
    }

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

    $("#register").click(function() {
        let name = $("#name").val();
        let email = $("#email").val();
        let password = $("#password").val();
        let cpassword = $("#cpassword").val();

        if(name && email && password && cpassword) {
            let error_string = "";

            if(!validate_email(email)) {
                error_string += "Invalid email address\n";
            }

            if(password != cpassword) {
                error_string += "Passwords do not match\n";
            }

            if(error_string) {
                Swal.fire({
                    "icon": "error",
                    "title": "Error",
                    "text": error_string,
                });
            } else {
                ajax_request("/register", {"name": name, "email": email, "password": password});
            }
        } else {
            Swal.fire({
                "icon": "error",
                "title": "Error",
                "text": "All fields are required!",
            });
        }
    });

    $("#login").click(function() {
        let email = $("#log_email").val();
        let password = $("#log_password").val();

        if(email && password) {
            ajax_request("/login", {"email": email, "password": password});
        } else {
            Swal.fire({
                "icon": "error",
                "title": "Error",
                "text": "All fields are required!",
            });
        }
    });

});