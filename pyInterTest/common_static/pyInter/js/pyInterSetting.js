var SelectEnv = {};
var SelectObj = {};
var TmpDeleteAssert={}
var TmpDeleteGlobalValue={}

var SettingAddEnvSetting = function(){
	// modal表单验证定义,添加suite
    $('#form_new_env').bootstrapValidator({
　　　　　message: '参数不正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_new_env_name: {
                validators: {
                    notEmpty: {
                        message: '名称不能为空'
                    }
                }
            }
        }
    });
  //添加执行环境
	$("#bt_setting_add_env").on("click",function(){

		$("#add_env_modal").modal("show");
		$("#h4_modal_env_title").html("添加执行环境");
		$("#bt_create_env").html("创建");
		$("#bt_create_env").attr('onclick','').unbind('click').click(function(){
			var bootstrapValidator = $("#form_new_env").data('bootstrapValidator');
		    // 手动触发验证
		    bootstrapValidator.validate();
		    if(!bootstrapValidator.isValid()){
		    	return;
		    }
			var pId = ProjectInfo["pId"];
			var name = $("#input_new_env_name").val();
			if(""==name){
				return;
			}
			var callback=function(data){
				if(data["success"] == "true"|| data["success"] == true){
					var li = SettingHandle.make_env_li(data.data.name,data.data.eId);
					$("#ul_setting_env").append(li);
					$("#add_env_modal").modal("hide");
				}else{
					$.fail_prompt("修改数据失败："+data["message"],5000);
				}
			}
			$.requestJson("/setting/add/env","POST",{"pId":pId,"name":name},callback);
		});
	})
}

var SettingEnvListIconSetting = function(){
	$('#div_env_list').on('show.bs.collapse', function () {
		$("#i_setting_env_collapse").attr("class","icon-chevron-up");
	});
	$('#div_env_list').on('hide.bs.collapse', function () {
		$("#i_setting_env_collapse").attr("class","icon-chevron-down");
	});
}

var SettingGetDataSetting = function(){
	//获取执行环境
	$("#setting_tab").on("click",function(){
		var pId = ProjectInfo["pId"];
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var list = data.data;
				$("#ul_setting_env").html("");
				for(var i=0;i<list.length;i++){
					var li = SettingHandle.make_env_li(list[i].name,list[i].eId);
					$("#ul_setting_env").append(li);
				}
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/setting/env/list","POST",{"pId":pId},callback);
	});
}

var SettingEditEnvSetting = function(){
	//编辑env
	$("#bt_setting_edit_env").on("click",function(){
		var active = $("#ul_setting_env").find("li.active");
		if(active.length<1){
			return;
		}
		$("#add_env_modal").modal("show");
		$("#h4_modal_env_title").html("编辑执行环境");
		$("#bt_create_env").html("保存");
		$("#input_new_env_name").val(SelectEnv["name"]);
		$("#bt_create_env").attr('onclick','').unbind('click').click(function(){
			var bootstrapValidator = $("#form_new_env").data('bootstrapValidator');
		    // 手动触发验证
		    bootstrapValidator.validate();
		    if(!bootstrapValidator.isValid()){
		    	return;
		    }
			var eId = SelectEnv["eId"];
			var name = $("#input_new_env_name").val();
			if(""==name){
				return;
			}
			var callback=function(data){
				if(data["success"] == "true"|| data["success"] == true){
					SelectEnv["name"] = data.data.name;
					$(SelectObj).find("#env_name").html(data.data.name);
					$("#add_env_modal").modal("hide");
				}else{
					$.fail_prompt("修改数据失败："+data["message"],5000);
				}
			}
			$.requestJson("/setting/update/env","POST",{"eId":eId,"name":name},callback);
		});
	});
}

var SettingDelEnvSetting = function(){
	//删除env
	$("#bt_setting_del_env").on("click",function(){
		var active = $("#ul_setting_env").find("li.active");
		if(active.length<1){
			return;
		}
		swal({
   	        title: "您确定要删除执行环境吗？",  
   	        text: "您确定要删除执行环境吗？",  
   	        type: "warning", 
   	        showCancelButton: true, 
   	        closeOnConfirm: true, 
   	        confirmButtonText: "是的，我要删除", 
   	        confirmButtonColor: "#ec6c62" 
   	    }, function() {
   	    	var callback = function(data){
   	 		   if(data["success"] == "true"|| data["success"] == true){
//   	              $.success_prompt("删除成功",2000);
   	              $(SelectObj).remove();
   	              
   	           $("#div_project_setting_env_deail").hide();
   	           $("#div_project_setting_assert").hide();
   	           $("#div_project_setting_no_data").show();
   	 		   }else{
   	 			   $.fail_prompt("删除失败："+data["message"],5000);
   	 		   }
   			}
   		 	$.requestJson("/setting/delete/env","POST",{"eId":SelectEnv["eId"]},callback);
   	    }); 
	});
}

