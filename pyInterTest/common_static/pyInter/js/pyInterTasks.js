/**
 * author:anonymous
 */
var TaskEditTmp = {};

/** 
 * 获取当前时间 格式：yyyy-MM-dd HH:MM:SS 
 */  
var getCurrentTime = function(){
	/** 
	 * 补零 
	 */  
	function zeroFill(i){  
	    if (i >= 0 && i <= 9) {  
	        return "0" + i;  
	    } else {  
	        return i;  
	    }  
	}
    var date = new Date();//当前时间  
    var month = zeroFill(date.getMonth() + 1);//月  
    var day = zeroFill(date.getDate());//日  
    var hour = zeroFill(date.getHours());//时  
    var minute = zeroFill(date.getMinutes());//分  
    //当前时间  
    var curTime = date.getFullYear() + "-" + month + "-" + day  
            + " " + hour + ":" + minute;  
    return curTime;
}

var TaskDefaultTimeSetting = function(){
	$("#input_add_task_datetimepicker").val(getCurrentTime());//设置当前时间
	$('#input_add_task_datetimepicker').datetimepicker({//新建任务的时候
		format: 'yyyy-mm-dd hh:ii',      /*此属性是显示顺序，还有显示顺序是mm-dd-yyyy*/
		autoclose: true,
		todayBtn: true,
		todayHighlight:true,
	});
	$("#input_edit_task_datetimepicker").val(getCurrentTime());//设置当前时间
	$('#input_edit_task_datetimepicker').datetimepicker({//编辑任务的时候
		format: 'yyyy-mm-dd hh:ii',      /*此属性是显示顺序，还有显示顺序是mm-dd-yyyy*/
		autoclose: true,
		todayBtn: true,
		todayHighlight:true,
	});
}

var TaskTypeSetting = function(){
	//任务类型显示设置
	$("input[name='task_type']").on('click',function(){
		var v = $(this).val();
		if("1"==v){
			$("#div_task_add_for_time_task").show();
		}else{
			$("#div_task_add_for_time_task").hide();
		}
	});
	//任务类型显示设置
	$("input[name='task_type_edit']").on('click',function(){
		var v = $(this).val();
		if("1"==v){
			$("#div_task_edit_for_time_task").show();
		}else{
			$("#div_task_edit_for_time_task").hide();
		}
	});
}

var TaskAddSetting = function(){
	//新建任务模态框弹出后的事件
	$('#modal_add_task').on('show.bs.modal', function () {
		$("#input_add_task_datetimepicker").val(getCurrentTime());//设置当前时间
		TaskHandle.get_suite_list("#select_task_suite_list");
		TaskHandle.get_env_list("#select_task_env_list");
	});
	//创建任务
	// modal表单验证定义,添加suite
    $('#form_task_add_task').bootstrapValidator({
　　　　　message: '参数不正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_add_task_name: {
                validators: {
                    notEmpty: {
                        message: '名称不能为空'
                    }
                }
            }
        }
    });
	$("#bt_task_add_task").on('click',function(){
		var pId = ProjectInfo["pId"];
		var bootstrapValidator = $("#form_task_add_task").data('bootstrapValidator');
	    // 手动触发验证
	    bootstrapValidator.validate();
	    if(!bootstrapValidator.isValid()){
	    	return;
	    }
	    var name=$("#input_add_task_name").val();
	    
	    suiteOption = $("#select_task_suite_list").find("option:selected");
	    if(suiteOption.length == 0 || undefined == suiteOption){
	    	$.fail_prompt("请首先选择或者创建测试套件");
	    	return;
	    }
	    var suId = Number($(suiteOption).attr("suId"));
	    
	    envOption = $("#select_task_env_list").find("option:selected");
	    if(envOption.length == 0 || undefined == envOption){
	    	$.fail_prompt("请首先选择或者创建执行环境");
	    	return;
	    }
	    var	eId = Number($(envOption).attr("eId"));

	    var taskType = $("input[name='task_type']:checked").val();
	    
	    var repeatDateTime = $("#input_add_task_datetimepicker").val();
	    
	    var repeatType = $("input[name='repeat_type']:checked").val();
	    
	    var data = {};
	    data["pId"] = pId;
	    data["name"] = name;
	    data["suId"] = suId;
	    data["eId"] = eId;
	    data["taskType"] = taskType;
	    data["repeatDateTime"] = repeatDateTime;
	    data["repeatType"] = repeatType;
	    
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$("#modal_add_task").modal('toggle');
				var d = data.data;
				var t = TaskHandle.make_task_panel(d.tId,d.name,d.suId,d.suName,d.eId,d.eName,d.taskType,d.repeatDateTime,d.repeatType,d.status,d.successRate);
				$("#panel_task_list").prepend(t);
				TaskHandle.task_panel_toggle_event();
				TaskHandle.collapse_show_event();
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/task/add","POST",data,callback);
	});
}

