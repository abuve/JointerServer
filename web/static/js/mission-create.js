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

function load_app_component_fn(value) {

    var selectedOption = value.options[value.selectedIndex];

    if (selectedOption.value != 'None') {
        var project_id = selectedOption.value

        $.ajax({
            url: '/get_app_by_project/',
            type: 'post',
            dataType: 'json',
            traditional:true,
            data: {'project_id': project_id},
            success: function (data, response, status) {
                if (data.status) {
                    $("#select1").html("")
                    for(var i in data.data){
                        $("#select1").append("<option value=" + data.data[i].id + ">" + data.data[i].name + "</option>")
                    }
                }
            }
        });

    }
}

function mission_create_fn() {

	var mission_name = $('input[name="mission_name"]').val()
	var mission_type = $('select[name="mission_type"]').val()
	var project_name = $('#project_name option:selected').text()
	var app_list = []

    $("#select2 option").each(function(){
        app_list.push($(this).val())
    })

    $.ajax({
        url: '/mission-create.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        data: {'mission_name': mission_name, 'mission_type': mission_type, 'project_name':project_name, 'app_list': app_list},
        success: function (data, response, status) {
            if (data.status) {
                window.location.href = "/mission-detail-" + data.data.mission_id + ".html"
            }
        }
    });

}