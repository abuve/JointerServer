/**
 * Created by aaron on 2017/9/11.
 */


var GroupTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function (app_id) {
        $('#group_table').bootstrapTable({
            url: '/server/config/group/json-' + app_id + '.html',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#group_toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            //height: 300,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [
                {
                    field: 'id',
                    title: '分组ID'
                },
                {
                    field: 'name',
                    title: '分组名称'
                },
                {
                    field: 'app_id__name',
                    title: '应用名称'
                },
                {
                    field: 'app_id__project_id__name',
                    title: '项目名称'
                },
                {
                    field: 'group_type',
                    title: '分组类型',
                    formatter: group_type_formatter
                },
                {
                    field: 'name',
                    title: '操作',
                    width: 330,
                    align: 'center',
                    formatter: group_operateFormatter
                },
            ]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            departmentname: $("#txt_search_departmentname").val(),
            statu: $("#txt_search_statu").val()
        };
        return temp;
    };
    return oTableInit;
};

function group_operateFormatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<a type="button" class="btn btn-default btn-xs" onclick="edit_group_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> 编辑</a>',
        '<a type="button" class="btn btn-default btn-xs" onclick=delete_group_data_fn(' + row.id + ',' + JSON.stringify(row.name) + ')><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> 删除</a>',
        '<a type="button" class="btn btn-default btn-xs" onclick="get_yaml_conf_fn(' + row.id + ')"><span class="glyphicon glyphicon-book" aria-hidden="true"></span> Docker YAML</a>',
        // '<a type="button" class="btn btn-default btn-xs" onclick="group_edit_fn(' + row.id + ')"><span class="glyphicon glyphicon-send" aria-hidden="true"></span> Instances</a>',
        '<a type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-tags" aria-hidden="true"></span> 实例信息</a> <button type="button" class="btn btn-default dropdown-toggle btn-xs"data-toggle="dropdown"> <span class="caret"></span> <span class="sr-only">切换下拉菜单</span> </button> <ul class="dropdown-menu" role="menu" style="margin:2px 164px; min-width:130px"> <li><a href="#">More Option</a></li> </ul>',
        '</div>'
    ].join('');
}

function group_type_formatter(value, row, index) {
    if (row.group_type == 0) {
        var btn_html = '<a type="button" class="btn btn-primary btn-xs"><span class="glyphicon glyphicon-tag" aria-hidden="true"></span> 私有分组</a>'
    } else if (row.group_type == 1) {
        var btn_html = '<a type="button" class="btn btn-success btn-xs"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span> 公共分组</a>'
    }
    return [
        '<div class="btn-group">' + btn_html + '</div>'
    ].join('');
}


function create_group_fn() {
    $("#add_server_group_form").trigger("reset");
    $("#update_server_group_fn").attr('onclick', 'update_server_group_fn("post")')
}

function delete_group_data_fn(group_id, group_name) {

    $("#group_html_area").html("确认删除分组 <span style='font-weight:bold; color: red;'>" + group_name + "</span> 吗? 该分组所有相关数据将会被删除！")
    $("#delete_server_group_fn").attr("onclick", "update_server_group_fn('delete', " + group_id + ")")
    $("#delete_group_modal").modal('show')

}

function edit_group_data_fn(group_id) {

    $("#update_server_group_fn").attr("onclick", "update_server_group_fn('put', " + group_id + ")")

    $.ajax({
        url: '/server/config/group/update-server-group.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'group_id': group_id},
        success: function (data, response, status) {
            $("#add_group_modal").modal('show')
            $('input[name="add_group_name"]').val(data[0].name)
            $('input[name="add_group_yaml_path"]').val(data[0].yaml_path)
            $("#add_group_type_" + data[0].group_type).prop("checked", true);
        }
    });

}