var SettingAddAssertSetting = function(){
	//添加全局断言
	$('#form_system_assert_add_assert').bootstrapValidator({
　　　　　message: '参数不正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_add_system_assert_name: {
                validators: {
                    notEmpty: {
                        message: '名称不能为空'
                    }
                }
            },
            input_add_system_assert_key: {
                validators: {
                    notEmpty: {
                        message: '关键字不能为空'
                    }
                }
            }
        }
    });
	$("#bt_add_system_assert").on("click",function(){
		var bootstrapValidator = $("#form_system_assert_add_assert").data('bootstrapValidator');
	    // 手动触发验证
	    bootstrapValidator.validate();
	    if(!bootstrapValidator.isValid()){
	    	return;
	    }
	    var pId = ProjectInfo["pId"];
	    var name = $("#input_add_system_assert_name").val();
	    var key = $("#input_add_system_assert_key").val();
	    var value = $("#input_add_system_assert_value").val();
	    var typeText = $("#select_add_system_assert_type").val();
	    var type=0;
	    if("exclude" == typeText){
	    	type=1;
	    }
	    var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var li = SettingHandle.make_assert_tr(data.data.name,data.data.key,data.data.value,data.data.type,data.data.sId);
				$("#tbody_system_assert_list").append(li);
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
	    var data={};
	    data["pId"] = pId;
	    data["name"] = name;
	    data["key"] = key;
	    data["value"] = value;
	    data["type"] = type;
		$.requestJson("/setting/add/assert","POST",data,callback);
	});
}

var SettingGetGlobalValuesSetting = function(){
	//添加全局参数
	$('#form_system_global_value').bootstrapValidator({
　　　　　message: '参数不正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_add_global_value_name: {
                validators: {
                    notEmpty: {
                        message: '名称不能为空'
                    }
                }
            },
            input_add_global_value_value: {
                validators: {
                    notEmpty: {
                        message: '变量值不能为空'
                    }
                }
            }
        }
    });
	$("#bt_add_global_value").on("click",function(){
		var bootstrapValidator = $("#form_system_global_value").data('bootstrapValidator');
	    // 手动触发验证
	    bootstrapValidator.validate();
	    if(!bootstrapValidator.isValid()){
	    	return;
	    }
	    var pId = ProjectInfo["pId"];
	    var name = $("#input_add_global_value_name").val();
	    var value = $("#input_add_global_value_value").val();
	    var type = $("#select_add_global_value_type").val();

	    var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var li = SettingHandle.make_global_value_tr(data.data.name,data.data.value,data.data.type,data.data.gId);
				$("#tbody_global_value_list").append(li);
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
	    var data={};
	    data["pId"] = pId;
	    data["name"] = name;
	    data["eId"] = SelectEnv["eId"];
	    data["value"] = value;
	    data["type"] = type;
		$.requestJson("/setting/add/globalValue","POST",data,callback);
	});
}