var TaskGetDataSetting = function(){
	//获取全部的task列表
	$("#task_tab").on('click',function(){
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var list = data.data;
				$("#panel_task_list").html("");
				for(var i=0;i<list.length;i++){
					var t = TaskHandle.make_task_panel(list[i].tId,list[i].name,list[i].suId,list[i].suName,list[i].eId,list[i].eName,list[i].taskType,list[i].repeatDateTime,list[i].repeatType,list[i].status,list[i].successRate);
					$("#panel_task_list").append(t);
				}
				TaskHandle.task_panel_toggle_event();
				TaskHandle.collapse_show_event();
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/task/list","POST",{"pId":ProjectInfo["pId"]},callback);
	});
}

var TaskEditSetting = function(){
    $('#form_task_edit_task').bootstrapValidator({
   　　　　　message: '参数不正确！',
           feedbackIcons: {
   　　　　　　　　validating: 'glyphicon glyphicon-refresh'
   　　　　　},
           fields: {
        	   input_edit_task_name: {
                   validators: {
                       notEmpty: {
	                           message: '名称不能为空'
                   }
               }
    	   }
       }
    });
    $("#bt_task_edit_task").on("click",function(){
		var bootstrapValidator = $("#form_task_edit_task").data('bootstrapValidator');
	    // 手动触发验证
	    bootstrapValidator.validate();
	    if(!bootstrapValidator.isValid()){
	    	return;
	    }
	    var tId = Number($(TaskEditTmp).attr("tId"));
	    
	    var name=$("#input_edit_task_name").val();
	    suiteOption = $("#select_task_suite_list_edit").find("option:selected");
	    if(0==suiteOption.length || undefined == suiteOption){
	    	$.fail_prompt("请首先选择或者创建测试套件");
	    	return;
	    }
	    var suId = Number($(suiteOption).attr("suId"));
	    
	    envOption = $("#select_task_env_list_edit").find("option:selected");
	    if(0==envOption.length || undefined == envOption){
	    	$.fail_prompt("请首先选择或者创建执行环境");
	    	return;
	    }
	    var eId = Number($(envOption).attr("eId"));
	    
	    var taskType = $("input[name='task_type_edit']:checked").val();
	    
	    var repeatDateTime = $("#input_edit_task_datetimepicker").val();
	    
	    var repeatType = $("input[name='repeat_type_edit']:checked").val();
	    
	    var data = {};
	    data["tId"] = tId;
	    data["name"] = name;
	    data["suId"] = suId;
	    data["eId"] = eId;
	    data["taskType"] = taskType;
	    data["repeatDateTime"] = repeatDateTime;
	    data["repeatType"] = repeatType;
	    
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$("#modal_edit_task").modal('toggle');
				var d = data.data;
				var t = TaskHandle.make_task_panel(d.tId,d.name,d.suId,d.suName,d.eId,d.eName,d.taskType,d.repeatDateTime,d.repeatType,d.status,d.successRate);
				$(TaskEditTmp).before(t);
				$(TaskEditTmp).remove();
				TaskHandle.task_panel_toggle_event();
				TaskHandle.collapse_show_event();
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/task/update","POST",data,callback);
	});
}

