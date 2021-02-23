function getDateRange() {
    var startDatetime = $('#datetimerange').data('daterangepicker').startDate;
    var endDatetime = $('#datetimerange').data('daterangepicker').endDate;

    return {
        'start': startDatetime.format('DD.MM.YYYY'),
        'end': endDatetime.format('DD.MM.YYYY'),
        'start_time': startDatetime.format('HH:mm'),
        'end_time': endDatetime.format('HH:mm')
    };
}

function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    var dateRange = getDateRange();

    indexed_array['start'] = dateRange['start'];
    indexed_array['end'] = dateRange['end'];
    indexed_array['start_time'] = dateRange['start_time'];
    indexed_array['end_time'] = dateRange['end_time'];

    return indexed_array;
}


function buildSearchData(){

    var filters = getFormData($("#fm_vends_filter"));
    var data = {
        "filters": JSON.stringify({
            "machine_type": filters['machine_type'],
            "product":"0",
            "product_caption": filters['product'],
            "payment":filters['payment'],
            "machines": filters['machines'],
            "region": filters['region'],
            "start": filters['start'],
            "end": filters['end'],
            "start_time": filters['start_time'],
            "end_time": filters['end_time'],
            "tax_rate_type": filters['tax_rate_type'],
            "search_data": $('#custom_table_search').val(),
            "machine_mode":filters['machine_mode']
        })
    };
    return data
}

$(function() {

    (function setDefaultMachineMode () {
        var mode = 'all';
            mode = 'live';
            mode = '{{ current_machine_mode }}';
        $('#machine_mode').val(mode);
    })();

    function endOfDay (momentObj) {
        return momentObj.add(1, 'days')
    }

    function shiftToday (shift) {
        var today = moment().hour(0).minutes(0);

        shift = parseInt(shift);

        if (shift === NaN)
            return today;

        return today.add(shift, 'days');
    }

    function shiftMonth () {
        var to_day = moment().hour(0).minutes(0);
        to_day = to_day.add(-1, 'months');
        to_day = to_day.add(1, 'days')
        return to_day;
    }
    // --------------------BEGIN----------------
    var datePickerDateLimit = window.location.hostname.toLocaleLowerCase().indexOf('ecta-03') >= 0 ? 2 : 31;
    var datePickerRanges = {
        "Today": [
            shiftToday(),
            endOfDay(shiftToday())
        ],
        "Yesterday": [
            shiftToday(-1),
            endOfDay(shiftToday(-1))
        ]
    };
    if (datePickerDateLimit > 3) {
        datePickerRanges["Last 7 Days"] = [
            shiftToday(-6),
            endOfDay(shiftToday())
        ];
        datePickerRanges["Last Month"] = [
            shiftMonth(),
            endOfDay(shiftToday())
        ];
    };
    // --------------------END----------------

    $('#datetimerange').daterangepicker({
        "locale": {
            "format": 'DD.MM.YYYY HH:mm'
        },
        "timePicker": true,
        "timePicker24Hour": true,
        "dateLimit": {
            "days": datePickerDateLimit
        },
        "maxDate": endOfDay(shiftToday()),
        "ranges": datePickerRanges,
        "startDate": shiftToday(),
        "endDate": endOfDay(shiftToday())
    });


    if(0 == 0){
        var columns = [
            {"data":"date"},
            {"data":"machine_caption"},
            {
                "data":"product",
                "render": function(product){
                    if (product['is_unknown'])
                        return '<i class="txt_alizarin">' + product['caption'] + '</i>';
                    else return product['caption'];
                }
            },
            {"data":"payment_type"},
            {"data":"column"},
            {"data":"quantity"},
                {"data":"value"}
        ]
    }
    else{
        var columns = [
            {"data":"date"},
            {
                "data":"product",
                "render": function(product){
                    if (product['is_unknown'])
                        return '<i class="txt_alizarin">' + product['caption'] + '</i>';
                    else return product['caption'];
                }
            },
            {"data":"payment_type"},
            {"data":"column"},
            {"data":"quantity"},
                {"data":"value"}
        ]
    }

    cTable = $("#vends_list_datatable").on('preXhr.dt', function(e,settings,data){
        data.filters = buildSearchData();
    }).DataTable({
        "bFilter" : false,
        "language": {
            "sEmptyTable":     "{% trans %}No data available in table{% endtrans %}",
            "sInfo":           "{% trans %}Showing _START_ to _END_ of _TOTAL_ entries{% endtrans %}",
            "sInfoEmpty":      "{% trans %}Showing 0 to 0 of 0 entries{% endtrans %}",
            "sInfoFiltered":   "{% trans %}(filtered from _MAX_ total entries){% endtrans %}",
            "sInfoPostFix":    "",
            "sInfoThousands":  ",",
            "sLengthMenu":     "{% trans %}Show _MENU_ entries{% endtrans %}",
            "sLoadingRecords": "{% trans %}Loading...{% endtrans %}",
            "sProcessing":     "{% trans %}Processing{% endtrans %}...",
            "sSearch":         "{% trans %}Search{% endtrans %}:",
            "sZeroRecords":    "{% trans %}No matching records found{% endtrans %}",
            "oPaginate": {
                "sFirst":    "{% trans %}First{% endtrans %}",
                "sLast":     "{% trans %}Last{% endtrans %}",
                "sNext":     "{% trans %}Next{% endtrans %}",
                "sPrevious": "{% trans %}Previous{% endtrans %}"
            },
            "oAria": {
                "sSortAscending":  ": {% trans %}activate to sort column ascending{% endtrans %}",
                "sSortDescending": ": {% trans %}activate to sort column descending{% endtrans %}"
            }
        },
        "bLengthChange": false,
        "bInfo": false,
        "bAutoWidth": false,
        "processing": true,
        "serverSide": true,

        "ajax":{
            "url":"{{ request.ROOT_URL }}/report/service/vends_list_ajax/",
            "type":"POST",
            "dataType":"json",
            "data":{
                "id": "{{ machine_detail_id }}"
            }
        },

        "columns": columns,
        "order":[[0, "desc"]]
    });

    cTable.on('xhr.dt', function(e, settings, json){
        $("#sales_info_vends").text(json['sales']);
        $("#quantity_info_vends").text(json['quantity']);

    })
});

$("#vends_list select").on('change', function(){
    cTable.ajax.reload();
});

$('#datetimerange').on('apply.daterangepicker', function(ev, picker) {
    cTable.ajax.reload();
});

$("#download_btn").on('click', function(){
    var report_type =  $("#report_type").val();
    $("#download_type").val(report_type);

    var dateRange = getDateRange();
    $('#datetimerange_start').val(dateRange['start']);
    $('#datetimerange_end').val(dateRange['end']);
    $('#datetimerange_start_time').val(dateRange['start_time']);
    $('#datetimerange_end_time').val(dateRange['end_time']);

    var button = $("#download_btn");
    var form = $("#fm_vends_filter");
    var url = form.attr("action");

    Utils.requestThrottled(url, button, function() {
        form.submit();
    });
});

$('input#custom_table_search').on('change',function(){
    cTable.ajax.reload();
    $('#search_data_filter_hidden').val($("#custom_table_search").val());
})

