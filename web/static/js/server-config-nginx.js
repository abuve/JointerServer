/* 重新加载根节点 */
function reload_tree() {
    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()
    var setting = {
        view: {
            selectedMulti: false
        },
        async: {
            enable: true,
            url:"/server/webconf/nginx/fileTreeJson-56.html?version=2017-12-28-09-11-22",
            autoParam:["id", "name=n", "level=lv"],
            otherParam:{"server_id": server_id, "version": version},
        },
        callback: {
            onClick: zTreeOnClick
        }
    };

    $.fn.zTree.init($("#treeDemo"), setting);
}

/* 重新加载选中节点 */
function reload_tree_selected(only_parent) {
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getSelectedNodes();
    console.log(nodes)
    if (nodes.length > 0) {
        if (only_parent) {
            var node = nodes[0].getParentNode()
        } else if (! nodes[0].isParent) {
            var node = nodes[0].getParentNode()
        } else {
            var node = nodes[0]
        }
        treeObj.reAsyncChildNodes(node, "refresh");
    } else {
        reload_tree()
    }
}

function load_tree_data(server_id, version) {

    $("#select_version_html_area").html(version);
    $("#version_display_html").html("Version：" + version);

    var setting = {
        view: {
            selectedMulti: false
        },
        async: {
            enable: true,
            url:"/server/webconf/nginx/fileTreeJson-56.html?version=2017-12-28-09-11-22",
            autoParam:["id", "name=n", "level=lv"],
            otherParam:{"server_id": server_id, "version": version},
        },
        callback: {
            onClick: zTreeOnClick
        }
    };

    $.fn.zTree.init($("#treeDemo"), setting);

    edit_btn_switch('off')

    // 设置当前选择版本&server_id
    $("input[name='select_version_name']").val(version)
    $("input[name='select_server_id']").val(server_id)
}

function zTreeOnClick(event, treeId, treeNode) {
    console.log(event, treeId)
    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()
    if ( ! treeNode.isParent ){
        // 加载文件内容
        $.ajax({
            url: '/server/webconf/nginx/file-data-' + server_id + '.html',
            type: 'get',
            dataType: 'json',
            data: {'version': version, 'select_id': treeNode.id},
            traditional:true,
            success: function (data, response, status) {
                if (data.status) {
                    $("#conf_html_area").html(data.data)
                    hljs.initHighlighting.called = false;
                    hljs.initHighlighting();
                } else {

                }
            }
        });
    }
};

function load_version_info(server_id) {
    $.ajax({
        url: '/server/webconf/nginx/version-json-' + server_id + '.html',
        async: false,
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                console.log(data.data)
                version_data = data.data
            } else {
                version_data = null
            }
        }
    });
    return version_data
}

function create_last_version(server_id) {
    $.ajax({
        url: '/server/webconf/nginx/version-json-' + server_id + '.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
           if (data.status) {
               set_version_info(server_id)
               alert("Nginx初始版本创建成功！")
           }
        }
    });
}

// function set_version_info(server_id) {
//     var version_data_list = load_version_info(server_id)
//     if (version_data_list) {
//         version_list_html = ''
//         $.each(version_data_list, function( index, value ) {
//             version_list_html += '<li><a href="#" onclick=\'load_tree_data(' + server_id + ',"'+value.name+'"),alert(123)\'>' + value.name + '</a></li>'
//         });
//         $("#version_list_area").html(version_list_html)
//     } else {
//         $("#version_list_area").html('<li><a href="#" onclick="create_last_version('+ server_id +')">无版本信息，点击创建！</a></li>')
//     }
// }

function set_version_info(server_id) {

    var has_last_version_tag = false

    get_version_list_from_dir = load_version_info(server_id)
    $.each(get_version_list_from_dir, function( index, value ) {
        if (value.name == 'last_version') {
            has_last_version_tag = true
        }
    });

    var version_list_html = ''

    $.ajax({
        url: '/server/webconf/nginx/version-tree-' + server_id + '.html',
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
            if (data.status && ! data.data.length == 0 && has_last_version_tag) {
                version_list_html += '<li><a href="#" onclick=\'load_tree_data(' + server_id + ',"last_version")\'>last_version</a></li>'
                $.each(data.data, function( index, value ) {
                    version_list_html += '<li><a href="#" onclick=\'load_tree_data(' + server_id + ',"' + value.version  + '"), ' + 'load_version_status(' + value.id + ')' +  '\'>' + value.version + '</a></li>'
                });
                $("#version_list_area").html(version_list_html)
            } else if (has_last_version_tag) {
                version_list_html += '<li><a href="#" onclick=\'load_tree_data(' + server_id + ',"last_version")\'>last_version</a></li>'
                $("#version_list_area").html(version_list_html)
            }
            else {
                $("#version_list_area").html('<li><a href="#" onclick="create_last_version('+ server_id +')">无版本信息，点击创建！</a></li>')
            }
        }
    });

    console.log(load_version_info(server_id))
}

