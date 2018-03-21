function load_tree_data() {

    var setting = {
        data: {
            simpleData: {
                enable: true
            }
        }
    };

    $.ajax({
        url: '/cmdb/business-json.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                var zNodes = data.data
                $.fn.zTree.init($("#treeDemo"), setting, zNodes);
            }
        }
    });

}

function get_business_detail_fn(obj_id) {
    $.ajax({
        url: '/cmdb/business-detail-' + obj_id + '.html',
        type: 'get',
        success: function (data, response, status) {
            $("#business_detail_html_area").html(data)
        }
    });
}

function add_business_fn(obj_id) {

    // 绑定button为post事件
    $("#business_update_fn").attr("onclick", "do_post_business_fn()")
    $("#business_update_fn").html("Add")

    $.ajax({
        url: '/cmdb/business-json.html?add=true',
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
            console.log(data)
            if (data.status) {
                $("#add_business_parent_id").html("")
                $("#add_business_parent_id").append("<option value=''>创建一个父级业务线</option>")
                for(var i in data.data){
                    if (data.data[i].pId == 0) {
                        $("#add_business_parent_id").append("<option value=" + data.data[i].id + ">" + data.data[i].name + "</option>")
                    }
                }

                // 设置选中
                $("#add_business_parent_id ").val(obj_id);

                // admin groups
                $("#add_business_admin_id").html("")
                for(var i in data.group_data){
                    $("#add_business_admin_id").append("<option value=" + data.group_data[i].id + ">" + data.group_data[i].name + "</option>")
                }

                // user groups
                $("#add_business_contact_id").html("")
                for(var i in data.group_data){
                    $("#add_business_contact_id").append("<option value=" + data.group_data[i].id + ">" + data.group_data[i].name + "</option>")
                }

                $("#business_add_modal").modal('show')
            }
        }
    });
}

function do_post_business_fn() {

    var add_business_parent_id = $('select[name="add_business_parent_id"]').val()
    var add_business_name = $('input[name="add_business_name"]').val()

    var add_business_admin_list = []
    var add_business_contact_list = []

    $("#add_business_admin_id option:selected").each(function(){
        add_business_admin_list.push($(this).val())
    })

    $("#add_business_contact_id option:selected").each(function(){
        add_business_contact_list.push($(this).val())
    })

    var add_business_memo = $('#add_business_memo').val()

    $.ajax({
        url: '/cmdb/business-json.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        data : {
            "add_business_parent_id": add_business_parent_id,
            "add_business_name": add_business_name,
            "add_business_admin_list": add_business_admin_list,
            "add_business_contact_list": add_business_contact_list,
            "add_business_memo": add_business_memo,
        },
        success: function (data, response, status) {
            if (data.status) {
                $("#business_add_modal").modal('hide');
                load_tree_data();
                document.getElementById("add_business_form").reset();
            } else {
                $("#add_business_error").html(data.message)
            }
        }
    });
}

function delete_business_fn(obj_id, obj_name) {
    confirm_text = "Confirm delete business unit " + obj_name + " ?"
    $("#delete_business_html_area").html(confirm_text)
    $("#business_delete_modal").modal('show')
    $("#do_delete_business_fn").attr("onclick", "do_delete_business_fn(" + obj_id + ")")
}

function do_delete_business_fn(obj_id) {
    $.ajax({
        url: '/cmdb/business-json.html',
        type: 'delete',
        data : {"obj_id": obj_id},
        success: function (data, response, status) {
            if (data.status) {
                $("#business_delete_modal").modal('hide');
                $("#delete_business_html_area").html("")
                load_tree_data();
            } else {
                alert(data.message)
            }
        }
    });
}

function edit_business_fn(obj_id) {

    // 绑定button为put事件
    $("#business_update_fn").attr("onclick", "do_put_business_fn(" + obj_id + ")")

    $.ajax({
        url: '/cmdb/business-json.html?edit=true&obj_id=' + obj_id,
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
            console.log(data)
            if (data.status) {
                $("#add_business_parent_id").html("")
                $("#add_business_parent_id").append("<option value=''>Create Parent unit</option>")
                for(var i in data.data){
                    if (data.data[i].pId == 0) {
                        $("#add_business_parent_id").append("<option value=" + data.data[i].id + ">" + data.data[i].name + "</option>")
                    }
                }
                // 设置选中
                $("#add_business_parent_id ").val(data.edit_data.parent_unit_id);

                // business name
                $('input[name="add_business_name"]').val(data.edit_data.name)

                // admin groups
                $("#add_business_admin_id").html("")
                for(var i in data.group_data){
                    $("#add_business_admin_id").append("<option value=" + data.group_data[i].id + ">" + data.group_data[i].name + "</option>")
                }

                // 设置选中
                $("#add_business_admin_id").select2().val(data.edit_data.manager_groups).trigger("change");

                // user groups
                $("#add_business_contact_id").html("")
                for(var i in data.group_data){
                    $("#add_business_contact_id").append("<option value=" + data.group_data[i].id + ">" + data.group_data[i].name + "</option>")
                }

                // 设置选中
                $("#add_business_contact_id").select2().val(data.edit_data.contact_groups).trigger("change");

                // business memo
                $('#add_business_memo').val(data.edit_data.memo)

                $("#business_add_modal").modal('show')
            }
        }
    });
}

function do_put_business_fn(obj_id) {

    var add_business_parent_id = $('select[name="add_business_parent_id"]').val()
    var add_business_name = $('input[name="add_business_name"]').val()

    var add_business_admin_list = []
    var add_business_contact_list = []

    $("#add_business_admin_id option:selected").each(function(){
        add_business_admin_list.push($(this).val())
    })

    $("#add_business_contact_id option:selected").each(function(){
        add_business_contact_list.push($(this).val())
    })

    var add_business_memo = $('#add_business_memo').val()

    $.ajax({
        url: '/cmdb/business-json.html',
        type: 'put',
        dataType: 'json',
        traditional:true,
        data : {
            "obj_id": obj_id,
            "add_business_parent_id": add_business_parent_id,
            "add_business_name": add_business_name,
            "add_business_admin_list": add_business_admin_list,
            "add_business_contact_list": add_business_contact_list,
            "add_business_memo": add_business_memo,
        },
        success: function (data, response, status) {
            if (data.status) {
                $("#business_add_modal").modal('hide');
                load_tree_data();
                get_business_detail_fn(obj_id)
                document.getElementById("add_business_form").reset();
            } else {
                $("#add_business_error").html(data.message)
            }
        }
    });
}