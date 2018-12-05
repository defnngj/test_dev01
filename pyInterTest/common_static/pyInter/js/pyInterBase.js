/**
 * author:anonymous
 */
//从数据库获取到的临时数据
var GlobalData = {
	"select_api_info":{},
	"select_case_info":{},
	"tree_list":[],
};
var UserInfo = {	
	"userName":"",
	"userId":"",
};
var ProjectInfo={
	"pId":"",
}

var textareaTab = (function(){
	//textarea支持tab缩进
	$("textarea").on('keydown',function(e){
	    if(e.keyCode == 9){
	        e.preventDefault();
	        var indent = '    ';
	        var start = this.selectionStart;
	        var end = this.selectionEnd;
	        var selected = window.getSelection().toString();
	        selected = indent + selected.replace(/\n/g,'\n'+indent);
	        this.value = this.value.substring(0,start) + selected + this.value.substring(end);
	        this.setSelectionRange(start+indent.length,start+selected.length);
	    }
	});
	$("input").css("color", "black");
	$("textarea").css("color", "black");
}());


var PIBase = (function () {
    var main = {};
    main.userInfo={};//用户的基本信息
    
    //csrf
    jQuery(document).ajaxSend(function(event, xhr, settings) {
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
	
	$(document).ajaxComplete(function () {			
		$("body").mLoading("hide");
	});
	$(document).ajaxError(function () {			
		$("body").mLoading("hide");
	});
	$(document).ajaxStop(function () {			
		$("body").mLoading("hide");
	});
//    $.ajaxSetup({
//        beforeSend:function (xhr,settings) {
//            xhr.setRequestHeader("X-CSRFtoken",$.cookie("csrftoken"))
//        }
//    });
    
    main.requestJson = function(url,methor,data,callback){
	   $.ajax({
		    url:url,
		    type:methor, // GET,POST
		    async:true,    // 或false,是否异步
		    data:JSON.stringify(data),
		    timeout:50000,    // 超时时间
		    contentType: "application/json; charset=utf-8",
		    dataType:'json',    // 返回的数据格式：json/xml/html/script/jsonp/text
		    beforeSend:function(xhr){
		        console.log('发送前');
		    },
		    success:function(data,textStatus,jqXHR){
		        console.log('执行成功');
		        console.log(textStatus);
		        callback(data);
		    },
		    error:function(xhr,textStatus){
		        console.log('错误');
		        console.log(xhr);
		        console.log(textStatus);
//		        Ladda.stopAll();
		    },
		    complete:function(){
		        console.log('结束');
		    }
		})
   }
   
  
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
   main.prompt = function (message, style, time)
   {
       style = (style === undefined) ? 'alert-success' : style;
       time = (time === undefined) ? 1200 : time;
       $('<div>')
           .appendTo('body')
           .addClass('alert ' + style)
           .html(message)
           .show()
           .delay(time)
           .fadeOut();
   };
   // 成功提示
   main.success_prompt = function(message, time) {
   	time = time||2000;

//	   swal("操作成功!", message, "success"); 
	   swal({   
			title: "操作成功!",   
			text: message,   
			timer: time,
			type: "success",
			showConfirmButton: true
		});
	   //PIBase.prompt(message, 'alert-success', time);
   };

   // 失败提示
   main.fail_prompt = function(message, time) {
	   time = time||5000;
	   //PIBase.prompt(message, 'alert-danger', time);
	   swal({ 
	        title: "操作失败",  
	        text: message,  
	        type: "error", 
	        showConfirmButton: true
//	        confirmButtonColor: "#ec6c62" 
	    }); 
   };

   // 提醒
   main.warning_prompt = function(message, time)
   {
	   PIBase.prompt(message, 'alert-warning', time);
   };

   // 信息提示
   main.info_prompt = function(message, time)
   {
	   PIBase.prompt(message, 'alert-info', time);
   };
   
   //文本过长设置
   main.textlength_settting = function(text, length){
   	   length = length||18;
	   if(text.length > length){
		   return (text.substr(0,length) + ".."); 
	   }else{
		   return text;
	   }
   }
   
   //textarea 自适应高度
   main.setStyle = function(id,min_height) {
   	   min_height = min_height||50;
	   var el = document.getElementById(id);
       el.style.height = 'auto';
       el.style.overflow = 'auto';
       el.style.resize = 'none';
       if(el.scrollHeight < min_height){
       	el.style.height = min_height + 'px';
       }else{
	        el.style.height = el.scrollHeight + 'px';
       }
       // console.log(el.scrollHeight);
   };
   main.textAreaAutoHeight = function(id,min_height) {
   	  min_height = min_height||50;
	  var el = document.getElementById(id);
	    var setStyle = function(el,min_height) {
	    	min_height = min_height||50;
	        el.style.height = 'auto';
	        el.style.overflow = 'auto';
	        el.style.resize = 'none';
	        if(el.scrollHeight < min_height){
	        	el.style.height = min_height + 'px';
	        }else{
		        el.style.height = el.scrollHeight + 'px';
	        }
	        // console.log(el.scrollHeight);
	    };
	    var delayedResize = function(el,min_height) {
	    	min_height = min_height||50;
	        window.setTimeout(function() {
	            setStyle(el,min_height);
	        },
	        0);
	    };
	    if (el.addEventListener) {
	        el.addEventListener('input',function() {
	            setStyle(el,min_height);
	        },false);
	        setStyle(el,min_height);
	    } else if (el.attachEvent) {
	        el.attachEvent('onpropertychange',function() {
	            setStyle(el,min_height);
	        });
	        setStyle(el,min_height);
	    }
	    if (window.VBArray && window.addEventListener) { //IE9
	        el.attachEvent("onkeydown",function() {
	            var key = window.event.keyCode;
	            if (key == 8 || key == 46) delayedResize(el);

	        });
	        el.attachEvent("oncut",function() {
	            delayedResize(el);
	        }); //处理粘贴
	    }
	};
   
	main.setScroll = function(d){
//		console.log($("body"));
		t = document.body.scrollLeft;           
		l = document.body.scrollTop;
//		w = document.documentElement.scrollWidth;           
//		h = document.documentElement.scrollHeight;  
		//console.log(t,l,w,h);
		var scrollheight = $("body")[0].scrollHeight
		$("body").animate({"scrollTop": l+"px"}, 1);
	}
	//*********
	//类型设置
	main.typeTell = function(res,key,data,type){
		if(undefined == res){
			res = {};
		}
		var d = {};
		switch(type){
	    case "string":
	    	d = String(data);
		    break;
	    case "number":
	    case "int":
	    case "float":
	    	d = Number(data);
	    	if(isNaN(d)){
	    		d=-1
	    	}
		    break;
	    case "bool":
	    case "boolean":
	    	d = true;
	    	if("false"==data||false==data){
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
		if(par.test(key)){
			n_key = key.substring(0,key.length - 2);
			if(undefined==res[n_key]){
				res[n_key] = [];
				res[n_key][0] = {};
			}
		}else{
			res[key] = d;
		}
	}
	//递归设置数据
	main.recursionSetObje = function(res,list,data,type,index){
		if(index >= list.length){
			return;
		}
		if(undefined==res){
			res = {};
		}
		var key = list[index];
		if(index == list.length -1){//如果是叶子节点，则直接设置数据
			PIBase.typeTell(res,key,data,type);
		}else{
			var par = /.+\[\]$/;
			if(par.test(key)){
				n_key = key.substring(0,key.length - 2);
				if(undefined == res[n_key]){
					res[n_key] = [];
					res[n_key][0] = {};
				}
				PIBase.recursionSetObje(res[n_key][0],list,data,type,index+1);
			}else{
				if(undefined == res[key]){
					res[key] = {};
				}
				PIBase.recursionSetObje(res[key],list,data,type,index+1);
			}
		}
	}
    main.form2json = function(data){//把form的数据转换为json数据
	    var res = {};
	    for(var i=0;i<data.length;i++){
		    var name = data[i].name;
		    var dec = data[i].dec;
		    var type = data[i].type;
		    list = name.split(".");
		    if(list.length < 2){
		    	PIBase.typeTell(res,name,dec,type)//没有子节点的处理
		    }else{
			    PIBase.recursionSetObje(res,list,dec,type,0);//存在子节点的处理
		    }
	    }
	    return res;
    };
    
    
    //以上是用来设置从form转为json
    //********
    
    //************
    //下面是设置为从json转为form
    
    main.isEmptyObject = function(obj) {
	   for (var key in obj) {
	     return false;
	   }
	   return true;
	};
    
    main.recursionObj2Array = function(res,name,origin){
    	console.log(name,origin);
    	switch(typeof(origin)){
		case "string":
	    case "number":
	    case "int":
	    case "float":
	    case "boolean":
	    	for(var i=0;i<res.length;i++){//如果存在相同的数据就略过
	    		if(name == res[i]["name"]){
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
	    	if(origin instanceof Array){
	    		if(origin.length == 0){
	    			var tmp = {};
	    	    	tmp["name"] = name;
	    	    	tmp["dec"] = "[]";
	    	    	tmp["type"] = "list";
	    	    	res.push(tmp);
	    	    	return;
	    		}else{
	    			var first = origin[0];
	    			if(PIBase.isEmptyObject(first)){
	    				var tmp = {};
    	    	    	tmp["dec"] = "[]";
    	    	    	tmp["type"] = "list";
	    				tmp["name"] = name;
	    				res.push(tmp);
	    				return;
	    			}
	    			for(var i in first){
	    				n_name = name+"[]."+i;
	    				PIBase.recursionObj2Array(res,n_name,first[i]);
	    			}
	    		}
	    	}else{
	    		if(PIBase.isEmptyObject(origin)){
	    			var tmp = {};
	    	    	tmp["name"] = name;
	    	    	tmp["dec"] = "{}";
	    	    	tmp["type"] = "object";
	    	    	res.push(tmp);
	    	    	return
	    		}else{
	    			for(var i in origin){
	    				n_name = name+"."+i;
	    				PIBase.recursionObj2Array(res,n_name,origin[i]);
	    			}
	    		}
	    	}
		}
    };
    main.json2form = function(data, aId){
    	aId = aId||-1;
    	var res=[];
    	for(var p in data){
    	    PIBase.recursionObj2Array(res,p,data[p]);
    	}
    	if(aId>0){
    		for(var i=0;i<res.length;i++){
        		res[i]["aId"] = aId;
        	}
    	}
    	return res;
    };
    
    main.IsURL = function(str){
        return !!str.match(/(((^https?:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)$/g);
    }
    
    main.make_bootstrap_tree_case_data = function(data){
    	function setNode(data,node){
    		if(ApiHandle.isEmpty(data)||ApiHandle.isEmpty(node)){
    			return false;
    		}
    		if(setJsonChild.mark){// 已经找到了父节点，直接返回
    			return true;
    		}
    		if(data.mId == node.parentId || data.aId == node.parentId){
				data.nodes.push(node);
				setJsonChild.mark=true;
				return true;
			}else{
				setJsonChild(data.nodes,node);
			}
    	}
    	function setJsonChild(data,node){
    		if(ApiHandle.isEmpty(data)||ApiHandle.isEmpty(node)){
    			return data;
    		}
    		if(setJsonChild.mark){// 已经找到了父节点，直接返回
    			return data;
    		}
 		
    		for(var i=0;i<data.length;i++){
    			re = setNode(data[i],node);
    			if(true == re){
    				break;
    			}
    		}
    	}
    	setJsonChild.mark=false;// 定义静态变量，用来标识是否已经找到了父节点
    	var tree=[];

    	for(var i=0;i<data.length;i++){
    		tmpNode={};
    		tmpNode["text"] = data[i].name;
    		tmpNode["mId"] = data[i].mId;
    		tmpNode["aId"] = data[i].aId;
    		tmpNode["parentId"] = data[i].parentId;
    		tmpNode["cId"] = data[i].cId;
    		tmpNode["pId"] = data[i].pId;
    		tmpNode["type"] = data[i].type;
    		tmpNode["method"] = data[i].method;
    		if(tmpNode["type"] == "module"){
    			tmpNode["tags"] = ['<i class="icon-folder-open"></i>'];
    		}else{
    			if("api" == tmpNode["type"]){
    				tmpNode["tags"] = ['<i class="icon-file"></i>'];
    				tmpNode["tagsClass"] = "badge badger-success";
    				
    			}else{
    				tmpNode["tags"] = ['<i class="icon-certificate"></i>'];
    				tmpNode["tagsClass"] = "badge badger-primary";
    			}
    		}
    		tmpNode["nodes"] = [];
    		if(data[i].parentId==undefined || data[i].parentId==0){
    			tree.push(tmpNode);
    		}else{
    			setJsonChild.mark=false;
    			setJsonChild(tree,tmpNode);// 递归设置数据
    		}
    	};
    	return tree;
    }
   
    main.stopBubble = function(e) {  
        var e = e ? e : window.event;  
        if (window.event) { // IE  
            e.cancelBubble = true;   
        } else { // FF  
            //e.preventDefault();   
            e.stopPropagation();   
        }   
    }
   return main;
}());

//$.fn.extend({
//	  txtaAutoHeight: function () {
//	 return this.each(function () {
//	 var $this = $(this);
//	                     if (!$this.attr('initAttrH')) {
//	                        $this.attr('initAttrH', $this.outerHeight());
//	                     }
//	                      setAutoHeight(this).on('input', function () {
//	                        setAutoHeight(this);
//	                     });
//	               });
//	                function setAutoHeight(elem) {
//	                    var $obj = $(elem);
//	                    return $obj.css({ height: $obj.attr('initAttrH'), 'overflow-y': 'hidden' }).height(elem.scrollHeight);
//	                }
//	           }
//	        });

(function($){
	$.fn.autoTextarea = function(options) {
		var defaults={
			maxHeight:null,//文本框是否自动撑高，默认：null，不自动撑高；如果自动撑高必须输入数值，该值作为文本框自动撑高的最大高度
			minHeight:$(this).height() //默认最小高度，也就是文本框最初的高度，当内容高度小于这个高度的时候，文本以这个高度显示
		};
		var opts = $.extend({},defaults,options);
		return $(this).each(function() {
			$(this).bind("paste cut keydown keyup focus blur",function(){
				var height,style=this.style;
				this.style.height =  opts.minHeight + 'px';
				if (this.scrollHeight > opts.minHeight) {
					if (opts.maxHeight && this.scrollHeight > opts.maxHeight) {
						height = opts.maxHeight;
						style.overflowY = 'scroll';
					} else {
						height = this.scrollHeight;
						style.overflowY = 'hidden';
					}
					style.height = height  + 'px';
				}
			});
		});
	};
})(jQuery);

(function($){
	$.fn.setTextareaHeight = function(options) {
		var defaults={
			maxHeight:null,//文本框是否自动撑高，默认：null，不自动撑高；如果自动撑高必须输入数值，该值作为文本框自动撑高的最大高度
			minHeight:100 //默认最小高度，也就是文本框最初的高度，当内容高度小于这个高度的时候，文本以这个高度显示
		};
		var opts = $.extend({},defaults,options);
		return $(this).each(function() {
			var height,style=this.style;
			this.style.height =  opts.minHeight + 'px';
			if (this.scrollHeight > opts.minHeight) {
				if (opts.maxHeight && this.scrollHeight > opts.maxHeight) {
					height = opts.maxHeight;
					style.overflowY = 'scroll';
				} else {
					height = this.scrollHeight;
					style.overflowY = 'hidden';
				}
				style.height = height  + 'px';
			}
		});
	};
})(jQuery);

$(document).keypress(function(e) {
   var eCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
    if (eCode == 13){
    	e.preventDefault();
        //自己写判断操作
    }
});