function enter_edit_fn() {
    $("#enter_edit_confirm_modal").modal('show')
}

function enter_edit_confirm_fn() {

    // 将当前版本覆盖至last_version
    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()
    if (version != "last_version"){
        $.ajax({
            url: '/server/webconf/nginx/version-json-' + server_id + '.html',
            type: 'put',
            dataType: 'json',
            data: {'version': version},
            traditional:true,
            success: function (data, response, status) {
                if (data.status) {
                    load_tree_data(server_id, 'last_version')
                    edit_btn_switch('on')
                }
            }
        });
    } else {
        edit_btn_switch('on')
    }

    $("#enter_edit_confirm_modal").modal('hide')

}

function edit_btn_switch(tag) {
    if (tag=='on') {
        // 激活编辑功能按钮
        $("#create_btn").removeAttr("disabled");
        $("#delete_btn").removeAttr("disabled");
        $("#edit_btn").removeAttr("disabled");
        $("#upload_btn").removeAttr("disabled");
        $("#update_btn").removeAttr("disabled");

        // 关闭进入编辑功能
        $("#enter_edit_btn").attr("disabled", "true")

    } else if (tag=='off') {
        // 关闭编辑功能按钮
        $("#create_btn").attr("disabled", "true")
        $("#delete_btn").attr("disabled", "true")
        $("#edit_btn").attr("disabled", "true")
        $("#upload_btn").attr("disabled", "true")
        $("#update_btn").attr("disabled", "true")

        // 激活进入编辑按钮
        $("#enter_edit_btn").removeAttr("disabled");
    }
}

function get_current_tree_node() {
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getSelectedNodes();
    return nodes[0]
}

function get_current_tree_path(file_tag) {
    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getSelectedNodes();
    var dir_path_list = []

    dir_path_str = '/'

    if (nodes.length != 0) {
        var node = nodes[0]
        for(i=0; i<=nodes[0].level; i++) {
            node = node.getParentNode()
            if (! node) {
                break
            }
            dir_path_list.unshift(node.name)
        }

        for (index in dir_path_list) {
            dir_path_str += dir_path_list[index] + '/'
        }

        if (file_tag) {
            dir_path_str += nodes[0].name
        } else {
            if (nodes[0].isParent) {
                dir_path_str += nodes[0].name + '/'
            }
        }

    }

    return dir_path_str
}

/* 新增文件 & 目录 */

function create_fn() {
    var dir_path = get_current_tree_path(file_tag=false)
    $("input[name='create_object_path']").val(dir_path)
    $("#create_modal").modal('show')
}

function do_create() {
    var create_object_name = $("input[name='create_object_name']").val()
    var create_object_path = $("input[name='create_object_path']").val()
    var create_object_type = $("input[name='create_object_type']:checked").val()

    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()

    if (create_object_name.length == 0) {
        alert("Please enter file name.")
        return false
    }

    $.ajax({
        url: '/server/webconf/nginx/file-data-' + server_id + '.html',
        type: 'post',
        dataType: 'json',
        data: {'version': version, 'create_object_name': create_object_name, 'create_object_path': create_object_path, 'create_object_type': create_object_type},
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                // 文件创建成功，刷新列表
                $("#create_modal").modal('hide')
                reload_tree_selected()
                document.getElementById("object_create_form").reset();
                $("#error_msg_handle").html('')

            } else {
                // 显示错误提示信息
                $("#error_msg_handle").show()
                $("#error_msg_handle").html(data.message)
                return false
            }
        }
    });
}

/* 删除文件 & 目录 */

