/**
 * Created by aaron on 2017/9/11.
 */

// function update_server_group_fn(update_type, group_id) {
//
//     var add_group_name = $('input[name="add_group_name"]').val()
//     var add_group_app_id = $('input[name="add_group_app_id"]').val()
//     var add_group_app_path = $('input[name="add_group_app_path"]').val()
//
//     $.ajax({
//         url: '/update-server-group.html',
//         type: update_type,
//         dataType: 'json',
//         traditional:true,
//         data: {'add_group_name': add_group_name, 'add_group_app_id': add_group_app_id, 'add_group_app_path': add_group_app_path, 'group_id': group_id},
//         success: function (data, response, status) {
//             $('#group_table').bootstrapTable('refresh');
//             $("#add_group_modal").modal('hide')
//             $("#delete_group_modal").modal('hide')
//             $("#add_server_group_form").trigger("reset");
//         }
//     });
// }

function delete_server_data_fn(server_id) {
    $("#delete_data_html_area").html("Confirm remove Application? All the data will be delete!")
    $("#delete_server_app_fn").attr("onclick", "delete_server_app_fn('delete', " + server_id + ")")
    $("#delete_app_modal").modal('show')
}

function update_server_app_fn(update_type, server_id) {

    var app_name = $('input[name="app_name"]').val()
    var project_id = $('select[name="project_id"]').val()
    var app_type = $('select[name="app_type"]').val()

    $.ajax({
        url: '/servers.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'server_id': server_id, 'app_name': app_name, 'project_id': project_id, 'app_type': app_type},
        success: function (data, response, status) {
            window.location.href = "/server.html"
        }
    });
}

function delete_server_app_fn(update_type, server_id) {

    $.ajax({
        url: '/servers.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'server_id': server_id},
        success: function (data, response, status) {
            $("#delete_app_modal").modal('hide')
            $('#do_refresh').trigger("click");
        }
    });
}