var TaskHandle = (function () {
	main = {};
	
	//panel的弹出事件
	main.task_panel_toggle_event = function(){
		$(".pannel_task_head").on('click',function(){
			var others = $(this).parent().siblings();
			var content = $(this).next();
			for(var i=0;i<others.length;i++){
				var t = $(others[i]).find(".panel-collapse")
				if($(t).hasClass("in")){
					$(t).collapse('hide');
				}
			}
			$(content).collapse('toggle');
		});
	}
	
	main.get_suite_list = function(sid,suId=-1){
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			    list = data.data;
 			    $(sid).html("");
		    	for(var i=0;i<list.length;i++){
		    		var option = TaskHandle.make_suite_option(list[i].suId,list[i].name);
					$(sid).append(option);
				}
		    	$(sid).find("option[suId="+suId+"]").attr("selected",true);
		    	$(sid).selectpicker('refresh');
 		   }else{
 			   $.fail_prompt("新建失败："+data["message"],5000);
 		   }
		}
	 	$.requestJson("/suite/list","POST",{"pId":ProjectInfo.pId},callback);
	}
	main.make_suite_option = function(suId,name){
		var option = '<option suId='+suId+'>'+name+'</option>';
		return option;
	}
	main.get_env_list = function(sid,eId=-1){
		var pId = ProjectInfo["pId"];
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var list = data.data;
				$(sid).html("");
				for(var i=0;i<list.length;i++){
					var option = TaskHandle.make_env_option(list[i].eId,list[i].name);
					$(sid).append(option);
				}
//				$(sid).val("");
		    	$(sid).find("option[eId="+eId+"]").attr("selected", true); 
		    	$(sid).selectpicker('refresh');
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/setting/env/list","POST",{"pId":pId},callback);
	}
	main.make_env_option = function(eId,name){
		var option = '<option eId='+eId+'>'+name+'</option>';
		return option;
	}

	main.make_task_panel = function(tId,name,suId,suName,eId,eName,taskType,repeatDateTime,repeatType,status,successRate){
		var statusStr = "未执行";
		switch(status){
		case 0:
			statusStr = "未执行";
			break;
		case -1:
			statusStr = "执行失败";
			break;
		case 1:
			statusStr = "执行成功";
			break;
		}

		var repeatStr = "无定时";
		if(1==taskType){
			repeatStr = repeatDateTime + "&nbsp;";
			switch(repeatType){
			case -1:
				repeatStr += "无重复";
				break;
			case 1:
				repeatStr += "每天";
				break;
			case 3:
				repeatStr += "每3天";
				break;
			case 7:
				repeatStr += "每周";
				break;
			}
		}
		var div_list = $("#div_task_case_list_model").html();
		
		var panel = '<div class="panel panel-info task_panel_class" tId='+tId+' suId='+suId+' eId='+eId+'>\
						<div class="panel-heading pannel_task_head" style="cursor: pointer">\
							<div style="display: flex; justify-content: space-between">\
								<div>\
									<h4 class="panel-title">\
										<a data-toggle="collapse" data-parent="#panel_task_list" href="#taskList'+tId+'">'+name+'</a>\
									</h4>\
								</div>\
								<div>\
									<button class="btn btn-info btn-xs" onclick="TaskHandle.edit_task(this);$.stopBubble(event)">\
										<i class="icon-edit">编辑</i>\
									</button>\
									<button class="btn btn-danger btn-xs" onclick="TaskHandle.delete_task(this);$.stopBubble(event)">\
										<i class="icon-trash">删除</i>\
									</button>\
								</div>\
							</div>\
							<div style=" font-size: 13px">\
								<strong>测试套件:&nbsp;</strong><suite>'+suName+'</suite>\
							</div>\
							<div style=" font-size: 13px">\
								<strong>环境变量:&nbsp;</strong><env>'+eName+'</env>\
							</div>\
							<div style="display: flex; justify-content: space-between">\
								<div style=" font-size: 13px; width: 500px; display: flex; justify-content: flex-start">\
									<div style="width: 50%">\
										<strong>定时执行:&nbsp;</strong>'+repeatStr+'\
									</div>\
									<div style="width: 20%">\
										<strong>状态:&nbsp;</strong>\
										<status id="status_task_status">'+statusStr+'</status>\
									</div>\
									<div style="width: 20%">\
										<strong>成功率:&nbsp;</strong>\
										<success id="success_task_success_rate">'+successRate+'%</success>\
									</div>\
								</div>\
								<div>\
									<button class="btn btn-success btn-xs" style="margin-top: -10px" onclick="TaskHandle.runTask(this);$.stopBubble(event)">\
										<i class="icon-play">立刻执行</i>\
									</button>\
								</div>\
							</div>\
						</div>\
						<div id="taskList'+tId+'" class="panel-collapse collapse collapse_panel_body">\
							<div class="panel-body">'+div_list+'</div>\
						</div>\
					</div>';
		return panel;
	}
	
	//删除任务
	main.delete_task=function(obj){
		swal({
   	        title: "您确定要删除任务吗？",  
   	        text: "您确定要删除任务吗？",  
   	        type: "warning", 
   	        showCancelButton: true, 
   	        closeOnConfirm: true, 
   	        confirmButtonText: "是的，我要删除", 
   	        confirmButtonColor: "#ec6c62" 
   	    }, function() {
   	    	var callback = function(data){
   	 		   if(data["success"] == "true"|| data["success"] == true){
//   	              $.success_prompt("删除成功",2000);
   	              var t = $(obj).parents(".task_panel_class");
   	              $(t).remove();
   	 		   }else{
   	 			   $.fail_prompt("新建失败："+data["message"],5000);
   	 		   }
   			}
   			var data={};
   			var t = $(obj).parents(".task_panel_class");
   			data["tId"] = Number($(t).attr("tId"));
   		 	$.requestJson("/task/delete","POST",data,callback);
   	    }); 
		return false;
	}
	//编辑任务
	main.edit_task = function(obj){
		TaskEditTmp = $(obj).parents(".task_panel_class");
		
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			   //设置套件
 			   TaskHandle.get_suite_list("#select_task_suite_list_edit",data.data.suId);
 			   //设置环境变量
 			   TaskHandle.get_env_list("#select_task_env_list_edit",data.data.eId);
 			   //设置名称
 			   $("#input_edit_task_name").val(data.data.name);
 			   //设置任务类型
 			   if(0==data.data.taskType){
 				  $("#input_task_time_task_edit").removeAttr("checked");
 				  $("#input_task_handle_task_edit").prop("checked","checked");
 				  $("#div_task_edit_for_time_task").hide();
 			   }else{
 				  $("#input_task_handle_task_edit").removeAttr("checked");
 				  $("#input_task_time_task_edit").prop("checked","checked");
 				  $("#div_task_edit_for_time_task").show();
 			   }
 			   //设置时间
 			   $("#input_edit_task_datetimepicker").val(data.data.repeatDateTime);
 			   //设置类型重复类型
 			   $("input[name='repeat_type_edit']").removeAttr("checked");
 			   switch(data.data.repeatType){
 			   case -1:
 				   $("input[name='repeat_type_edit'][value=-1]").prop("checked","checked");
 				   break;
 			   case 1:
 				   $("input[name='repeat_type_edit'][value=1]").prop("checked","checked");
 				   break;
 			   case 3:
 				   $("input[name='repeat_type_edit'][value=3]").prop("checked","checked");
 				   break;
 			   case 7:
 				   $("input[name='repeat_type_edit'][value=7]").prop("checked","checked");
 				   break;
 			   }
 			   $("#modal_edit_task").modal("show");
 		   }else{
 			   $.fail_prompt("查询失败："+data["message"],5000);
 		   }
		}
		var data={};
		var tId = Number($(TaskEditTmp).attr("tId"));
		data["tId"] = tId;
	 	$.requestJson("/task/get","POST",data,callback);
	}
	
	//查看案例列表
	main.fresh_task_case = function(obj){
		var tbody = $(obj).find("#tbody_case_list_detail");
		var time = $(obj).find("#last_running_time");
		var user = $(obj).find("#last_running_user");
		var success = $(obj).find("#last_running_success_count");
		var failed = $(obj).find("#last_running_failed_count");
		var lastResult = $(obj).find("#last_running_result");
		var preSql = $(obj).find("#div_task_show_pre_sql");
		var postSql = $(obj).find("#div_task_show_post_sql");
		var preRequire = $(obj).find("#table_pre_require_detail");
		var preRequireBody = $(obj).find("#tbody_pre_require_detail");
		
		var tId = Number($(obj).parent().attr("tId"));
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var list = data.data.cases;
				var pre = data.data.preRequirement;
				
				$(time).html(data.data.lastRunningTime);
				$(user).html(data.data.lastRunningUser);
				$(success).html(data.data.lastRunningSuccessCount);
				$(failed).html(data.data.lastRunningfailedCount);
				$(lastResult).html(data.data.lastRunningResult);
				
				if(0==data.data.preRequirement.length && ""==data.data.preSql){
					$(preSql).parent().hide();
				}else{
					$(preSql).parent().show();
					if(""!=data.data.preSql){
						$(preSql).show();
						$(preSql).html(data.data.preSql);
					}else{
						$(preSql).hide();
					}
					if(0==data.data.preRequirement.length){
						$(preRequire).hide();
					}else{
						$(preRequire).show();
						$(preRequireBody).html("")
						for(var i=0;i<pre.length;i++){
							var tr = TaskHandle.make_task_case_list_tr(pre[i].apiName,pre[i].name,pre[i].success,pre[i].rId);
							$(preRequireBody).append(tr);
						}
					}
				}
				
				
				if(""!=data.data.postSql){
					$(postSql).parent().show();
					$(postSql).html(data.data.postSql);
				}else{
					$(postSql).parent().hide();
				}
				
				$(tbody).html("")
				for(var i=0;i<list.length;i++){
					var tr = TaskHandle.make_task_case_list_tr(list[i].apiName,list[i].name,list[i].success,list[i].rId);
					$(tbody).append(tr);
				}
				console.log();
			}else{
				$.fail_prompt("加载数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/task/getCases","POST",{"tId":tId},callback);
	}
	main.collapse_show_event = function(){
		$('.collapse_panel_body').on('show.bs.collapse', function () {
			TaskHandle.fresh_task_case(this);
		});
	}
	main.make_task_case_list_tr = function(apiName,caseName,status,rId){
		var s = "";
		switch(status){
		case 1:
			s = '<span class="label label-success label-mini">pass</span>';
			break;
		case 0:
			s = '<span class="label label-danger label-mini">failed</span>'
			break;
		case -1:
			s = '<span class="label label-primary label-mini">none</span>'
			break;
		default:
			s = '<span class="label label-primary label-mini">none</span>'
		}
		var tr = '<tr rId='+rId+'><td width="40%" id="a_task_case_api_name">'+apiName+'</td>\
        <td width="40%" id="a_task_case_case_name">'+caseName+'</td>\
        <td width="10%">'+s+'</td>\
        <td width="10%"><button class="btn btn-primary btn-xs" onclick="TaskHandle.show_test_result(this)"><i class="icon-ok">结果</i></button>\
        </td>\
       </tr>';

		return tr;
	}
	
	//立刻执行任务
	main.runTask = function(obj){

		var panel = $(obj).parents(".task_panel_class");
		var content = $(panel).find(".collapse_panel_body");
		var tId = $(panel).attr("tId");
		var uId = PIBase.userInfo["userId"]
		tId = Number(tId);
		$(panel).find("status").html("正在执行");
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				//更新数据
				$(panel).find("success").html(data.data.successRate + "%");
				TaskHandle.fresh_task_case($(content));
				$.success_prompt("执行成功",2000);
			}else{
				$.fail_prompt("执行任务失败："+data["message"],5000);
			}
			$(panel).find("status").html("未执行");
		}
		$.requestJson("/task/run","POST",{"tId":tId,"uId":uId},callback);
	}
	
	main.tmpResult = ""
	//获取result
	main.get_task_result = function(obj,call){
		var tr = $(obj).parents("tr");
		var rId = Number($(tr).attr("rId"));
		if(-1 == rId) {
			$.fail_prompt("无结果！",5000);
			return;
		}
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				TaskHandle.tmpResult = data.data;
				call();
			}else{
				$.fail_prompt("获取结果失败："+data["message"],5000);
			}
		}
		$.requestJson("/case/getResult","POST",{"rId":rId},callback);
	}
	
	//显示result
	main.show_test_result = function(obj){
		callback = function(){
			TaskHandle.show_result_message()
			TaskHandle.show_result_preSql();
			TaskHandle.show_result_preSql();
			TaskHandle.show_result_request();
			TaskHandle.show_result_response();
			TaskHandle.show_result_picker();
			TaskHandle.show_result_assert();
			$("#modal_show_test_result").modal("show");
		}
		TaskHandle.get_task_result(obj,callback);
	}
	
	//显示执行消息结果
	main.show_result_message = function(){
		$("#tab_result_message").html(TaskHandle.tmpResult.message);
	}
	//显示前置sql
	main.show_result_preSql = function(){
		$("#tab_result_pre_sql").html(TaskHandle.tmpResult.preSql);
	}
	//显示后置sql
	main.show_result_postSql = function(){
		$("#tab_result_post_sql").html(TaskHandle.tmpResult.postSql);
	}
	//显示请求
	main.show_result_request = function(){
		
		$("#div_task_result_show_url").html(TaskHandle.tmpResult.method+"&nbsp;&nbsp;"+TaskHandle.tmpResult.url+"&nbsp;&nbsp;HTTP/1.1");
		var head = ""
		for(i in TaskHandle.tmpResult.requestHead){
			head += i + ":&nbsp;"+TaskHandle.tmpResult.requestHead[i] + "<br>";
		}
		$("#div_task_result_show_request_head").html(head);
		if("json"==TaskHandle.tmpResult.parmasType){
			$("#div_task_result_show_request_body_type").html("json:");
//			var s = "";
//			try{
//				s = JSON.stringify(TaskHandle.tmpResult.requestBody, null, 8)
//			}catch(e){
//				s = String(TaskHandle.tmpResult.requestBody) + "";
//			}
			var s = String(TaskHandle.tmpResult.requestBody) + "";
			s = $.toJson(s);
			s = $.text2divText(s);
			$("#div_task_result_show_request_body").html(s);
		}else{
			$("#div_task_result_show_request_body_type").html("form:");
			var s = "";
			for(i in TaskHandle.tmpResult.requestBody){
				s += i + ":&nbsp;"+TaskHandle.tmpResult.requestBody[i]+"<br>"
			}
			if(""==s){
				s = JSON.stringify(TaskHandle.tmpResult.requestBody, null, 8)
			}
			$("#div_task_result_show_request_body").html(s);
		}
	}
	//显示response
	main.show_result_response = function(){
		var head = ""
		for(i in TaskHandle.tmpResult.responseHead){
			head += i + ":&nbsp;"+TaskHandle.tmpResult.responseHead[i] + "<br>";
		}
		$("#div_task_result_show_response_head").html(head);
		var s = TaskHandle.tmpResult.responseBody;
		s = $.toJson(s);
		s = $.text2divText(s);
		$("#div_task_result_show_response_body").html(s);
	}
	//显示picker
	main.show_result_picker = function(){
		var tbody = $("#tab_result_picker").find("tbody");
		$(tbody).html("");
		for(var i in TaskHandle.tmpResult.pickerValues){
			var tr = '<tr><td width="30%">'+i+'</td><td width="70%">'+TaskHandle.tmpResult.pickerValues[i]+'</td></tr>';
			$(tbody).append(tr);
		}
	}
	//显示assert
	main.show_result_assert = function(){
		var div_sql = $("#tab_result_assert").find("#div_task_result_sql_assert");
		tbody = $("#tab_result_assert").find("tbody");
		$(div_sql).html("");
		for(var i=0;i<TaskHandle.tmpResult.asserts.length;i++){
			var a_s = "";
			var a_e = "";
			var a_m = "";
			if("sql"==TaskHandle.tmpResult.asserts[i].assertType){
				a_s = '<a class="list-group-item"><h5 class="list-group-item-heading">'+TaskHandle.tmpResult.asserts[i].sql+'</h5>';
				a_e = '<p class="list-group-item-text">'+TaskHandle.tmpResult.asserts[i].sqlAssert+'</p></a>';
			}else{
				var t = TaskHandle.tmpResult.asserts[i].key;
				if(""!=TaskHandle.tmpResult.asserts[i].value){
					t +="&nbsp;:&nbsp;"+TaskHandle.tmpResult.asserts[i].value;
				}
				a_s = '<a  class="list-group-item"><h5 class="list-group-item-heading">'+t+'</h5>';
				a_e = '<p class="list-group-item-text">'+TaskHandle.tmpResult.asserts[i].type+'</p></a>';
			}
			a_m = '<span class="badge badger-danger">failed</span>';
			var result = TaskHandle.tmpResult.asserts[i].result
			if("true"==result || true==result||"True"==result){
				a_m = '<span class="badge badger-success">success</span>';
			}
			$(div_sql).append(a_s + a_m + a_e);
		}
	}
	
	//历史记录
	main.show_history_result = function(obj){
		var t = $(obj).parents(".task_panel_class");
		var tId = Number($(t).attr("tId"));
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var list =data.data;
				$("#div_task_history_list").html("");
				for(var i=0;i<list.length;i++){
					var tr = TaskHandle.make_history_li(list[i].hId,list[i].time,list[i].version,list[i].name);
					$("#div_task_history_list").append(tr);
				}
				$("#modal_show_task_history").modal('show');
			}else{
				$.fail_prompt("获取结果失败："+data["message"],5000);
			}
		}
		$.requestJson("/task/getHistory","POST",{"tId":tId},callback);
	}
	main.make_history_li = function(hId,time,version,name){
		var tr = '<a class="list-group-item" hId='+hId+' version='+version+' time="'+time+'" name="'+name+'">\
					<label>版本: '+version+'&nbsp;&nbsp;&nbsp;&nbsp;执行时间: '+time+'</label>\
					<span class="badge badger-info" style="cursor:pointer" onclick="TaskHandle.getHistoryResult(this)">\
						<i class="icon-share-alt">查看</i>\
					</span>\
				 </a>';
		return tr;
	}
	main.getHistoryResult = function(obj){
		var t = $(obj).parent();
		var hId = $(t).attr("hId");
		window.open("/history/"+hId);
	}
