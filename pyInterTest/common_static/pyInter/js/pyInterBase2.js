/**
 * author:anonymous
 */
//从数据库获取到的临时数据
var GlobalData = {
    "select_api_info": {},
    "select_case_info": {},
    "tree_list": [],
};
var UserInfo = {
    "userName": "",
    "userId": "",
};
var ProjectInfo = {
    "pId": "",
}

var PIBase = (function () {
    var main = {};
    main.userInfo = {};//用户的基本信息
    //textarea支持tab缩进
    $("textarea").on('keydown', function (e) {
        if (e.keyCode == 9) {
            e.preventDefault();
            var indent = '    ';
            var start = this.selectionStart;
            var end = this.selectionEnd;
            var selected = window.getSelection().toString();
            selected = indent + selected.replace(/\n/g, '\n' + indent);
            this.value = this.value.substring(0, start) + selected + this.value.substring(end);
            this.setSelectionRange(start + indent.length, start + selected.length);
        }
    });
    $("input").css("color", "black");
    $("textarea").css("color", "black");
    //csrf
    jQuery(document).ajaxSend(function (event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });

    $(document).ajaxStart(function () {
        $("body").mLoading("show");
    });
    $(document).ajaxError(function () {
        $("body").mLoading("hide");
    });
    $(document).ajaxStop(function () {
        $("body").mLoading("hide");
    });


    $(document).keypress(function (e) {
        var eCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
        if (eCode == 13) {
            e.preventDefault();
            //自己写判断操作
        }
    });
//   

    return main;
}());


/////////////////////////////////////////

