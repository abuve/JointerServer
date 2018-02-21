(function (jq) {

    function approvedData() {

        $.ajax({
            url: "/cmdb/approval-json.html",
            type: 'PUT',
            data: {"id_list": id_list},
            traditional: true,
            success: function (response) {
                console.log(response)
                if (response.status) {
                    SuccessHandleStatus(response.message);
                    $('#do_refresh').trigger("click");
                } else {
                    ErrorHandleStatus(response.message, response.error);
                }
                $("#approved_data_modal").modal('hide');

            },
            error: function () {
                $.Hide('#shade,#modal_delete');
                alert('请求异常');
            }
        })
    }

    function select_check() {
        id_list = [];
        $('#table_body').find(':checkbox').each(function () {
            if ($(this).prop('checked')) {
                id_list.push($(this).val());
            }
        });
        if (id_list.length == 0) {
            alert("please select rows.");
            return false;
        } else {
            return true;
        }
    }

    /*
     绑定头部按钮事件
     */
    function bindMenuFunction() {

        $('#do_approved').click(function () {
            if (select_check()) {
                $("#approved_data_modal").modal('show');
            }
        });

        $('#do_approved_confirm').click(function () {
            approvedData();
        });


    }

    bindMenuFunction();

})(jQuery);