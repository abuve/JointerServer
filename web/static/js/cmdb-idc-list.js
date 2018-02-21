/**
 * Created by aaron on 2017/9/11.
 */


function delete_idc_data_fn(idc_id) {
    $("#delete_data_html_area").html("Confirm remove Idc? All the data will be delete!");
    $("#delete_idc_app_fn").attr("onclick", "delete_idc_app_fn('delete', " + idc_id + ")");
    $("#delete_app_modal").modal('show')
}

function update_idc_app_fn(update_type, idc_id) {

    var idc_name = $('input[name="idc_name"]').val();
    var idc_floor = $('input[name="idc_floor"]').val();
    var idc_phone = $('input[name="idc_phone"]').val();
    var idc_address = $('input[name="idc_address"]').val();

    $.ajax({
        url: '/cmdb/idcs.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'idc_id': idc_id, 'idc_name': idc_name, 'idc_floor': idc_floor, 'idc_phone': idc_phone, 'idc_address': idc_address},
        success: function (data, response, status) {
            window.location.href = "/cmdb/idc-list.html"
        }
    });
}

function delete_idc_app_fn(update_type, idc_id) {

    $.ajax({
        url: '/cmdb/idcs.html',
        type: update_type,
        dataType: 'json',
        traditional:true,
        data: {'idc_id': idc_id},
        success: function (data, response, status) {
            $("#delete_app_modal").modal('hide');
            $('#do_refresh').trigger("click");
        }
    });
}