//	main.downloadHistoryResult = function(obj){
//		if ('download' in document.createElement('a')) {
//		    // 作为test.html文件下载
//			var t = $(obj).parent();
//			var hId = Number($(t).attr("hId"));
//			var name = $(t).attr("name");
//			var time = $(t).attr("time");
//			var callback=function(data){
//				if(data["success"] == "true"|| data["success"] == true){
//					TaskHandle.makeHtmlReport("test", name+'-'+time+'.html');
//				}else{
//					$.fail_prompt("获取结果失败："+data["message"],5000);
//				}
//			}
//			$.requestJson("/task/getHistoryReport","POST",{"hId":hId},callback);
//		} else {
//			alert('浏览器不支持'); 
//		}
//	}
//	main.makeHtmlReport = function (content, filename) {
//		$("body").mLoading("show");
//	    var eleLink = document.createElement('a');
//	    eleLink.download = filename;
//	    eleLink.style.display = 'none';
//	    // 字符内容转变成blob地址
//	    var blob = new Blob([content]);
//	    eleLink.href = URL.createObjectURL(blob);
//	    // 触发点击
//	    document.body.appendChild(eleLink);
//	    eleLink.click();
//	    // 然后移除
//	    document.body.removeChild(eleLink);
//	    $("body").mLoading("hide");
//	};
	
	
	TaskDefaultTimeSetting();
	TaskTypeSetting();
	TaskAddSetting();
	TaskEditSetting();
	TaskGetDataSetting();
//	TaskHistorySetting();
	return main;
}());


