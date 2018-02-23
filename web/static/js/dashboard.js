/**
 * Created by aaron on 2018/2/22.
 */

function show_chart_count(data_preset, data_obj) {
    var dom = document.getElementById(data_preset.dom_id);
    var chart = echarts.init(dom);
    option = null;
    option = {
        title : {
            text: data_preset.title,
            subtext: data_preset.subtext,
            x:'center'
        },
        tooltip : {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: data_obj.name_list
        },
        series : [
            {
                name: '数据统计',
                type: 'pie',
                radius : '55%',
                center: ['50%', '60%'],
                data: data_obj.value_list,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    if (option && typeof option === "object") {
        chart.setOption(option, true);
    }
}

function show_business_bar(data_obj) {
    var app = {};

    option3 = {
        tooltip : {
            trigger: 'axis',
            axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: data_obj.asset_type_list
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis:  {
            type: 'category',
            data: data_obj.business_list
        },
        yAxis: {
            type: 'value'
        },
        series: data_obj.data_count
    };

    var dom3 = document.getElementById("business_count_container");
    var myChart3 = echarts.init(dom3);
    myChart3.setOption(option3, true);
}

$(function () {

    var asset_count_preset = {'title': 'CMDB资源类型统计', 'subtext': '分类数据', 'dom_id': 'asset_count_container'}
    var idc_count_preset = {'title': 'IDC资源数据统计', 'subtext': '机房数据', 'dom_id': 'idc_count_container'}

    $.ajax({
        url: '/dashboard_chart_ajax/',
        type: 'get',
        dataType: 'json',
        traditional:true,
        success: function (data, response, status) {
            if (data.status) {
                show_chart_count(asset_count_preset, data.asset_count)
                show_chart_count(idc_count_preset, data.idc_count)
                show_business_bar(data.business_count)
            }
        }
    });

});