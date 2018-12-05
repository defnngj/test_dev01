var Script = function () {

        // begin first table
        $('#sample_1').dataTable({
            // "sDom": "<'row'<'col-sm-6'l><'col-sm-6'f>r>t<'row'<'col-sm-6'i><'col-sm-6'p>>",
            "sDom": "t<'row'<'col-sm-6'i><'col-sm-6'p>>",
            // "dom": '<"top"i>rt<"bottom"flp><"clear">',
            "sPaginationType": "bootstrap",
            "bProcessing": false,
            "oLanguage": {
            	"sLengthMenu": "每页显示 _MENU_ 条记录",
                "sZeroRecords": "对不起，查询不到任何相关数据",
                "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
                "sInfoEmtpy": "找不到相关数据",
                "sInfoFiltered": "数据表中共为 _MAX_ 条记录)",
                "sProcessing": "正在加载中...",
                "oPaginate": {
                    "sPrevious": "上一页",
                    "sNext": "下一页"
                }
            },
            "aaSorting": [[ 5, 'desc' ],[ 6, 'desc' ]],
            "aoColumnDefs": [{
                'bSortable': false,
                'aTargets': [0]
            }]
        });
        jQuery('#sample_1_wrapper .dataTables_filter input').addClass("form-control"); // modify table search input
        jQuery('#sample_1_wrapper .dataTables_length select').addClass("form-control"); // modify table per page dropdown
//        jQuery('#sample_1 .group-checkable').change(function () {
//            var set = jQuery(this).attr("data-set");
//            var checked = jQuery(this).is(":checked");
//            jQuery(set).each(function () {
//                if (checked) {
////                    $(this).attr("checked", true);
//                    $(this).prop("checked", true);
//                } else {
//                	$(this).prop("checked", false);
////                    $(this).attr("checked", false);
//                }
//            });
//            jQuery.uniform.update(set);
//        });
//
        

        // begin second table
        $('#sample_2').dataTable({
            "sDom": "<'row'<'col-sm-6'l><'col-sm-6'f>r>t<'row'<'col-sm-6'i><'col-sm-6'p>>",
            "sPaginationType": "bootstrap",
            "oLanguage": {
            	"sLengthMenu": "每页显示 _MENU_ 条记录",
                "sZeroRecords": "对不起，查询不到任何相关数据",
                "sInfo": "当前显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
                "sInfoEmtpy": "找不到相关数据",
                "sInfoFiltered": "数据表中共为 _MAX_ 条记录)",
                "sProcessing": "正在加载中...",
                "oPaginate": {
                    "sPrevious": "上一页",
                    "sNext": "下一页"
                }
            },
            "aoColumnDefs": [{
                'bSortable': false,
                'aTargets': [0]
            }]
        });

        jQuery('#sample_2 .group-checkable').change(function () {
            var set = jQuery(this).attr("data-set");
            var checked = jQuery(this).is(":checked");
            jQuery(set).each(function () {
                if (checked) {
                    $(this).attr("checked", true);
                } else {
                    $(this).attr("checked", false);
                }
            });
            jQuery.uniform.update(set);
        });

        jQuery('#sample_2_wrapper .dataTables_filter input').addClass("form-control"); // modify table search input
        jQuery('#sample_2_wrapper .dataTables_length select').addClass("form-control"); // modify table per page dropdown

        // begin: third table
        $('#sample_3').dataTable({
            "sDom": "<'row'<'col-sm-6'l><'col-sm-6'f>r>t<'row'<'col-sm-6'i><'col-sm-6'p>>",
            "sPaginationType": "bootstrap",
            "oLanguage": {
                "sLengthMenu": "_MENU_ per page",
                "oPaginate": {
                    "sPrevious": "Prev",
                    "sNext": "Next"
                }
            },
            "aoColumnDefs": [{
                'bSortable': false,
                'aTargets': [0]
            }]
        });

        jQuery('#sample_3 .group-checkable').change(function () {
            var set = jQuery(this).attr("data-set");
            var checked = jQuery(this).is(":checked");
            jQuery(set).each(function () {
                if (checked) {
                    $(this).attr("checked", true);
                } else {
                    $(this).attr("checked", false);
                }
            });
            jQuery.uniform.update(set);
        });

        jQuery('#sample_3_wrapper .dataTables_filter input').addClass("form-control"); // modify table search input
        jQuery('#sample_3_wrapper .dataTables_length select').addClass("form-control"); // modify table per page dropdown
}();