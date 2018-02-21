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


function delete_project_data_fn(project_id) {
    $("#delete_data_html_area").html("Confirm remove Application? All the data will be delete!");
    $("#delete_project_app_fn").attr("onclick", "delete_project_app_fn('delete', " + project_id + ")");
    $("#delete_app_modal").modal('show')
}

function update_project_app_fn(update_type, project_id) {

    var project_name = $('input[name="project_name"]').val();
    var business_unit_id = $('input[name="business_unit_id"]').val();

    $.ajax({
        url: '/projects.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'project_id': project_id, 'project_name': project_name, 'business_unit_id': business_unit_id},
        success: function (data, response, status) {
            window.location.href = "/project.html"
        }
    });
}

function delete_project_app_fn(update_type, project_id) {

    $.ajax({
        url: '/projects.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'project_id': project_id},
        success: function (data, response, status) {
            $("#delete_app_modal").modal('hide');
            $('#do_refresh').trigger("click");
        }
    });
}

function load_appviews_detail_fn(app_id) {
    // 激活头部菜单
    $(".appviews_nav_control").removeClass('active')
    $("#" + app_id).addClass('active')

    $.ajax({
        url: '/server-config-' + app_id + '.html',
        type: 'get',
        traditional:true,
        data: {'data_from': 'appviews'},
        success: function (data, response, status) {
            $("#appviews_detail_html").html(data)
        }
    });
}

function default_appviews_detail_fn(app_id) {
    load_appviews_detail_fn(app_id)
}
