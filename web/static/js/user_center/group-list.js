/**
 * Created by abbott on 1/26/2018.
 */
function delete_group_data_fn(group_id) {
    $("#delete_data_html_area").html("Confirm remove Group? All the data will be delete!");
    $("#delete_group_app_fn").attr("onclick", "delete_group_app_fn('delete', " + group_id + ")");
    $("#delete_app_modal").modal('show')
}

function update_group_app_fn(update_type, group_id) {

    var group_name = $('input[name="group_name"]').val();

    if (group_name.length == 0 ) {
                alert("Please fill group name.");
                return false;
    }
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
        url: '/user_center/groups.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'group_id': group_id, 'group_name': group_name},
        success: function (data, response, status) {
            window.location.href = "/user_center/group-list.html"
        }
    });
}

function delete_group_app_fn(update_type, group_id) {

    $.ajax({
        url: '/user_center/groups.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'group_id': group_id},
        success: function (data, response, status) {
            $("#delete_app_modal").modal('hide');
            $('#do_refresh').trigger("click");
        }
    });
}