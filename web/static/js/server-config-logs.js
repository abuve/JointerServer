/**
 * Created by aaron on 2017/9/11.
 */

var LogsTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function (app_id) {
        $('#logs_table').bootstrapTable({
            url: '/server/config/logs/json-' + app_id + '.html',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#logs_toolbar',                //工具按钮用哪个容器
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
                    title: 'ID'
                },
                {
                    field: 'url',
                    title: 'Logs Url'
                },
                {
                    field: 'memo',
                    title: 'Logs Memo'
                },
                {
                    field: 'group_id__name',
                    title: 'Group Name',
                },
                {
                    field: 'group_id__app_id__name',
                    title: 'Application',
                },
                {
                    field: 'group_id__app_id__project_id__name',
                    title: 'Project',
                },
                {
                    field: 'name',
                    title: 'Options',
                    width: 240,
                    align: 'center',
                    formatter: docker_operateFormatter
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

function docker_operateFormatter(value, row, index) {
        return [
            '<div class="btn-group">',
            '<a type="button" class="btn btn-default btn-xs" onclick="edit_logs_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> Edit</a>',
            '<a type="button" class="btn btn-default btn-xs" onclick="delete_logs_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Delete</a>',
            '<a type="button" class="btn btn-default btn-xs"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span> Option</a> <button type="button" class="btn btn-default dropdown-toggle btn-xs"data-toggle="1dropdown"> <span class="caret"></span> <span class="sr-only">切换下拉菜单</span> </button> <ul class="dropdown-menu" role="menu" style="margin:2px 164px; min-width:130px"> <li><a href="#">More Option</a></li> </ul>',
            '</div>'
        ].join('');
    }

function bond_logs_fn() {
    $("#add_server_logs_form").trigger("reset");
    // 添加分组实例时，选择分组名
    $('select[name="add_logs_group_id"]').removeAttr("disabled", "true")
    $("#update_server_logs_fn").attr('onclick', 'do_bond_logs_fn()')
}

function delete_logs_data_fn(log_id) {

    $("#delete_logs_html_area").html("Confirm remove Logs ID " + log_id + " ? All the data will be delete.")
    $("#delete_server_logs_fn").attr("onclick", "delete_server_logs_fn( " + log_id + ")")
    $("#delete_logs_modal").modal('show')

}

function edit_logs_data_fn(log_id) {
    $("#update_server_logs_fn").attr("onclick", "update_server_logs_fn('put', " + log_id + ")")

    $.ajax({
        url: '/server/config/logs/update-server-logs.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'log_id': log_id},
        success: function (data, response, status) {
            $("#add_logs_modal").modal('show')
            $('select[name="add_logs_group_id"]').val(data[0].group_id_id);
            $('input[name="add_server_log_url"]').val(data[0].url);
            $('textarea[name="add_server_log_memo"]').val(data[0].memo);

            // 修改日志时，禁止修改分组名
            $('select[name="add_logs_group_id"]').attr("disabled", "true")
        }
    });
}

function checkUrl(urlString){
    if(urlString!=""){
        var reg=/(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/;
        if(!reg.test(urlString)){
            alert("Error Http Url...");
            return false;
        } else {
            return true;
        }
    } else {
        alert('Please enter url address...');
        return false;
    }
}

function do_bond_logs_fn() {

    var server_id = $('input[name="server_id"]').val();
    var add_logs_group_id = $('select[name="add_logs_group_id"]').val();
    var add_server_log_url = $('input[name="add_server_log_url"]').val();
    var add_server_log_memo = $('textarea[name="add_server_log_memo"]').val();

    if (checkUrl(add_server_log_url)) {
        $.ajax({
            url: '/server/config/logs/update-server-logs.html',
            type: 'post',
            dataType: 'json',
            traditional:true,
            data: {'add_logs_group_id': add_logs_group_id,
                'add_server_log_url': add_server_log_url,
                'add_server_log_memo': add_server_log_memo},
            success: function (data, response, status) {
                $('#logs_table').bootstrapTable('refresh');
                $("#add_logs_modal").modal('hide');
                $("#add_server_logs_form").trigger("reset");
            }
        });
    }
}

function update_server_logs_fn(update_type, log_id) {

    var add_server_log_url = $('input[name="add_server_log_url"]').val();
    var add_server_log_memo = $('textarea[name="add_server_log_memo"]').val();

    if (checkUrl(add_server_log_url)) {
        $.ajax({
            url: '/server/config/logs/update-server-logs.html',
            type: update_type,
            dataType: 'json',
            traditional: true,
            data: {
                'add_server_log_url': add_server_log_url,
                'add_server_log_memo': add_server_log_memo,
                'log_id': log_id
            },
            success: function (data, response, status) {
                $('#logs_table').bootstrapTable('refresh');
                $("#add_logs_modal").modal('hide');
                $("#add_server_logs_form").trigger("reset");
            }
        });
    }
}

function delete_server_logs_fn(log_id) {
    $.ajax({
        url: '/server/config/logs/update-server-logs.html',
        type: 'delete',
        dataType: 'json',
        traditional:true,
        data: {'log_id': log_id},
        success: function (data, response, status) {
            $('#logs_table').bootstrapTable('refresh');
            $("#delete_logs_modal").modal('hide')
        }
    });
}