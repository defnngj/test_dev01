/**
 * authur cch
 */
"use strict"

var add_project_validater = function () {
//  modal表单验证定义
    $('#modal_form').bootstrapValidator({
        message: '参数不能正确！',
        feedbackIcons: {
            /* 　valid: 'glyphicon glyphicon-ok',
             　　　　　　　　invalid: 'glyphicon glyphicon-remove', */
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            text_project_name: {
                validators: {
                    notEmpty: {
                        message: '项目名不能为空'
                    }
                }
            },
            text_project_dec: {
                validators: {
                    notEmpty: {
                        message: '描述不能为空'
                    }
                }
            }
        }
    });
    return $("#modal_form").data('bootstrapValidator');
};

var AddProjectSetting = (function () {
    //点击新建项目
    $("#bt_open_add_project_modal").click(function () {
        $("#modal_title").html("新建项目");
        $("#bt_update_project").hide();
        $("#bt_create_project").show();
        $("#myModal").modal('toggle');
    });
    //点击创建项目
    $("#bt_create_project").on("click", function () {
        //获取表单对象
        var bootstrap_validator = add_project_validater();
        //手动触发验证
        bootstrap_validator.validate();
        if (bootstrap_validator.isValid()) {
            var callback = function (data) {
                $("#myModal").modal('toggle');
                ProjectHandle.filer_project("all_projects");
            };
            var date = {};
            date["name"] = $("#text_project_name").val();
            date["dec"] = $("#text_project_dec").val();
            date["user_id"] = ProjectHandle.userInfo["user_id"];
            $.request_json("/project/add", "POST", date, callback);
        }
    });
});

var EditProjectSetting = (function () {
    //点击编辑项目
    $("#bt_update_project").on("click", function () {
        //获取表单对象
        var bootstrap_validator = add_project_validater();
        //手动触发验证
        bootstrap_validator.validate();
        if (bootstrap_validator.isValid()) {
            //表单提交的方法、创建项目
            var callback = function (data) {
                $("#myModal").modal('toggle');
                ProjectHandle.filer_project("all_projects");
            };
            var date = {};
            date["name"] = $("#text_project_name").val();
            date["dec"] = $("#text_project_dec").val();
            date["project_id"] = ProjectHandle.projectList[ProjectHandle.current_Index]["project_id"];
            $.request_json("/project/update", "POST", date, callback);
        }
    });
});

var ListEventSetting = (function () {
    //项目列表点击事件
    $("#get_all_projects").on("click", function () {
        ProjectHandle.filer_project("all_projects");
    });
    $("#get_my_projects").on("click", function () {
        ProjectHandle.filer_project("my_projects");
    });
    $("#get_other_projects").on("click", function () {
        ProjectHandle.filer_project("other_projects");
    });
    $("#get_running_projects").on("click", function () {
        ProjectHandle.filer_project("running_projects");
    });
    $("#get_ready_projects").on("click", function () {
        ProjectHandle.filer_project("ready_projects");
    });
    $("#get_close_projects").on("click", function () {
        ProjectHandle.filer_project("close_projects");
    });
    $("#get_normal_projects").on("click", function () {
        ProjectHandle.filer_project("normal_projects");
    });
});

