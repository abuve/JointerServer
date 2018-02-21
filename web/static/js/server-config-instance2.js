/**
 * Created by aaron on 2017/9/11.
 */

var InstanceTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function (app_id) {
        $('#instance_table').bootstrapTable({
            //url: '/server-instances-' + app_id + '.html',         //请求后台的URL（*）
            url: '/server/config/instance/json-' + app_id + '.html',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#instance_toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortName: 'Group',
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
                    title: 'Instance ID'
                },
                {
                    field: 'server__ipaddress',
                    title: 'IP Address'
                },
                {
                    field: 'instances__name',
                    title: 'Group',
                },
                {
                    field: 'instances__app_id__name',
                    title: 'Application',
                },
                {
                    field: 'instances__app_id__project_id__name',
                    title: 'Project',
                },
                {
                    field: 'name',
                    title: 'Options',
                    width: 240,
                    align: 'center',
                    formatter: instance_operateFormatter
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


var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };

    return oInit;
};

function instance_operateFormatter(value, row, index) {
        console.log(row.instances__id)
        return [
            '<div class="btn-group">',
            '<a type="button" class="btn btn-default btn-xs" onclick="edit_instance_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>',
            '<a type="button" class="btn btn-default btn-xs" onclick="delete_instance_data_fn(' + row.instances__id + ',' + row.id + ')"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>',
            '<a type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span> Option</a> <button type="button" class="btn btn-default dropdown-toggle btn-xs"data-toggle="1dropdown"> <span class="caret"></span> <span class="sr-only">切换下拉菜单</span> </button> <ul class="dropdown-menu" role="menu" style="margin:2px 164px; min-width:130px"> <li><a href="#">More Option</a></li> </ul>',
            '</div>'
        ].join('');
    }

function create_instance_fn() {
    $("#add_server_instance_form").trigger("reset");
    // 添加分组实例时，选择分组名
    $('select[name="add_instance_group_id"]').removeAttr("disabled", "true")
    $("#update_server_instance_fn").attr('onclick', 'do_create_instance_fn("post")')
}

function get_instance_type() {
    var recv_data
    $.ajax({
        url: '/get-server-instance_type.html',
        async: false,
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
           recv_data = data
        }
    });
    return recv_data
}

function delete_instance_data_fn(group_id, instance_id) {

    $("#instance_html_area").html("Confirm remove Instance ID " + instance_id + " ? All the data will be delete.")
    $("#delete_server_instance_fn").attr("onclick", "delete_server_instance_fn( " + group_id + "," + instance_id + ")")
    $("#delete_instance_modal").modal('show')

}

function edit_instance_data_fn(instance_id) {
    $("#update_server_instance_fn").attr("onclick", "update_server_instance_fn('put', " + instance_id + ")")

    $.ajax({
        url: '/server/config/instance/update-server-instance.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'instance_id': instance_id},
        success: function (data, response, status) {
            $("#add_instance_modal").modal('show')
            $('select[name="add_instance_group_id"]').val(data[0].instances__id);
            $('select[name="add_instance_ip"]').val(data[0].id);
            $('input[name="old_instance_id"]').val(data[0].id);

            // 修改分组实例时，禁止修改分组名
            $('select[name="add_instance_group_id"]').attr("disabled", "true")
        }
    });
}

function do_create_instance_fn(update_type, delete_instance_id) {

    var server_id = $('input[name="server_id"]').val();
    var add_instance_group_id = $('select[name="add_instance_group_id"]').val();
    var add_instance_id = $('select[name="add_instance_ip"]').val();
    //var add_instance_id = $('select[name="instance_select"]').val()

    $.ajax({
        url: '/server/config/instance/update-server-instance.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'add_instance_group_id': add_instance_group_id,
                'add_instance_id': add_instance_id,
                'server_id': server_id,
                'delete_instance_id': delete_instance_id},
        success: function (data, response, status) {
            $('#instance_table').bootstrapTable('refresh');
            $("#add_instance_modal").modal('hide');
            $("#delete_instance_modal").modal('hide');
            $("#add_server_instance_form").trigger("reset");
        }
    });
}

function update_server_instance_fn(update_type) {

    var instance_group_id = $('select[name="add_instance_group_id"]').val();
    var new_instance_id = $('select[name="add_instance_ip"]').val();
    var old_instance_id = $('input[name="old_instance_id"]').val();

    $.ajax({
        url: '/server/config/instance/update-server-instance.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'instance_group_id': instance_group_id,
                'new_instance_id': new_instance_id,
                'old_instance_id': old_instance_id},
        success: function (data, response, status) {
            $('#instance_table').bootstrapTable('refresh');
            $("#add_instance_modal").modal('hide');
            $("#delete_instance_modal").modal('hide');
            $("#add_server_instance_form").trigger("reset");
        }
    });
}

function delete_server_instance_fn(group_id, instance_id) {

    var server_id = $('input[name="server_id"]').val()

    $.ajax({
        url: '/server/config/instance/update-server-instance.html',
        type: 'delete',
        dataType: 'json',
        traditional:true,
        data: {'group_id': group_id,
                'instance_id': instance_id},
        success: function (data, response, status) {
            $('#instance_table').bootstrapTable('refresh');
            $("#delete_instance_modal").modal('hide')
        }
    });
}

function load_instance_fn(value) {

    var selectedOption = value.options[value.selectedIndex];

    if (selectedOption.value != 'None') {
        var asset_id = selectedOption.value

        $.ajax({
            url: '/cmdb/docker-json.html?condition=%7B"asset_id"%3A%5B' + asset_id + '%5D%7D',
            type: 'get',
            dataType: 'json',
            traditional:true,
            success: function (data, response, status) {
                console.log(data)
                if (data.status) {
                    $("#instance").html("")
                    for(var i in data.data.data_list){
                        $("#instance").append("<option value=" + data.data.data_list[i].id + ">" + data.data.data_list[i].name + "</option>")
                    }
                }
            }
        });

    }
}