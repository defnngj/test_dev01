/**
 * author:anonymous
 */
var ApiDebugTmp={
		"method":"get",
		"height_running1" : false,
		"height_running2" : false
};
var divHeight= (function () {
	
	var observer1 = new MutationObserver(function (mutations, observer) {
		//$("#section_debug_parmas").css("height","auto");
		var h1 = $("#section_debug_parmas")[0].clientHeight;
		$("#section_debug_response").css("min-height",h1);
		  
	});
	var observer2 = new MutationObserver(function (mutations, observer) {
		//$("#section_debug_response").css("height","auto");
		var h1 = $("#section_debug_response")[0].clientHeight;
		  //$("#section_debug_response").height(h1);
		$("#section_debug_parmas").css("min-height",h1);
	});


	var parmas = document.querySelector('#section_debug_parmas');
	var response = document.querySelector('#section_debug_response');
	var  options = {
		attributes: true,
		characterData: true,
		childList: true,
		subtree: true,
		attributeOldValue: true,
		characterDataOldValue: true
	};
	observer1.observe(parmas, options);
	//observer2.observe(response, options);
}());


var DebugResultSetting = function(){
	$('.li_debug_response').on('show.bs.tab', function (e) {//标签显示的时候，在执行一次调整
//		  e.target // 激活的标签页
//		  e.relatedTarget // 前一个激活的标签页
		//console.log(1);
//		PIBase.setStyle('textarea_debug_response_json',410);
//	    PIBase.setStyle('textarea_debug_response_text',410);
//	    PIBase.setStyle('textarea_debug_response_header',410);
//	    PIBase.setStyle('textarea_debug_response_request',410);
		$("#textarea_debug_response_json").autoTextarea();
		$("#textarea_debug_response_text").autoTextarea();
		$("#textarea_debug_response_header").autoTextarea();
		$("#textarea_debug_response_request").autoTextarea();
	});
}

var DebugRadioSetting = function(){
	$(".radio_type").change(function(){
		var checkedvalue = $("input[name='debug_parmas']:checked").val();
		if("json"==checkedvalue){
			$("#div_debug_parmas_json").show();
			$("#div_debug_parmas_form").hide();
		}else{
			$("#div_debug_parmas_json").hide();
			$("#div_debug_parmas_form").show();
		}
	});
}

var DebugDataSetting = function(){
	$("#bt_debug_add_parmas").on('click',function(){
		var tbody=$(this).prev().find("tbody");
		var tr = '<tr> \
			        <td width="35%"><input type="text" class="form-control" id="input_debug_parmas_name" style="color:black" name=""></td> \
					<td width="60%"><input type="text" class="form-control" id="input_debug_parmas_value" style="color:black"  name=""></td> \
					<td width="5%"> <button class="btn btn-danger btn-xs" type="button" style="margin-top: 5px" onclick="$(this).parent().parent().remove()"> <i class="icon-trash "></i></button> </td> \
				  </tr>';
		$(tbody).append(tr);
	});
	$("#bt_debug_add_header").on('click',function(){
		var tbody=$(this).prev().find("tbody");
		var tr = '<tr> \
			        <td width="35%"><input type="text" class="form-control" id="input_debug_head_name" style="color:black"  name=""></td> \
					<td width="60%"><input type="text" class="form-control" id="input_debug_head_value"  style="color:black" name=""></td> \
					<td width="5%"> <button class="btn btn-danger btn-xs" type="button" style="margin-top: 5px" onclick="$(this).parent().parent().remove()"> <i class="icon-trash "></i></button> </td> \
				  </tr>';
		$(tbody).append(tr);
	});
	
	$("#div_debug_method").find("li").on('click',function(){
		ApiDebugTmp["method"] = $(this).find("a").html();
		var button = $(this).parent().prev();
		$(button).html(ApiDebugTmp["method"]+'<span class="caret"></span>');
	});
}