function delete_fn() {
    var dir_path = get_current_tree_path(file_tag=true)
    if (dir_path=='/') {
        alert('请选择需要删除的项目！')
    } else {
        var delete_object_html = "确定要删除 <b>" + dir_path + "</b> 吗？ 如果所选项目为目录，那么该目录下的所有文件将全部被删除！"
        $("#delete_object_html").html(delete_object_html)
        $("input[name='delete_object_path']").val(dir_path)
        $("#delete_modal").modal('show')
    }
}

function do_delete() {

    var delete_object_path = $("input[name='delete_object_path']").val()

    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()

    $.ajax({
        url: '/server/webconf/nginx/file-data-' + server_id + '.html',
        type: 'delete',
        dataType: 'json',
        data: {'version': version, 'delete_object_path': delete_object_path},
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                // 文件删除成功，刷新列表
                $("#delete_modal").modal('hide')
                reload_tree_selected(only_parent=true)
            } else {
                alert(data.message)
            }
        }
    });
}

function edit_fn() {
    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()

    var treeObj = $.fn.zTree.getZTreeObj("treeDemo");
    var nodes = treeObj.getSelectedNodes();

    var tree_node = get_current_tree_node()
    if (tree_node) {
        // 编辑文件
        if (! tree_node.isParent) {
            var dir_path = get_current_tree_path(file_tag=true)
            $("input[name='edit_object_path']").val(dir_path)

            $.ajax({
                url: '/server/webconf/nginx/file-data-' + server_id + '.html',
                type: 'get',
                dataType: 'json',
                data: {'version': version, 'select_id': nodes[0].id},
                traditional:true,
                success: function (data, response, status) {
                    if (data.status) {
                        $("textarea[name='edit_value']").val(data.data)
                        $("#edit_modal").modal('show')
                    } else {

                    }
                }
            });
        } else {
            // 编辑目录
            alert('暂不支持目录重命名！')
        }
    } else {
        alert('请选择需要编辑的项目！')
    }
}

function do_edit() {

    var server_id = $("input[name='select_server_id']").val()
    var version = $("input[name='select_version_name']").val()

    var edit_object_path = $("input[name='edit_object_path']").val()
    var edit_data = $("textarea[name='edit_value']").val()



    $.ajax({
        url: '/server/webconf/nginx/file-data-' + server_id + '.html',
        type: 'put',
        dataType: 'json',
        data: {'version': version, 'edit_object_path': edit_object_path, 'edit_data': edit_data},
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                // 文件编辑成功，刷新列表
                var e = jQuery.Event("click");
                zTreeOnClick(e, 'treeDome', get_current_tree_node())
                $("#edit_modal").modal('hide')
            } else {
                alert(data.message)
            }
        }
    });
}

function push_fn() {
    push_button('off')
    $("#version_push_modal").modal('show')
}

function push_button(switch_tag) {
    if (switch_tag == "on") {
        $("#push_loading").show();
        $("#push_btn_cancel").attr('disabled', 'disabled');
        $("#push_btn_submit").attr('disabled', 'disabled');
    } else if (switch_tag == "off") {
        $("#push_loading").hide();
        $("#push_btn_cancel").removeAttr('disabled', 'disabled');
        $("#push_btn_submit").removeAttr('disabled', 'disabled');
    }
}

function do_push() {
    var server_id = $("input[name='select_server_id']").val()
    var push_group_id = $("select[name='push_group_id']").val()
    var push_memo = $("textarea[name='push_memo']").val()

    push_button('on')

    $.ajax({
        url: '/server/webconf/nginx/file-push-' + server_id + '.html',
        type: 'post',
        dataType: 'json',
        data: {'push_group_id': push_group_id, 'push_memo': push_memo},
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                $("#version_push_modal").modal('hide')
                set_version_info(server_id)
                load_tree_data(server_id, data.data.version_name)
                push_button('off')
                document.getElementById("push_version_form").reset()
                load_version_status(data.data.version_id)
            } else {

            }
        }
    });
}

function load_version_status(version_id) {
    var server_id = $("input[name='select_server_id']").val()
    $.ajax({
        url: '/server/webconf/nginx/get_version_status.html',
        type: 'post',
        data: {'version_id': version_id, 'server_id': server_id},
        traditional:true,
        success: function (data, response, status) {
            $("#version_status_html").html(data)
        }
    });
}

