/**
 * Created by aaron on 2017/9/11.
 */

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

function role_create_fn() {
    var role_name = $('input[name="role_name"]').val()
    var role_memo = $('input[name="role_memo"]').val()
	var permission_list = []

    $("#select2 option").each(function(){
        permission_list.push($(this).val())
    })

    $.ajax({
        url: '/user_center/roles-json.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        data: {'role_name': role_name, 'role_memo': role_memo, 'permission_list':permission_list},
        success: function (data, response, status) {
            if (data.status) {
                window.location.href = "/user_center/roles-list.html"
            }
        }
    });
}

function delete_role_fn(obj_id) {
    $("#delete_data_html_area").html("Confirm remove Role?");
    $("#delete_role_fn").attr("onclick", "do_delete_role(" + obj_id + ")");
    $("#role_delete_modal").modal('show')
}

function do_delete_role(obj_id) {
    $.ajax({
        url: '/user_center/roles-json.html',
        type: 'delete',
        dataType: 'json',
        traditional:true,
        data: {'obj_id': obj_id},
        success: function (data, response, status) {
            $("#role_delete_modal").modal('hide');
            $('#do_refresh').trigger("click");
        }
    });
}

function role_update_fn() {
    var role_id = $('input[name="role_id"]').val()
    var role_name = $('input[name="role_name"]').val()
    var role_memo = $('input[name="role_memo"]').val()
	var permission_list = []

    $("#select2 option").each(function(){
        permission_list.push($(this).val())
    })

    $.ajax({
        url: '/user_center/roles-json.html',
        type: 'put',
        dataType: 'json',
        traditional:true,
        data: {'role_id': role_id, 'role_name': role_name, 'role_memo': role_memo, 'permission_list':permission_list},
        success: function (data, response, status) {
            if (data.status) {
                window.location.href = "/user_center/roles-list.html"
            }
        }
    });
}