var ApiDebug= (function () {
	var main={};
	
//	PIBase.textAreaAutoHeight("textarea_debug_parmas",195);	
//	PIBase.textAreaAutoHeight("textarea_debug_response_header",410);
//	PIBase.textAreaAutoHeight("textarea_debug_response_text",410);
//	PIBase.textAreaAutoHeight("textarea_debug_response_json",410);
//	PIBase.textAreaAutoHeight("textarea_debug_response_request",410);
	
	$("#textarea_debug_parmas").autoTextarea();
	$("#textarea_debug_response_header").autoTextarea();
	$("#textarea_debug_response_text").autoTextarea();
	$("#textarea_debug_response_json").autoTextarea();
	$("#textarea_debug_response_request").autoTextarea();
	
	DebugResultSetting();
	DebugRadioSetting();
	DebugDataSetting();
	

	main.debug = function(){
		var url = $("#input_debug_url").val();
		alert(url);
		if(!$.IsURL(url)){
			$.fail_prompt("请输入正确的urlssss");
			return;
		}
		if(""==url){
			$.fail_prompt("url不能为空");
			return;
		}
		var method = ApiDebugTmp["method"];
		var head = {};
		var headtr = $("#table_debug_head").find("tbody tr");
		for(var i=0;i<headtr.length;i++){
			name=$(headtr[i]).find("#input_debug_head_name").val();
			value=$(headtr[i]).find("#input_debug_head_value").val();
			console.log(name);
			console.log(value);
			if(""==name||""==value){
				continue;
			}
			
			head[name] = value;
		};
		console.log(head);
		console.log(headtr);
		var checkedvalue = $("input[name='debug_parmas']:checked").val();
		var json = $("#textarea_debug_parmas").val();
		var jsonObj = {}
		var parmastr = $("#table_debug_parmas").find("tbody tr");
		var parmas = [];
		for(var i=0;i<parmastr.length;i++){
			parmastmp = {};
			parmastmp["name"]=$(parmastr[i]).find("#input_debug_parmas_name").val();
			parmastmp["value"]=$(parmastr[i]).find("#input_debug_parmas_value").val();
			if(""==parmastmp["name"]||""==parmastmp["value"]){
				continue;
			}
			parmas.push(parmastmp);
		}
		
		var data = {};
		data["url"] = url;
		data["method"] = method;
		data["header"] = head;
		data["parmasType"] = checkedvalue;
		if("json" == checkedvalue){
			try{
				jsonobj = JSON.parse(json);
				$("#textarea_debug_parmas").val(JSON.stringify(jsonobj, null, 8))
//				PIBase.setStyle('textarea_debug_parmas',195);
			}catch(err){
				$.fail_prompt("json格式不正确，请重新检查输入");
				return;
			}
			data["json"] = jsonobj;
		}else{
			data["form"] = parmas;
		}
		
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
			    var body = data.data.body;
			    var head = data.data.head;
			    var request = data.data.request;
			    var status = data.data.status;
			    
			    $("#textarea_debug_response_text").val(body);
			    try{
			    	var obj = JSON.parse(body);
			    	var jsonstr = JSON.stringify(obj,null,8);
			    	$("#textarea_debug_response_json").val(jsonstr);
			    	
			    }catch(err){
			    	$("#textarea_debug_response_json").val("");
			    }
			    
			    var headstr = ""; 
			    for(var i in head){
			    	headstr += i+":\t"+head[i+""]+"\n"
			    }
			    $("#textarea_debug_response_header").val(headstr);
			    
			    var requeststr = "";
			    requeststr += "status:\t"+status+"\n"
			    requeststr += "url:\t"+request.url+"\n"
			    requeststr += "header:\n"
			    for(var i in request.head){
			    	requeststr += "\t"+i+":\t"+request.head[i+""]+"\n"
			    }
			    
			    if("json" == request.parmasType){
			    	requeststr += "json:\n"
			    	requeststr += JSON.stringify(request.json,null,8);
			    }else{
			    	requeststr += "x-www-form-urlencoded:\n"
			    	for(var i in request.form){
				    	requeststr += "\t"+ i+":\t"+request.form[i+""]+"\n"
				    }
			    }
			    $("#textarea_debug_response_request").val(requeststr);
			    
//			    PIBase.setStyle('textarea_debug_response_json',410);
//			    PIBase.setStyle('textarea_debug_response_text',410);
//			    PIBase.setStyle('textarea_debug_response_header',410);
//			    PIBase.setStyle('textarea_debug_response_request',410);
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		$.requestJson("/api/debug","POST",data,callback);
		
	}
	
	main.debugApi = function(){
		var method = $("#lable_Inter_method").html();
		var url = $("#lable_Inter_url").html();
		$("#input_debug_url").val(url);
		ApiDebugTmp["method"] = method;
		$("#div_debug_method").find("button").html(ApiDebugTmp["method"]+'<span class="caret"></span>');

		var headtr = $("#tb_header").find("tbody tr");
		$("#table_debug_head").find("tbody").html("");
		var tbody=$("#table_debug_head").find("tbody");
		for(var i=0;i<(headtr.length-1);i++){
			console.log(headtr);
			name = $(headtr[i]).find("td.head_name").html();
			value = $(headtr[i]).find("td.head_value").html();
			if(""==name||undefined==name){
				continue;
			}
			var tr = '<tr> \
				        <td width="35%"><input type="text" class="form-control" id="input_debug_head_name" style="color:black" value="'+name+'"></td> \
						<td width="60%"><input type="text" class="form-control" id="input_debug_head_value" style="color:black"  value="'+value+'"></td> \
						<td width="5%"> <button class="btn btn-danger btn-xs" type="button" style="margin-top: 5px" onclick="$(this).parent().parent().remove()"> <i class="icon-trash "></i></button> </td> \
					  </tr>';
			$(tbody).append(tr);
		}

		var parmastr = $("#tb_parmas").find("tbody tr");
		$("#table_debug_parmas").find("tbody").html("");
		for(var i=0;i<(parmastr.length-1);i++){
			name = $(parmastr[i]).find("td.parmas_name").html();
			
			if(""==name||undefined==name){
				continue;
			}
			var tbody=$("#table_debug_parmas").find("tbody");
			var tr = '<tr> \
				        <td width="35%"><input type="text" class="form-control" id="input_debug_parmas_name" style="color:black" value="'+name+'"></td> \
						<td width="60%"><input type="text" class="form-control" id="input_debug_parmas_value"  style="color:black" name=""></td> \
						<td width="5%"> <button class="btn btn-danger btn-xs" type="button" style="margin-top: 5px" onclick="$(this).parent().parent().remove()"> <i class="icon-trash "></i></button> </td> \
					  </tr>';
			$(tbody).append(tr);
		};	
		var parmasType = $("#lable_Inter_parmas_type").html();
		var json = $("#textarea_inter_parmas").val();
		$("#textarea_debug_parmas").val(json);

		$("#textarea_debug_parmas").autoTextarea();
		if("json"==parmasType){
			$("input[name='debug_parmas']:eq(1)").attr("checked",'checked'); 
			$("#div_debug_parmas_json").show();
			$("#div_debug_parmas_form").hide();
		}else{
			$("input[name='debug_parmas']:eq(0)").attr("checked",'checked'); 
			$("#div_debug_parmas_json").hide();
			$("#div_debug_parmas_form").show();
		}
		$('#tab_menu a[href="#api_debug"]').tab('show');
	};
	
	main.debugCase = function(){
		var method = $("#input_case_api_method").val();
		var url = $("#input_case_api_url").val();
		$("#input_debug_url").val(url);
		ApiDebugTmp["method"] = method;
		$("#div_debug_method").find("button").html(ApiDebugTmp["method"]+'<span class="caret"></span>');

		var headtr = $("#tb_case_header").find("tbody tr");
		$("#table_debug_head").find("tbody").html("");
		var tbody=$("#table_debug_head").find("tbody");
		for(var i=0;i<(headtr.length);i++){
			name = $(headtr[i]).find("#case_head_name").val();
			value = $(headtr[i]).find("#case_head_value").val();
			if(""==name||undefined==name){
				continue;
			}
			var tr = '<tr> \
				        <td width="35%"><input type="text" class="form-control" id="input_debug_head_name" style="color:black" value="'+name+'"></td> \
						<td width="60%"><input type="text" class="form-control" id="input_debug_head_value" style="color:black"  value="'+value+'"></td> \
						<td width="5%"> <button class="btn btn-danger btn-xs" type="button" style="margin-top: 5px" onclick="$(this).parent().parent().remove()"> <i class="icon-trash "></i></button> </td> \
					  </tr>';
			$(tbody).append(tr);
		}

		var parmastr = $("#tb_case_parmas").find("tbody tr");
		$("#table_debug_parmas").find("tbody").html("");
		for(var i=0;i<(parmastr.length);i++){
			name = $(parmastr[i]).find("#case_parmas_name").val();
			value = $(parmastr[i]).find("#case_parmas_value").val();
			if(""==name||undefined==name){
				continue;
			}
			var tbody=$("#table_debug_parmas").find("tbody");
			var tr = '<tr> \
				        <td width="35%"><input type="text" class="form-control" id="input_debug_parmas_name" style="color:black" value="'+name+'"></td> \
						<td width="60%"><input type="text" class="form-control" id="input_debug_parmas_value"  style="color:black" value="'+value+'"></td> \
						<td width="5%"> <button class="btn btn-danger btn-xs" type="button" style="margin-top: 5px" onclick="$(this).parent().parent().remove()"> <i class="icon-trash "></i></button> </td> \
					  </tr>';
			$(tbody).append(tr);
		};
		
		var parmasType = GlobalData["select_case_info"].apiparmasType;
		var json = $("#textarea_case_parmas").val();
		$("#textarea_debug_parmas").val(json);
//		PIBase.textAreaAutoHeight("",195);	
		$("#textarea_debug_parmas").autoTextarea();
		if("json"==parmasType){
			$("input[name='debug_parmas']:eq(1)").attr("checked",'checked'); 
			$("#div_debug_parmas_json").show();
			$("#div_debug_parmas_form").hide();
		}else{
			$("input[name='debug_parmas']:eq(0)").attr("checked",'checked'); 
			$("#div_debug_parmas_json").hide();
			$("#div_debug_parmas_form").show();
		}
		$('#tab_menu a[href="#api_debug"]').tab('show');
	};
	
	return main;
}());


