/**
 * author:anonymous
 */
"use strict";

var get_user_validate = function () {
    $('#form_user_reset_pwd').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            input_user_name: {
                validators: {
                    notEmpty: {
                        message: '用户名不能为空'
                    }
                }
            },
            input_user_old_pwd: {
                validators: {
                    notEmpty: {
                        message: '旧密码不能为空'
                    }
                }
            },
            input_user_new_pwd: {
                validators: {
                    notEmpty: {
                        message: '新密码不能为空'
                    }
                }
            }
        }
    });
    var bootstrapValidator = $("#form_user_reset_pwd").data('bootstrapValidator');
    return bootstrapValidator;
};

var user_setting = function () {

    $("#bt_reset_pwd").on("click", function () {
        $("#div_user_message_boards").hide();
        var bootstrapValidator = get_user_validate();
        //手动触发验证
        bootstrapValidator.validate();
        if (bootstrapValidator.isValid()) {
            var name = $("#input_user_name").val();
            var user_id_str = $("#input_user_name").attr("user_id");
            var user_id = Number(user_id_str);

            var old_pwd = $("#input_user_old_pwd").val();
            var new_pwd = $("#input_user_new_pwd").val();
            var data = {};
            data["user_id"] = user_id;
            data["old_pwd"] = old_pwd;
            data["new_pwd"] = new_pwd;
            data["name"] = name;

            $.request_json("/reset_pwd", "POST", data, function (data) {
                swal({
                        title: "修改成功！",
                        type: "success",
                        showConfirmButton: true,
                        showCancelButton: true,
                        confirmButtonText: "重新修改",
                        cancelButtonText: "返回首页",
                        closeOnConfirm: true
                    },
                    function (isConfirm) {
                        if (!isConfirm) {
                            window.location.href = "/";
                        }
                    });
            }, function (data) {
                $("#user_message").html(data.message);
                $("#div_user_message_boards").show();
                $(".alert").alert();
            });
        }
    });
};

var UserHandle = (function () {
    var main = {};
    user_setting();
    return main;
}());