(function ($) {
    //类方法
    $.extend({
        "IsURL": function (str) {
            return !!str.match(/(((^https?:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)$/g);
        },
        "requestJson": function (url, methor, data, callback) {
            $.ajax({
                url: url,
                type: methor, // GET,POST
                async: true,    // 或false,是否异步
                data: JSON.stringify(data),
                timeout: 50000,    // 超时时间
                contentType: "application/json; charset=utf-8",
                dataType: 'json',    // 返回的数据格式：json/xml/html/script/jsonp/text
                beforeSend: function (xhr) {
//	 		        console.log('发送前');
                },
                success: function (data, textStatus, jqXHR) {
//	 		        console.log('执行成功');
//	 		        console.log(textStatus);
//	 		        console.log(callback);
                    callback(data);
                },
                error: function (xhr, textStatus) {
                    console.log('错误');
                    console.log(xhr);
                    console.log(textStatus);
                },
                complete: function () {
//	 		        console.log('结束');
                }
            });
        },
        "request_json": function (url, method, data, success, failed) {
            failed = failed || 0;
            var func = function (data) {
                if (data.success === "true" || data.success === true) {
                    success(data);
                } else {
                    if (failed !== 0) {
                        failed(data);
                    } else {
                        $.base_danger_prompt(data.message);
                    }
                }
            };
            $.ajax({
                url: url,
                type: method, // GET,POST
                async: true,    // 或false,是否异步
                data: JSON.stringify(data),
                timeout: 50000,    // 超时时间
                contentType: "application/json; charset=utf-8",
                dataType: 'json',    // 返回的数据格式：json/xml/html/script/jsonp/text
                beforeSend: function (xhr) {
//	 		        console.log('发送前');
                },
                success: function (data, textStatus, jqXHR) {
                    func(data);
                },
                error: function (xhr, textStatus) {
                    console.log('错误');
                    console.log(xhr);
                    console.log(textStatus);
                },
                complete: function () {
//	 		        console.log('结束');
                }
            });
        },
        //   上传附件到方法
        "upload": function (url, file_info, callback) {
            if (file_info == undefined) {//暂且不许要判断是否有附件
                $.fail_prompt("请首先选择文件!");
                return;
            }
            var form_data = new FormData();
//            var file_info = $('#file_upload')[0].files[0];
            form_data.append('file', file_info);
            // 提交ajax的请求
            $.ajax({
                url: url,
                type: 'POST',
                data: form_data,
                processData: false,  // tell jquery not to process the data
                contentType: false, // tell jquery not to set contentType
                success: function (data) {
                    callback(data);
                },
                error: function (xhr, textStatus) {
                    console.log('错误');
                    console.log(xhr);
                    console.log(textStatus);
                }
            }); // end ajax
        },
        /**
         * 弹出式提示框，默认1.2秒自动消失
         *
         * @param message
         *            提示信息
         * @param style
         *            提示样式，有alert-success、alert-danger、alert-warning、alert-info
         * @param time
         *            消失时间
         */
        "prompt": function (message, style, time) {
            style = (style === undefined) ? 'alert-success' : style;
            time = (time === undefined) ? 1200 : time;
            $('<div>')
                .appendTo('body')
                .addClass('alert ' + style)
                .html(message)
                .show()
                .delay(time)
                .fadeOut();
        },
        // 提醒
        "warning_prompt": function (message, time) {
            $.prompt(message, 'alert-warning', time);
        },
        // 信息提示
        "info_prompt": function (message, time) {
            $.prompt(message, 'alert-info', time);
        },
        // 信息提示
        "base_danger_prompt": function (message, time) {
            $.prompt(message, 'alert-danger', time);
        },
        // 成功提示
        "success_prompt": function (message, time) {
            time = time||2000;
            swal({
                title: "操作成功!",
                text: message,
                timer: time,
                type: "success",
                showConfirmButton: true
            });
        },
        // 失败提示
        "fail_prompt": function (message, time) {
            time = time||5000;
            swal({
                title: "操作失败",
                text: message,
                type: "error",
                showConfirmButton: true
//		        confirmButtonColor: "#ec6c62" 
            });
        },
        "about_me": function () {
            swal({
                title: "接口自动化系统 V1.0 (开源版)",
                text: "如需帮助，请联系 fnngj@126.com",
                imageUrl: "/static/img/about.png"
            });
        },
        //文本过长设置
        "textlength_settting": function (text, length) {
            length = length||18;
            if (text.length > length) {
                return (text.substr(0, length) + "..");
            } else {
                return text;
            }
        },
        //文本过长设置
        "text_prefix": function (text, length) {
            length = length || 20;
            if (text.length > length) {
                return (text.substr(0, length) + "..");
            } else {
                return text;
            }
        },
        "isEmptyObject": isEmptyObject,
        "form2json": function (data) {//把form的数据转换为json数据
            var res = {};
            for (var i = 0; i < data.length; i++) {
                var name = data[i].name;
                var dec = data[i].dec;
                var type = data[i].type;
                list = name.split(".");
                if (list.length < 2) {
                    typeTell(res, name, dec, type)//没有子节点的处理
                } else {
                    recursionSetObje(res, list, dec, type, 0);//存在子节点的处理
                }
            }
            return res;
        },
        "json2form": function (data, aId) {
            aId = aId||-1;
            var res = [];
            for (var p in data) {
                PIBase.recursionObj2Array(res, p, data[p]);
            }
            if (aId > 0) {
                for (var i = 0; i < res.length; i++) {
                    res[i]["aId"] = aId;
                }
            }
            return res;
        },
        "stopBubble": function (e) {
            var e = e ? e : window.event;
            if (window.event) { // IE
                e.cancelBubble = true;
            } else { // FF
                //e.preventDefault();
                e.stopPropagation();
            }
        },
        "toJson": function (s) {
            try {

                obj = JSON.parse(s);
                parmasDataStr = JSON.stringify(obj, null, 4);
                return parmasDataStr;
            } catch (e) {
                console.log(e);
//				$.fail_prompt("输入的数据不是json格式!!!",2000);
                return s;
            }
        },
        "text2divText": function (str) {
            var reg = new RegExp("\n", "g");
            var reg1 = new RegExp(" ", "g");
            str = str.replace(reg, "<br>");
            str = str.replace(reg1, "&nbsp;&nbsp;");
//	    	str = str.replace(reg1,"＜p＞"); 
            return str;
        },
        "divText2text": function (str) {
            var reg = new RegExp("＜br＞", "g");
            var reg1 = new RegExp("&nbsp;&nbsp;", "g");
            str = str.replace(reg, "\n");
            str = str.replace(reg1, " ");
            return str;
        },
    });
    //成员方法
    $.fn.extend({
        "autoTextarea": function (options) {
            var defaults = {
                maxHeight: null,//文本框是否自动撑高，默认：null，不自动撑高；如果自动撑高必须输入数值，该值作为文本框自动撑高的最大高度
                minHeight: $(this).height() //默认最小高度，也就是文本框最初的高度，当内容高度小于这个高度的时候，文本以这个高度显示
            };
            var opts = $.extend({}, defaults, options);
            return $(this).each(function () {
                $(this).bind("paste cut keydown keyup focus blur click change", function () {
                    var height, style = this.style;
                    this.style.height = opts.minHeight + 'px';
                    if (this.scrollHeight > opts.minHeight) {
                        if (opts.maxHeight && this.scrollHeight > opts.maxHeight) {
                            height = opts.maxHeight;
                            style.overflowY = 'scroll';
                        } else {
                            height = this.scrollHeight;
                            style.overflowY = 'hidden';
                        }
                        style.height = height + 'px';
                    }
                });
            });
        }
    });
    //*********
    //类型设置
    function typeTell(res, key, data, type) {
        if (undefined == res) {
            res = {};
        }
        var d = {};
        switch (type) {
            case "string":
                d = String(data);
                break;
            case "number":
            case "int":
            case "float":
                d = Number(data);
                if (isNaN(d)) {
                    d = -1
                }
                break;
            case "bool":
            case "boolean":
                d = true;
                if ("false" == data || false == data) {
                    d = false;
                }
                break;
            case "object":
                d = {};
                break;
            case "list":
                d = [];
                break;
        }
        var par = /.+\[\]$/;
        if (par.test(key)) {
            n_key = key.substring(0, key.length - 2);
            if (undefined == res[n_key]) {
                res[n_key] = [];
                res[n_key][0] = {};
            }
        } else {
            res[key] = d;
        }
    }

    //递归设置数据
    function recursionSetObje(res, list, data, type, index) {
        if (index >= list.length) {
            return;
        }
        if (undefined == res) {
            res = {};
        }
        var key = list[index];
        if (index == list.length - 1) {//如果是叶子节点，则直接设置数据
            typeTell(res, key, data, type);
        } else {
            var par = /.+\[\]$/;
            if (par.test(key)) {
                n_key = key.substring(0, key.length - 2);
                if (undefined == res[n_key]) {
                    res[n_key] = [];
                    res[n_key][0] = {};
                }
                recursionSetObje(res[n_key][0], list, data, type, index + 1);
            } else {
                if (undefined == res[key]) {
                    res[key] = {};
                }
                recursionSetObje(res[key], list, data, type, index + 1);
            }
        }
    }

    function recursionObj2Array(res, name, origin) {
//    	console.log(name,origin);
        switch (typeof(origin)) {
            case "string":
            case "number":
            case "int":
            case "float":
            case "boolean":
                for (var i = 0; i < res.length; i++) {//如果存在相同的数据就略过
                    if (name == res[i]["name"]) {
                        return;
                    }
                }
                var tmp = {};
                tmp["name"] = name;
                tmp["dec"] = origin;
                tmp["type"] = typeof(origin);
                res.push(tmp);
                return;
            case "object":
                if (origin instanceof Array) {
                    if (origin.length == 0) {
                        var tmp = {};
                        tmp["name"] = name;
                        tmp["dec"] = "[]";
                        tmp["type"] = "list";
                        res.push(tmp);
                        return;
                    } else {
                        var first = origin[0];
                        if (isEmptyObject(first)) {
                            var tmp = {};
                            tmp["dec"] = "[]";
                            tmp["type"] = "list";
                            tmp["name"] = name;
                            res.push(tmp);
                            return;
                        }
                        for (var i in first) {
                            n_name = name + "[]." + i;
                            recursionObj2Array(res, n_name, first[i]);
                        }
                    }
                } else {
                    if (isEmptyObject(origin)) {
                        var tmp = {};
                        tmp["name"] = name;
                        tmp["dec"] = "{}";
                        tmp["type"] = "object";
                        res.push(tmp);
                        return;
                    } else {
                        for (var i in origin) {
                            n_name = name + "." + i;
                            recursionObj2Array(res, n_name, origin[i]);
                        }
                    }
                }
        }
    }

    function isEmptyObject(obj) {
        for (var key in obj) {
            return false;
        }
        return true;
    }
})(window.jQuery);


