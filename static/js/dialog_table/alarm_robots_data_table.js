$(function () {
    var uTable = $('#robot_alarms_last_8_hour').DataTable({
        "bLengthChange": false,
        "language": {
            "sEmptyTable":     "No data available in table",
            "sInfo":           "Showing _START_ to _END_ of _TOTAL_ entries",
            "sInfoEmpty":      "Showing 0 to 0 of 0 entries",
            "sInfoFiltered":   "(filtered from _MAX_ total entries)",
            "sInfoPostFix":    "",
            "sInfoThousands":  ",",
            "sLengthMenu":     "Show _MENU_ entries",
            "sLoadingRecords": "Loading...",
            "sProcessing":     "Processing...",
            "sSearch":         "Search:",
            "sZeroRecords":    "No matching records found",
            "oPaginate": {
                "sFirst":    "First",
                "sLast":     "Last",
                "sNext":     "Next",
                "sPrevious": "Previous"
            },
            "oAria": {
                "sSortAscending":  ": activate to sort column ascending",
                "sSortDescending": ": activate to sort column descending"
            }
        },
        "bInfo": false,
        "bAutoWidth": false,
        "processing": true,
        'ajax':{
            'url': '/api/alarm/robot/',
            'type':'GET',
            'data':function(){
            }
        },
        'dom':'tp',
        'iDisplayLength':10,
        'responsive': true,
    });
});