var SettingSaveDatabaseSetting = function(){
	//保存sql设置
	$('#form_setting_mysql').bootstrapValidator({
　　　　　message: '参数不正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_setting_sql_host: {
                validators: {
                    notEmpty: {
                        message: 'host不能为空'
                    }
                }
            },
            input_setting_sql_user: {
                validators: {
                    notEmpty: {
                        message: 'user不能为空'
                    }
                }
            },
            input_setting_sql_pwd: {
                validators: {
                    notEmpty: {
                        message: 'pwd不能为空'
                    }
                }
            },
            input_setting_sql_port: {
                validators: {
                    notEmpty: {
                        message: 'port不能为空'
                    }
                }
            },
            input_setting_sql_database: {
                validators: {
                    notEmpty: {
                        message: 'dabatase不能为空'
                    }
                }
            },
            
        }
    });
	
	$('#form_setting_ssh').bootstrapValidator({
	　　　　　message: '参数不正确！',
	        feedbackIcons: {
	　　　　　　　　validating: 'glyphicon glyphicon-refresh'
	　　　　　},
	        fields: {
	        	input_setting_ssh_host: {
	                validators: {
	                    notEmpty: {
	                        message: 'ssh host不能为空'
	                    }
	                }
	            },
	            input_setting_ssh_port: {
	                validators: {
	                    notEmpty: {
	                        message: 'ssh port 不能为空'
	                    }
	                }
	            },
	            input_setting_ssh_user: {
	                validators: {
	                    notEmpty: {
	                        message: 'ssh user 不能为空'
	                    }
	                }
	            },
	            input_setting_ssh_psw: {
	            	trigger:"change",
	                validators: {
	                    notEmpty: {
	                        message: 'ssh psw key 不能为空'
	                    }
	                }
	            },
	            
	        }
	    });
	
	$("#span_setting_switch_modal").on("click",function(){
		var value = $("#span_setting_switch_modal").attr("value");
		if(0==value || "0"==value){
			SettingHandle.showSqlModal(1);
		}else{
			SettingHandle.showSqlModal(0);
		}
	});
	//修改ssh模式
	$("#li_setting_switch_psw").on("click",function(e){
		var text = $(e.currentTarget).find("a").html();
		$("#input_setting_ssh_psw").val("");
		SettingHandle.showSSHModal(text,0);
	});
	$("#li_setting_switch_key").on("click",function(e){
		var text = $(e.currentTarget).find("a").html();
		$("#input_setting_ssh_psw").val("");
		SettingHandle.showSSHModal(text,1);
	});
	$("#input_setting_ssh_psw").on('click',function(){
		var index = $("#input_setting_ssh_psw").next().find("button").attr("tabindex");
		if(1==index || "1"==index){
			var s = document.getElementById("input_setting_file");  
			s.click();
		}
	});
	$("#input_setting_file").on("change",function(){
		var name = $("#input_setting_file")[0].files[0].name
		$("#input_setting_ssh_psw").val(name);
	});
	//保存配置
	$("#bt_setting_save_sql").on("click",function(){
		var bootstrapValidator = $("#form_setting_mysql").data('bootstrapValidator');
		var bootstrapValidator1 = $("#form_setting_ssh").data('bootstrapValidator');
	    // 手动触发验证
	    bootstrapValidator.validate();
	    if(!bootstrapValidator.isValid()){
	    	return;
	    }
	    var value = $("#span_setting_switch_modal").attr("value");
	    $('#input_setting_ssh_psw').change();
		if(1==value || "1"==value){
			bootstrapValidator1.validate();
		    if(!bootstrapValidator1.isValid()){
		    	return;
		    }
		    var sshtype = $("#input_setting_ssh_psw").next().find("button").attr("tabindex");
			if(0==sshtype||"0"==sshtype){
				SettingHandle.saveSSHSqlSetting();
			}else{
				var n = $('#input_setting_file')[0].files[0];
				if(undefined == n || ""==n || null==n){
					SettingHandle.saveSSHSqlSetting();
				}else{
					var callback = SettingHandle.saveSSHSqlSetting;
					SettingHandle.uploadKey(callback);
				}
			}
		}else{
			SettingHandle.saveBaseSqlSetting();
		}
	});
}
var SettingGetAssertSetting = function(){
	//获取 system assert 列表
	$("#setting_tab").on("click",function(){
		SettingHandle.getPublicAssertList();
	});
	$("#div_public_assert_head").on("click",function(){
		SettingHandle.getPublicAssertList();
	});
}

var SettingFunctionDec = function(){
	//获取 system assert 列表
	$("#div_function_description").on("click",function(){
		$("#div_project_setting_no_data").show();
		$("#div_project_setting_env_deail").hide();
		$("#div_project_setting_assert").hide();
	});
}