function update_server_group_fn(update_type, group_id) {

    var add_group_name = $('input[name="add_group_name"]').val()
    var add_group_app_id = $('input[name="add_group_app_id"]').val()
    var add_group_yaml_path = $('input[name="add_group_yaml_path"]').val()
    var add_group_type = $('input[name="add_group_type"]:checked').val()

    $.ajax({
        url: '/server/config/group/update-server-group.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'add_group_name': add_group_name, 'add_group_app_id': add_group_app_id, 'add_group_yaml_path': add_group_yaml_path, 'group_id': group_id, 'add_group_type': add_group_type},
        success: function (data, response, status) {
            $('#group_table').bootstrapTable('refresh');
            $("#add_group_modal").modal('hide')
            $("#delete_group_modal").modal('hide')
            $("#add_server_group_form").trigger("reset");
        }
    });
}

function get_yaml_conf_fn(group_id) {
    $("#yaml_conf_html").html("");

    $.ajax({
        url: '/update-yaml-nginx.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'group_id': group_id},
        success: function (data, response, status) {
            if (data.status) {
                $("#yaml_conf_html").html(data.data.yaml_data)
                $("#edit_yaml_conf_btn").html("Edit")
                $("#edit_yaml_conf_btn").attr("onclick", "edit_yaml_conf_fn(" + group_id + ")")
            } else {
                $("#yaml_conf_html").html('Not found YAML File, Create first.')
                $("#edit_yaml_conf_btn").html("Add")
                $("#edit_yaml_conf_btn").attr("onclick", "add_yaml_conf_fn(" + group_id + ")")
            }
        }
    });

    $("#yaml_update_modal").modal('show')
}

function add_yaml_conf_fn(group_id) {

    $("#yaml_conf_html").html('<textarea type="textarea" class="form-control" name="yaml_conf_data" rows="30"></textarea>')

    $("#edit_yaml_conf_btn").html("Save")
    $("#edit_yaml_conf_btn").attr("onclick", "yaml_update_fn('post'," + group_id + ")")
}

function edit_yaml_conf_fn(group_id) {

    $.ajax({
        url: '/update-yaml-nginx.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'group_id': group_id},
        success: function (data, response, status) {
            if (data.status) {
                $("#yaml_conf_html").html('<textarea type="textarea" class="form-control" name="yaml_conf_data" rows="30">' + data.data.yaml_data + '</textarea>')
            } else {
                $("#yaml_conf_html").html('<textarea type="textarea" class="form-control" name="yaml_conf_data" rows="30"></textarea>')
            }
        }
    });

    $("#edit_yaml_conf_btn").html("Save")
    $("#edit_yaml_conf_btn").attr("onclick", "yaml_update_fn('put'," + group_id + ")")
}


function yaml_update_fn(update_type, group_id) {

    var yaml_conf_data = $('textarea[name="yaml_conf_data"]').val()

    $.ajax({
        url: '/update-yaml-nginx.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'yaml_conf_data': yaml_conf_data, 'group_id': group_id},
        success: function (data, response, status) {
            get_yaml_conf_fn(group_id)
            $("#edit_yaml_conf_btn").html("Edit")
            $("#edit_yaml_conf_btn").attr("onclick", "edit_yaml_conf_fn(" + group_id + ")")

        }
    });
}

function bond_public_group_fn() {

    var add_group_app_id = $('input[name="add_group_app_id"]').val()

    $.ajax({
        url: '/server/config/group/update-public-group.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
            $("#bond_public_group").html("")
            $.each(data, function( index, value ) {
                if (value.group_type == 1) {
                    $("#bond_public_group").append("<option value=" + data[index].id + ">" + data[index].name + "</option>")
                }
            });
        }
    });

}

function do_bond_public_group() {

    var add_group_app_id = $('input[name="add_group_app_id"]').val()
    var public_group_id = $("select[name='bond_public_group']").val()

    $.ajax({
        url: '/server/config/group/update-public-group.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        data: {'add_group_app_id': add_group_app_id, 'public_group_id': public_group_id},
        success: function (data, response, status) {
            $('#group_table').bootstrapTable('refresh');
            $("#add_public_group_modal").modal('hide')
        }
    });

}