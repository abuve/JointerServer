/**
 * Created by aaron on 2017/9/11.
 */

var LogsTableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function (app_id) {
        $('#urlmaps_table').bootstrapTable({
            url: '/server/config/urlmaps/json-' + app_id + '.html',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#urlmaps_toolbar',                //工具按钮用哪个容器
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
                    title: 'Url地址',
                    formatter: urlFormatter
                },
                {
                    field: 'memo',
                    title: '备注信息'
                },
                {
                    field: 'group_id__name',
                    title: '分组名称',
                },
                {
                    field: 'group_id__app_id__name',
                    title: '应用名称',
                },
                {
                    field: 'group_id__app_id__project_id__name',
                    title: '项目名称',
                },
                {
                    field: 'name',
                    title: '操作',
                    width: 460,
                    align: 'center',
                    formatter: button_operateFoarmatter
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

function urlFormatter(value, row, index) {
    return [
        '<a href="' + row.url + '" target="_blank">' + row.url + '</a>'
    ]
}

function button_operateFoarmatter(value, row, index) {
    return [
        '<div class="btn-group">',
        '<a type="button" class="btn btn-default btn-xs" onclick="detail_urlmaps_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-search" aria-hidden="true"></span> 映射详情</a>',
        '<a type="button" class="btn btn-default btn-xs no-radius" onclick="edit_urlmaps_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-edit" aria-hidden="true"></span> 编辑</a>',
        '<a type="button" class="btn btn-default btn-xs no-radius" onclick="delete_urlmaps_data_fn(' + row.id + ')"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span> 删除</a>',
        '</div>',
        '&nbsp;',
        '<div class="btn-group">',
        '<a type="button" class="btn btn-primary btn-xs no-radius" onclick="update_urlmaps_group_fn(\'cloud\',' + row.group_id_id + ',' + row.id + ')"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span> 一层转发</a>',
        '<a type="button" class="btn btn-primary btn-xs no-radius" onclick="update_urlmaps_group_fn(\'forward\',' + row.group_id_id + ',' + row.id + ')"><span class="glyphicon glyphicon-indent-left" aria-hidden="true"></span> 二层转发</a>',
        '<a type="button" class="btn btn-primary btn-xs" onclick="update_urlmaps_group_fn(\'docker\',' + row.group_id_id + ',' + row.id + ')"><span class="glyphicon glyphicon-leaf" aria-hidden="true"></span> Docker实例</a>',
        '</div>'
    ].join('');
}

function detail_urlmaps_data_fn(urlmaps_id) {
    $.ajax({
        url: '/server/config/urlmaps/get_urlmaps_detail.html',
        type: 'post',
        traditional:true,
        data: {'urlmaps_id': urlmaps_id},
        success: function (data, response, status) {
            $('#detail_urlmaps_modal').modal('show');
            $('#detail_urlmaps_html').html(data)
        }
    });
}

function create_urlmaps_fn() {
    $("#update_urlmaps_form").trigger("reset");
    $("#update_urlmaps_fn").attr('onclick', 'update_urlmaps_fn("post")')
}

function delete_urlmaps_data_fn(urlmaps_id) {

    $("#delete_urlmaps_html_area").html("Confirm remove UrlMap ID " + urlmaps_id + " ?")
    $("#delete_urlmaps_data_fn").attr("onclick", "do_delete_urlmaps_fn(" + urlmaps_id + ")")
    $("#delete_urlmaps_modal").modal('show')

}

function edit_urlmaps_data_fn(urlmaps_id) {
    $("#update_urlmaps_fn").attr("onclick", "update_urlmaps_fn('put', " + urlmaps_id + ")")

    $.ajax({
        url: '/server/config/urlmaps/update-server-urlmaps.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'urlmaps_id': urlmaps_id},
        success: function (data, response, status) {

            $('input[name="urlmaps_url"]').val(data[0].url);
            $('select[name="urlmaps_group_id"]').val(data[0].group_id_id);
            $('select[name="urlmaps_cloud_id"]').val(data[0].cloud__id);
            $('select[name="urlmaps_forward_id"]').val(data[0].forward__id);
            $('select[name="urlmaps_instance_id"]').val(data[0].docker__id);
            $('textarea[name="urlmaps_memo"]').val(data[0].memo);
            $("#create_url_maps_modal").modal('show')

        }
    });
}

function update_urlmaps_group_fn(group_type, group_id, urlmaps_id) {
    // 判断当前分组选择的实例分组
    // $('select[name="urlmaps_group_id"]').val(group_id);
    $('input[name="urlmaps_group_type"]').val(group_type);

    // 根据当前分组id 获取相应的选择实例
    $.ajax({
        url: '/server/config/urlmaps/update-server-urlmaps-groups.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        data: {'group_type': group_type, 'group_id': group_id, 'urlmaps_id': urlmaps_id},
        success: function (data, response, status) {
            $('input[name="urlmaps_groups_url"]').val(data.urlmaps_obj[0].url);
            $("#select1").html("");
            // for(var index in data.left_select_list){
            //     $("#select1").append("<option value=" + data.left_select_list[index][0] + ">" + data.left_select_list[index][1] + "</option>")
            // }
            $("#select2").html("");
            if (group_type == 'docker') {
                for(var index in data.right_select_list){
                    $("#select2").append("<option value=" + data.right_select_list[index].id + ">" + data.right_select_list[index].asset__server__ipaddress + ":" + data.right_select_list[index].port + "</option>")
                }
            } else {
                for(var index in data.right_select_list){
                    $("#select2").append("<option value=" + data.right_select_list[index].id + ">" + data.right_select_list[index].server__ipaddress + "</option>")
                }
            }
        }
    });
    $("#do_update_urlmaps_groups").attr("onclick", "do_update_urlmaps_groups(" + group_id + ',' + urlmaps_id + ")")
    $('#urlmaps_group_modal').modal('show')
}

function load_instance_component_fn(value) {

    var selectedOption = value.options[value.selectedIndex];
    var group_type = $('input[name="urlmaps_group_type"]').val();

    if (selectedOption.value != 'None') {
        var group_id = selectedOption.value

        $.ajax({
            url: '/server/config/instance/get-instance-by-groupid.html',
            type: 'get',
            dataType: 'json',
            traditional:true,
            data: {'group_id': group_id, 'group_type': group_type},
            success: function (data, response, status) {
                if (data.status) {
                    $("#select1").html("")
                    //$("#select2").html("")
                    if (group_type=='docker') {
                        for(var i in data.data){
                            $("#select1").append("<option value=" + data.data[i].id + ">" + data.data[i].asset__server__ipaddress + ":" + data.data[i].port + "</option>")
                        }
                    } else {
                        for(var i in data.data){
                            $("#select1").append("<option value=" + data.data[i].id + ">" + data.data[i].server__ipaddress + "</option>")
                        }
                    }
                }
            }
        });

    }
}

function do_update_urlmaps_groups(group_id, urlmaps_id) {
    instance_list = []
    var group_type = $('input[name="urlmaps_group_type"]').val();
    $("#select2 option").each(function(){
        instance_list.push($(this).val())
    })
    $.ajax({
            url: '/server/config/urlmaps/update-server-urlmaps-groups.html',
            type: 'post',
            dataType: 'json',
            traditional: true,
            data: {
                'group_id': group_id,
                'group_type': group_type,
                'urlmaps_id': urlmaps_id,
                'instance_list': instance_list,
            },
            success: function (data, response, status) {
                $('#urlmaps_group_modal').modal('hide')
            }
        });
}

function checkUrl(urlString){
    if(urlString!=""){
        var reg=/(http|ftp|https|ws):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?/;
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

function update_urlmaps_fn(update_type, urlmaps_id) {

    var urlmaps_url = $('input[name="urlmaps_url"]').val();
    var urlmaps_group_id = $('select[name="urlmaps_group_id"]').val();
    var urlmaps_memo = $('select[name="urlmaps_memo"]').val();

    if (checkUrl(urlmaps_url)) {
        $.ajax({
            url: '/server/config/urlmaps/update-server-urlmaps.html',
            type: update_type,
            dataType: 'json',
            traditional: true,
            data: {
                'urlmaps_id': urlmaps_id,
                'urlmaps_url': urlmaps_url,
                'urlmaps_group_id': urlmaps_group_id,
                'urlmaps_memo': urlmaps_memo,
            },
            success: function (data, response, status) {
                $('#urlmaps_table').bootstrapTable('refresh');
                $("#create_url_maps_modal").modal('hide');
                $("#update_urlmaps_form").trigger("reset");
            }
        });
    }
}

function do_delete_urlmaps_fn(urlmaps_id) {
    $.ajax({
        url: '/server/config/urlmaps/update-server-urlmaps.html',
        type: 'delete',
        dataType: 'json',
        traditional:true,
        data: {'urlmaps_id': urlmaps_id},
        success: function (data, response, status) {
            $('#urlmaps_table').bootstrapTable('refresh');
            $("#delete_urlmaps_modal").modal('hide')
        }
    });
}

$(function(){
	//移到右边
	$('#add').click(function(){
		//先判断是否有选中
		if(!$("#select1 option").is(":selected")){
			alert("请选择需要移动的选项")
		}
		//获取选中的选项，删除并追加给对方
		else{
			$('#select1 option:selected').appendTo('#select2');
		}
	});

	//移到左边
	$('#remove').click(function(){
		//先判断是否有选中
		if(!$("#select2 option").is(":selected")){
			alert("请选择需要移动的选项")
		}
		else{
			$('#select2 option:selected').appendTo('#select1');
		}
	});

	//全部移到右边
	$('#add_all').click(function(){
		//获取全部的选项,删除并追加给对方
		$('#select1 option').appendTo('#select2');
	});

	//全部移到左边
	$('#remove_all').click(function(){
		$('#select2 option').appendTo('#select1');
	});

	//双击选项
	$('#select1').dblclick(function(){ //绑定双击事件
		//获取全部的选项,删除并追加给对方
		$("option:selected",this).appendTo('#select2'); //追加给对方
	});

	//双击选项
	$('#select2').dblclick(function(){
		$("option:selected",this).appendTo('#select1');
	});

});