var SettingHandle= (function () {
	var main = {}
	//设置已选择的item
	main.select_item = function(obj){
		var myt = $(obj).find("#env_name");
		SelectEnv["eId"] = Number($(myt).attr("eId"));
		SelectEnv["name"] = $(myt).html();
		SelectObj = obj;
		$("#ul_setting_env").find("li").removeClass("active");
		$(obj).addClass("active");
		SettingHandle.get_env_detail(SelectEnv["eId"]);
		
	}
	
	main.make_env_li = function(name = "",eId = ""){
		var li = '<li style="border-bottom: 1px solid #d5d8df" onclick="SettingHandle.select_item(this)"><a>\
					<i class="icon-sign-blank text-info"></i><myt id="env_name" eId='+eId+'>'+name+'</myt>\
			      </a></li>';
		return li;
	}
	
	//获取 env detail
	main.get_env_detail=function(eId){
		$("#div_project_setting_env_deail").show();
		$("#div_project_setting_assert").hide();
		$("#div_project_setting_no_data").hide();
		SettingHandle.get_global_values_list();
		SettingHandle.get_setting_sql();
	}


	main.getPublicAssertList=function(){
		$("#div_project_setting_env_deail").hide();
		$("#div_project_setting_assert").show();
		$("#div_project_setting_no_data").hide();
		
		var pId = ProjectInfo["pId"];
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var list = data.data;
				$("#tbody_system_assert_list").html("");
				for(var i=0;i<list.length;i++){
					var li = SettingHandle.make_assert_tr(list[i].name,list[i].key,list[i].value,list[i].type,list[i].sId);
					$("#tbody_system_assert_list").append(li);
				}
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/setting/assert/list","POST",{"pId":pId},callback);
	}
	
	main.make_assert_tr = function(name,key,value,type,sId){
		var typetext = "include";
		if(1==type){
			typetext = "exclude"
		}
		var tr ='<tr sId='+sId+'>\
					<td width="20%">'+name+'</td>\
					<td width="35%">'+key+'</td>\
					<td width="38%">'+value+'</td>\
					<td width="7%">'+typetext+'</td>\
					<td width="5%"><button type="button" class="btn btn-danger btn-xs" onclick="SettingHandle.deletePublicAssert(this)"><i class="icon-trash"></i></button></td>\
				</tr>';
		return tr;
	}
	
	//删除断言
	main.deletePublicAssert=function(obj){
		var tr = $(obj).parents("tr");
		TmpDeleteAssert = tr;
		var sId = Number($(tr).attr("sId"));
		
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$(TmpDeleteAssert).remove();
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/setting/delete/assert","POST",{"sId":sId},callback);
	}
	
	main.make_global_value_tr=function(name,value,type,gId){
		var tr ='<tr gId='+gId+'>\
				<td width="20%">'+name+'</td>\
				<td width="70%">'+value+'</td>\
				<td width="10%">'+type+'</td>\
				<td width="5%"><button type="button" class="btn btn-danger btn-xs" onclick="SettingHandle.delete_global_value(this)"><i class="icon-trash"></i></button></td>\
			</tr>';
		return tr;
	}
	//获取全局变量列表
	main.get_global_values_list = function(){
	    var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var list = data.data;
				$("#tbody_global_value_list").html("");
				for(var i=0;i<list.length;i++){
					var li = SettingHandle.make_global_value_tr(list[i].name,list[i].value,list[i].type,list[i].gId);
					$("#tbody_global_value_list").append(li);
				}
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
	    var data={};
	    data["eId"] = SelectEnv["eId"];
		$.requestJson("/setting/globalValue/list","POST",data,callback);
	}
	
	//删除全局变量
	main.delete_global_value=function(obj){
		var tr = $(obj).parents("tr");
		TmpDeleteGlobalValue = tr;
		var gId = Number($(tr).attr("gId"));
		
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$(TmpDeleteGlobalValue).remove();
			}else{
				$.fail_prompt("删除数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/setting/delete/globalValue","POST",{"gId":gId},callback);
	}
	
	main.get_setting_sql = function(){
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
//				$.success_prompt("保存成功");
				if(undefined==data.data.host){
					$("#select_setting_sql_type").val("mysql");
					$("#input_setting_sql_host").val("");
					$("#input_setting_sql_user").val("");
					$("#input_setting_sql_pwd").val("");
					$("#input_setting_sql_port").val("3306");
					$("#input_setting_sql_database").val("test");
					
					$("#input_setting_ssh_host").val("");
				    $("#input_setting_ssh_port").val("22");
				    $("#input_setting_ssh_user").val("");
				    $("#input_setting_ssh_psw").val("");
				    SettingHandle.showSSHModal('PassWord',0);
//				    var obj = document.getElementById('input_setting_file') ; 
//				    obj.outerHTML=obj.outerHTML;
				    
					SettingHandle.showSqlModal(0);
				}else{
					$("#select_setting_sql_type").val(data.data["type"]);
					$("#input_setting_sql_host").val(data.data["host"]);
					$("#input_setting_sql_user").val(data.data["user"]);
					$("#input_setting_sql_pwd").val(data.data["psw"]);
					$("#input_setting_sql_port").val(data.data["port"]);
					$("#input_setting_sql_database").val(data.data["database"]);
					
					if(""==data.data["sshHost"]){
						$("#input_setting_ssh_host").val("");
					    $("#input_setting_ssh_port").val("22");
					    $("#input_setting_ssh_user").val("");
					    $("#input_setting_ssh_psw").val("");
					    SettingHandle.showSSHModal('PassWord',0);
//					    var obj = document.getElementById('input_setting_file') ; 
//					    obj.outerHTML=obj.outerHTML;
						SettingHandle.showSqlModal(0);
					}else{
						SettingHandle.showSqlModal(1);
						$("#input_setting_ssh_host").val(data.data["sshHost"]);
					    $("#input_setting_ssh_port").val(data.data["sshPort"]);
					    $("#input_setting_ssh_user").val(data.data["sshUser"]);
						if(""==data.data["sshPsw"] || undefined == data.data["sshPsw"]){
							$("#input_setting_ssh_psw").val(data.data["sshKey"]);
							SettingHandle.showSSHModal('Key',1);
						}else{
							$("#input_setting_ssh_psw").val(data.data["sshPsw"]);
							SettingHandle.showSSHModal('PassWord',0);
						}
					}
				}
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
	    var data={};
	    data["eId"] = SelectEnv["eId"];
		$.requestJson("/setting/get/envSql","POST",data,callback);
	}
	//ssh 密码和key切换
	main.showSSHModal = function(text,t){
		$("#input_setting_ssh_psw").next().find('button').html(text + '&nbsp;<span class="caret"></span>');
		$("#input_setting_ssh_psw").next().find('button').attr("tabindex",t);
		if(0==t){
			$("#input_setting_ssh_psw").removeAttr("readonly");
			$("#input_setting_ssh_psw").css("cursor","text");
			$("#input_setting_ssh_psw").attr("type","password");
		}else{
			$("#input_setting_ssh_psw").attr("readonly","readonly");
			$("#input_setting_ssh_psw").css("cursor","pointer");
			$("#input_setting_ssh_psw").attr("type","text");
		}
		
		var p = $("#input_setting_file").parent();
		$("#input_setting_file").remove();//先删除，在添加
		$(p).append('<input type="file" id="input_setting_file" style="display:none" mce_style="display:none">');
	}
	//sql模式切换
	main.showSqlModal = function(modal){
		if(0==modal){
			$("#div_setting_ssh").hide();
			$("#span_setting_switch_modal").attr("value",0);
			$("#span_setting_switch_modal i").html("切换ssh模式");
		}else{
			$("#div_setting_ssh").show();
			$("#span_setting_switch_modal").attr("value",1);
			$("#span_setting_switch_modal i").html("切换基础模式");
		}
	}
	
	//上传
	main.uploadKey = function(callback1){
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				callback1();
			}else{
				$.fail_prompt("上传key失败："+data["message"],5000);
			}
		}
		var data = $("#input_setting_file")[0].files[0];
		$.upload("/setting/upload/sshKey",data,callback);
	}
	main.saveSSHSqlSetting = function(){
		var callback1=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
	    var data={};
	    data["pId"] = ProjectInfo["pId"];
	    data["eId"] = SelectEnv["eId"];
	    data["type"] = $("#select_setting_sql_type").val();
	    data["host"] = $("#input_setting_sql_host").val();
	    data["user"] = $("#input_setting_sql_user").val();
	    data["psw"] = $("#input_setting_sql_pwd").val();
	    data["port"] = $("#input_setting_sql_port").val();
	    data["database"] = $("#input_setting_sql_database").val();
	    
	    data["SSHHost"] = $("#input_setting_ssh_host").val();
	    data["SSHPort"] = $("#input_setting_ssh_port").val();
	    data["SSHUser"] = $("#input_setting_ssh_user").val();
		var sshtype = $("#input_setting_ssh_psw").next().find("button").attr("tabindex");
		if(0==sshtype||"0"==sshtype){
			data["SSHPsw"] = $("#input_setting_ssh_psw").val();
		}else{
			data["SSHKey"] = $("#input_setting_ssh_psw").val();
		}
		$.requestJson("/setting/save/envSql","POST",data,callback1);
	}
	main.saveBaseSqlSetting = function(){
		var callback=function(data){
		if(data["success"] == "true"|| data["success"] == true){
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
	    var data={};
	    data["pId"] = ProjectInfo["pId"];
	    data["eId"] = SelectEnv["eId"];
	    data["type"] = $("#select_setting_sql_type").val();
	    data["host"] = $("#input_setting_sql_host").val();
	    data["user"] = $("#input_setting_sql_user").val();
	    data["psw"] = $("#input_setting_sql_pwd").val();
	    data["port"] = $("#input_setting_sql_port").val();
	    data["database"] = $("#input_setting_sql_database").val();
		$.requestJson("/setting/save/envSql","POST",data,callback);
	}
	SettingFunctionDec()
	SettingAddEnvSetting();
	SettingEnvListIconSetting();
	SettingGetDataSetting();
	SettingEditEnvSetting();
	SettingDelEnvSetting();
	SettingAddAssertSetting();
	SettingGetGlobalValuesSetting();
	SettingSaveDatabaseSetting();
	SettingGetAssertSetting();
	
	return main;
}());