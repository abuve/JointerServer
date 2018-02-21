function load_tree_data() {

    var setting = {
        data: {
            simpleData: {
                enable: true
            }
        }
    };

    $.ajax({
        url: '/cmdb/business-json.html?from=cmdb_asset_create',
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

function select_business_node(node_data, business_id) {
    if (business_id) {
        $('input[name="business_unit_id"]').val(business_id)
        close_business_tree()
        $("#business_select_text").html(node_data.title)
    }
}

$(".model-group-list").click(function (e) {
    e.preventDefault();
    e.stopPropagation();
    return false;
});

function close_business_tree() {
    $("#business_tree_btn").removeClass("open");
}

function checkIP(value) {
    var exp=/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
    var reg = value.match(exp);
    if(reg) {
        return true;
    }
}

function isInteger(obj) {
 return obj%1 === 0
}

function cmdb_asset_create_fn() {
    var device_type_id = $('select[name="device_type_id"]').val()
    var idc_id = $('select[name="idc_id"]').val()
    var business_unit_id = $('input[name="business_unit_id"]').val()
    var hostname = $('input[name="hostname"]').val()
    var ipaddress = $('input[name="ipaddress"]').val()
    var manage_ip = $('input[name="manage_ip"]').val()
    var cpu_count = $('input[name="cpu_count"]').val()
    var Memory = $('input[name="Memory"]').val()
    var DeviceSize = $('input[name="DeviceSize"]').val()

    // Business 验证
    if (! business_unit_id) {
        alert("Please select Business Unit.")
        return false
    }

    // IP 验证
    if (! ipaddress) {
        alert("Please enter IP Address.")
        return false
    }

    if (! checkIP(ipaddress)) {
        alert("Wrong IP address, Please check value.")
        return false
    }

    // 管理地址IP验证
    if (manage_ip) {
        if (! checkIP(manage_ip)) {
            alert("Wrong Manage IP address, Please check value.")
            return false
        }
    }

    // CPU 验证
    if (cpu_count) {
        if (! isInteger(cpu_count)) {
            alert("Error CPU Count, Please check value.")
            return false
        }
    }

    // Memory 验证
    if (Memory) {
        if (! isInteger(Memory)) {
            alert("Error Memory Size, Please check value.")
            return false
        }
    }

    //Disk 验证
    if (DeviceSize) {
        if (! isInteger(DeviceSize)) {
            alert("Error Device Size, Please check value.")
            return false
        }
    }

    $.ajax({
        url: '/cmdb/server-json.html',
        type: 'post',
        dataType: 'json',
        traditional:true,
        data : {
            "device_type_id": device_type_id,
            "idc_id": idc_id,
            "business_unit_id": business_unit_id,
            "hostname": hostname,
            "ipaddress": ipaddress,
            "manage_ip": manage_ip,
            "cpu_count": cpu_count,
            "Memory": Memory,
            "DeviceSize": DeviceSize,
        },
        success: function (data, response, status) {
            if (data.status) {
                window.location.href='/cmdb/server-list.html'
            } else {
                alert(data.message)
            }
        }
    });

}