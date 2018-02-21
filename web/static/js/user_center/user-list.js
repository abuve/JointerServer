/**
 * Created by abbott on 1/26/2018.
 */
function delete_user_data_fn(user_id) {
    $("#delete_data_html_area").html("Confirm remove User? All the data will be delete!");
    $("#delete_user_app_fn").attr("onclick", "delete_user_app_fn('delete', " + user_id + ")");
    $("#delete_app_modal").modal('show')
}

function update_user_app_fn(update_type, user_id) {

    var user_name = $('input[name="user_name"]').val();
    var user_phone = $('input[name="user_phone"]').val();
    var user_email = $('input[name="user_email"]').val();
    var user_department = $('input[name="user_department"]').val();
    var user_group = $('select[name="user_group"]').val();

    // if (user_name.length == 0 ) {
    //             alert("Please fill user name.");
    //             return false;
    // }
    // if (user_phone.length == 0 ) {
    //             alert("Please fill user phone.");
    //             return false;
    // }
    // if (user_email.length == 0 ) {
    //             alert("Please fill user email.");
    //             return false;
    // }
    // if (user_department.length == 0 ) {
    //             alert("Please fill user department.");
    //             return false;
    // }

    $.ajax({
        url: '/user_center/users.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'user_id': user_id, 'user_name': user_name, 'user_phone': user_phone, 'user_email': user_email, 'user_department': user_department, 'user_group': user_group},
        success: function (data, response, status) {
            window.location.href = "/user_center/user-list.html"
        }
    });
}

function delete_user_app_fn(update_type, user_id) {

    $.ajax({
        url: '/user_center/users.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'user_id': user_id},
        success: function (data, response, status) {
            $("#delete_app_modal").modal('hide');
            $('#do_refresh').trigger("click");
        }
    });
}