var ItemsAddEventSetting = (function () {
    //给编辑项目添加事件
    $(".table_edit_botton").on("click", function () {
        $("#modal_title").html("编辑项目");
        $("#bt_update_project").show();
        $("#bt_create_project").hide();
        $("#myModal").modal('toggle');
        ProjectHandle.current_Index = $(this).attr("index");
        $("#text_project_name").val(ProjectHandle.projectList[ProjectHandle.current_Index]["name"]);
        $("#text_project_dec").val(ProjectHandle.projectList[ProjectHandle.current_Index]["dec"]);
    });
    //给关闭项目添加事件
    $('.table_delete_botton').on('click', function () {

        ProjectHandle.current_Index = $(this).attr("index");
        var status = ProjectHandle.projectList[ProjectHandle.current_Index]["status"];
        if (status === -1) {
            swal({
                title: "您确定要打开项目吗？",
                text: "您确定要重新打开这个项目吗？",
                type: "warning",
                showCancelButton: true,
                closeOnConfirm: true,
                confirmButtonText: "是的，我要打开",
                confirmButtonColor: "#ec6c62"
            }, function () {
                var callback = function (data) {
                    ProjectHandle.filer_project("all_projects");
                };
                var project_id = ProjectHandle.projectList[ProjectHandle.current_Index]["project_id"];
                $.request_json("/project/close", "POST", {"project_id": project_id, "status": 0}, callback);
            });
        } else {
            swal({
                title: "您确定要关闭项目吗？",
                text: "您确定要关闭这个项目吗？",
                type: "warning",
                showCancelButton: true,
                closeOnConfirm: true,
                confirmButtonText: "是的，我要关闭",
                confirmButtonColor: "#ec6c62"
            }, function () {
                var callback = function (data) {
                    ProjectHandle.filer_project("all_projects");
                };
                var project_id = ProjectHandle.projectList[ProjectHandle.current_Index]["project_id"];
                $.request_json("/project/close", "POST", {"project_id": project_id, "status": -1}, callback);

            });
        }

    });

});

var ProjectHandle = (function () {
    var main = {};
    main.userInfo = PIBase.userInfo;//用户的基本信息
    main.projectList = [];//项目列表
    main.current_Index = -1;

    main.make_table_tr = function (data, i) {
        var tmp = [];
        var name = $.text_prefix(data["name"], 20);

        if (0 === data["status"] || 1 === data["status"]) {
            tmp.push("<a href='/project/" + data["project_id"] + "'>" + name + "</a>");
        } else {
            tmp.push("<other>" + name + "</other>");
        }
        tmp.push($.text_prefix(data["dec"], 25));
        tmp.push(data["user_name"]);
        tmp.push(data["task_counts"]);
        tmp.push(data["inter_counts"]);
        switch (data["status"]) {
            case 0:
                tmp.push("正常");
                break;
            case 1:
                tmp.push("有任务");
                break;
            case -1:
                tmp.push("已关闭");
                break;
            default:
                tmp.push("未知状态");
        }
        tmp.push(data["create_time"]);
        var ope_str = '<a class="table_edit_botton" index=' + i + '><i class="icon-edit"></i></a>&nbsp;&nbsp;<a  class="table_delete_botton"  index=' + i + '><i class="icon-archive"></i></a>';
        tmp.push(ope_str);
        return tmp;
    };
//    刷新表格
    main.flesh_table_data = function (list) {
        ProjectHandle.projectList = list;
        var table = $("#sample_1").dataTable();
        var oSettings = table.fnSettings();
        table.fnClearTable(this);

        var ret = [];
        for (var i = 0; i < list.length; i++) {
            var t = ProjectHandle.make_table_tr(list[i], i);
            ret.push(t);
        }
        for (i = 0; i < ret.length; i++) {
            table.oApi._fnAddData(oSettings, ret[i]);
        }
        oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
        table.fnDraw();
        ItemsAddEventSetting();
    };

    //请求获取项目数据
    main.filer_project = function (model) {
        var callback = function (data) {
            ProjectHandle.flesh_table_data(data.data.data);
        };
        switch (model) {
            case "all_projects":
                $.request_json("/project/lists", "POST", {}, callback);
                break;
            case "my_projects":
                $.request_json("/project/lists", "POST", {"user_id": ProjectHandle.userInfo["user_id"]}, callback);
                break;
            case "other_projects":
                $.request_json("/project/lists", "POST", {
                    "user_id": ProjectHandle.userInfo["user_id"],
                    "exclude": "true"
                }, callback);
                break;
            case "running_projects":
                $.request_json("/project/lists", "POST", {"status": 1}, callback);
                break;
            case "ready_projects":
                $.request_json("/project/lists", "POST", {"status": 0}, callback);
                break;
            case "close_projects":
                $.request_json("/project/lists", "POST", {"status": -1}, callback);
                break;
            case "normal_projects":
                $.request_json("/project/lists", "POST", {"status": -1, "exclude": "true"}, callback);
                break;
        }
    };
    AddProjectSetting();
    EditProjectSetting();
    ListEventSetting();
    return main;
}());
ProjectHandle.filer_project("all_projects");
