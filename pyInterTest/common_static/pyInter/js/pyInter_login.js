/**
 * author:anonymous
 */
"use strict";

var validator = function () {
    $('#form_login').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            /* 　valid: 'glyphicon glyphicon-ok',
             　　　　　　　　invalid: 'glyphicon glyphicon-remove', */
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            user: {
                validators: {
                    notEmpty: {
                        message: '用户名不能为空'
                    }
                }
            },
            pwd: {
                validators: {
                    notEmpty: {
                        message: '密码不能为空'
                    }
                }
            }
        }
    });
    var bootstrapValidator = $("#form_login").data('bootstrapValidator');
    return bootstrapValidator;
};

var LoginSetting = function () {
    $("#bt_login").on("click", function () {
        LoginHandle.login_make_request("/login");
    });
    $("#a_register").on('click', function () {
        LoginHandle.login_make_request("/register");
    });
};

var LoginHandle = (function () {
    var main = {};
    main.login_make_request = function (url) {
        var bootstrapValidator = validator();
        bootstrapValidator.validate();
        if (bootstrapValidator.isValid()) {
            $.request_json(url, "post", {
                "user": $("#input_user_name").val(),
                "pwd": $("#input_user_pwd").val()
            }, function (data) {
                $("#message").html(data.message);
                $("#div_message_boards").hide();
                $.cookie(data.data.token_name, data.data.token, {expires: Number(data.data.token_expird), path: '/'});
                window.location.href = "/index";
            }, function (data) {
                $("#message").html(data.message);
                $("#div_message_boards").show();
            });
        }
    };
    LoginSetting();
    return main;
}());



