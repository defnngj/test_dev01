/**
 * author:anonymous
 */
var CaseTmp={
		
};
var CasePanelTmpHtml = "";
var CaseSelectRequirement = "";
var CaseSelectRequirePicker = "";

//用于设置面板的显示和隐藏的图标
var CasePartDisplaySetting = function(){
	$(".case_part_display_control").on('click',function(){
		var target = $(this).parent().next();
    	if($(target).hasClass("in")){
    		$(this).find("i").removeClass("icon-chevron-down");
    		$(this).find("i").addClass("icon-chevron-up");
    	}else{
    		$(this).find("i").removeClass("icon-chevron-up");
    		$(this).find("i").addClass("icon-chevron-down");
    	}
//    	PIBase.setStyle('textarea_case_parmas');
	});
}

var CaseAddSetting = function(){
	// modal表单验证定义
    $('#new_case_form').bootstrapValidator({
　　　　　message: '参数不能正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_new_case_name: {
                validators: {
                    notEmpty: {
                        message: '案例名不能为空'
                    }
                }
            },
            input_new_case_dec: {
                validators: {
                    notEmpty: {
                        message: '案例描述不能为空'
                    }
                }
            }
        }
    });
	$("#bt_create_case").on('click',function(){
		 // 获取表单对象
	    var bootstrapValidator = $("#new_case_form").data('bootstrapValidator');
	   // 手动触发验证
	    bootstrapValidator.validate();
	    if(bootstrapValidator.isValid()){
			var label = $("#input_new_case_label").val();
			var data = {};
			data["name"] = $("#input_new_case_name").val();
			data["dec"] = $("#input_new_case_dec").val();
			var nodes = $("#ztree").getSelectedNodes();
			if(0==nodes.length){
				return;
			}
			data["aId"] = GlobalData["select_api_info"].aId;
			data["pId"] = GlobalData["select_api_info"].pId;
			data["uId"] = GlobalData["select_api_info"].uId;
			if(""!=label && undefined!=label){
				data["label"] = label
			}
			var callback = function(data){
	 		   if(data["success"] == "true"|| data["success"] == true){
                    $("#caseModal").modal('toggle');
                    $("#ztree").addZTreeChildNode(data.data);
	 		   }else{
	 			   $.fail_prompt("查询数据失败："+data["message"],5000);
	 		   }
	         }
	 		$.requestJson("/case/add","POST",data,callback);
	    }
		
	});
}

var CaseSaveBaseSetting = function(){
	//保存基本信息
	$('#form_case_info').bootstrapValidator({
	　　　　　message: '参数不能正确！',
	        feedbackIcons: {
	　　　　　　　　validating: 'glyphicon glyphicon-refresh'
	　　　　　},
	        fields: {
	        	input_case_name: {
	                validators: {
	                    notEmpty: {
	                        message: '案例名不能为空'
	                    }
	                }
	            },
	            textarea_case_dec: {
	                validators: {
	                    notEmpty: {
	                        message: '案例描述不能为空'
	                    }
	                }
	            }
	        }
	    });
	$("#bt_case_save_base").on("click",function(){
		 // 获取表单对象
	    var bootstrapValidator = $("#form_case_info").data('bootstrapValidator');
	   // 手动触发验证
	    bootstrapValidator.validate();
	    if(bootstrapValidator.isValid()){
	    	var name = $("#input_case_name").val();
			var dec = $("#textarea_case_dec").val();
			var label = $("#input_case_label").val();
			var cId = GlobalData["select_case_info"].cId;
			
			var callback=function(data){
				if(data["success"] === "true"|| data["success"] === true){
					var name = $("#input_case_name").val();
					$("#ztree").updateCurrentZTreeNode(name);
				}else{
					$.fail_prompt("修改数据失败："+data["message"],5000);
				}
			}
			$.requestJson("/case/update/base","POST",{"cId":cId,"name":name,"dec":dec,"label":label},callback);
	    }
	});
}

var CaseSaveHeadSetting = function(){
	//保存头部
	$("#bt_case_save_header").on("click",function(){
		var trs = $("#tb_case_header").find("tr");
		var headerData = {};
		for(var i=0;i<trs.length;i++){
			var name = $(trs[i]).find("#case_head_name").val();
			var value = $(trs[i]).find("#case_head_value").val();
			headerData[name] = value;
		}
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
//				$.success_prompt("修改成功");
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		var headerDataStr = JSON.stringify(headerData);
		$.requestJson("/case/update/header","POST",{"cId":GlobalData["select_case_info"].cId,"headerData":headerDataStr},callback);
	});
}

var CaseSaveParmasSetting = function(){
	//保存 测试参数
	$("#bt_case_save_parmas").on("click",function(){
		var parmasData = {};
		var parmasDataStr = "";
		var dataType=1;
		
		if("json" == GlobalData["select_case_info"].apiParmasType){
			dataType=0;
			var str = $("#textarea_case_parmas").val();
			if(""==str){
				parmasDataStr="";
			}else{
				var obj={};
				try{
					obj=JSON.parse(str);
				}catch(e){
					$.fail_prompt("输入的数据不是json格式!!!",2000);
					return;
				}
				parmasDataStr = JSON.stringify(obj,null,8);
				$("#textarea_case_parmas").val(parmasDataStr);
//				PIBase.setStyle('textarea_case_parmas');
			}
		}else{
			var trs = $("#tb_case_parmas").find("tr");
			for(var i=0;i<trs.length;i++){
				var name = $(trs[i]).find("#case_parmas_name").val();
				var value = $(trs[i]).find("#case_parmas_value").val();
				parmasData[name] = value;
			}
			parmasDataStr = JSON.stringify(parmasData);
			dataType=1;
		};
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
//				$.success_prompt("修改成功");
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		}
		$.requestJson("/case/update/parmas","POST",{"cId":GlobalData["select_case_info"].cId,"parmasData":parmasDataStr,"dataType":dataType},callback);
	});
}

var CaseSavePickerSetting = function(){
	$("#bt_case_picker_add").on("click",function(){
		var tr = CaseHandle.make_picker_tr();
		$("#tb_case_value_picker").find("tbody").append(tr);
	});
	$("#bt_case_save_picker").on("click",function(){
		var trs = $("#tb_case_value_picker").find("tr");
		var picker = [];
		for(var i=0;i<trs.length;i++){
			var tmp = {}
			var name = $(trs[i]).find("#case_picker_name").val();
			var value = $(trs[i]).find("#case_picker_value").val();
			if(""==name||""==value){
				continue;
			}
			tmp["name"] = name;
			tmp["value"] = name;
			tmp["expression"] = value;
			picker.push(tmp);
		}
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
//				$.success_prompt("修改成功");
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		};
		$.requestJson("/case/update/picker","POST",{"cId":GlobalData["select_case_info"].cId,"valuePicker":picker},callback);
	});
}

var CaseAssertSetting = function(){
	$("#bt_case_add_sql_assert").on("click",function(){
		var tr = CaseHandle.make_sql_assert_tr();
    	$("#tb_case_sql_assert").find("tbody").append(tr);
	});
	$("#bt_case_add_assert").on("click",function(){
		var tr = CaseHandle.make_assert_tr();
    	$("#tb_case_other_assert").find("tbody").append(tr);
	});
	$("#bt_case_save_assert").on("click",function(){
		var trs = $("#tb_case_other_assert").find("tr");
		var otherAssert = [];
		for(var i=0;i<trs.length;i++){
			var name = $(trs[i]).find("#case_assert_name").val();
			var value = $(trs[i]).find("#case_assert_value").val();
			var caId = $(trs[i]).attr("caId");
			var type = $(trs[i]).find("#case_assert_type").attr("value");
			if(""==name){
				continue;
			}else{
				otherAssert.push({"name":name,"key":name,"value":value,"type":Number(type),"caId":Number(caId)});
			}
		};
		
		var preAssert = [];
		var input = $("#div_case_pre_assert").find("input");
		for(var i=0;i<input.length;i++){
			if($(input[i]).is(':checked')){
				preAssert.push(Number($(input[i]).attr("sId")));
			}
		};
		
		var sqlAssert = [];
		var sqltrs = $("#tb_case_sql_assert").find("tr");
		for(var i=0;i<sqltrs.length;i++){
			var name = $(sqltrs[i]).find("#input_case_sql_assert_name").val();
			var sql = $(sqltrs[i]).find("#input_case_sql_assert_sql").val();
			var assert = $(sqltrs[i]).find("#input_case_sql_assert_assert").val();
			var caId = $(trs[i]).attr("caId");
			if(""==name||""==sql||""==assert){
				continue;
			}else{
				sqlAssert.push({"name":name,"sql":sql,"sqlAssert":assert,"caId":Number(caId)});
			}
		};
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
//				$.success_prompt("修改成功");
				$("#tb_case_other_assert").find("tbody").html("");
			    var otherAssert=data.data.otherAssert
			    for(var i=0;i<otherAssert.length;i++){
			    	var tr = CaseHandle.make_assert_tr(otherAssert[i].name,otherAssert[i].value,otherAssert[i].type,otherAssert[i].caId);
			    	$("#tb_case_other_assert").find("tbody").append(tr);
			    }
			    
			    $("#tb_case_sql_assert").find("tbody").html("");
			    var sqlAssert=data.data.sqlAssert;
			    for(var i=0;i<sqlAssert.length;i++){
			    	var tr = CaseHandle.make_sql_assert_tr(sqlAssert[i].name,sqlAssert[i].sql,sqlAssert[i].sqlAssert,sqlAssert[i].caId);
			    	$("#tb_case_sql_assert").find("tbody").append(tr);
			    }
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		};
		$.requestJson("/case/update/assert","POST",{"cId":GlobalData["select_case_info"].cId,"sqlAssert":sqlAssert,"preAssert":preAssert,"otherAssert":otherAssert},callback);
	});
}

var CaseSqlSetting = function(){
	//前置条件,后置条件
	//修改pre sql
	$("#bt_case_save_pre_sql").on("click",function(){
		var pre_sql = $("#textarea_case_pre_sql").val();
		
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
//				$.success_prompt("修改成功");
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		};
		var data={};
		data["cId"]=GlobalData["select_case_info"].cId;
		data["preSql"]=pre_sql;
		$.requestJson("/case/update/preSql","POST",data,callback);
	})
	$("#bt_case_save_post_sql").on("click",function(){
		var post_sql = $("#textarea_case_post_sql").val();
		var data={};
		data["cId"]=GlobalData["select_case_info"].cId;
		data["postSql"]=post_sql;
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
//				$.success_prompt("修改成功");
			}else{
				$.fail_prompt("修改数据失败："+data["message"],5000);
			}
		};
		$.requestJson("/case/update/postSql","POST",data,callback);
	});
}

//////////////////////////////分界线

//显示text类型的信息
var CaseShowBase = function(data){
	$("#input_case_api_name").val(data.apiName);
    $("#input_case_api_method").val(data.apiMethod);
    $("#input_case_api_url").val(data.apiUrl);
    $("#input_case_name").val(data.name);
    $("#input_case_label").val(data.label);
    $("#textarea_case_dec").val(data.dec);
  //前置sql
	$("#textarea_case_pre_sql").val(data.preSql);
	//后置sql
	$("#textarea_case_post_sql").val(data.postSql);
}
//显示头部信息
var CaseShowHead = function(data){
	//头部设置
    $("#tb_case_header").find("tbody").html("");
    var headObj = {};
    var hasData = true;
    try{
    	headObj = JSON.parse(data.headerData);
    }catch(e){
//    	console.log(e);
    	hasData = false;
    }
    for(var i=0;i<data.apiHeader.length;i++){
    	var name = data.apiHeader[i].name;
    	var value = ""
    	if(hasData){
    		try{
    			value = headObj[name];
    		}catch(e){
    			value = "";
    		}
    	}
		tr = '<tr>\
				<td width="20%" style="padding:5px;">\
					<input type="text" readonly="readonly" style="color:black;cursor:text" value="'+name+'" class="form-control" id="case_head_name" placeholder="key"/>\
				</td>\
				<td width="80%"  style="padding:5px;" >\
					<input type="text" class="form-control"style="color:black" value="'+value+'" id="case_head_value" placeholder="value"/>\
				</td>\
			  </tr>';
		$("#tb_case_header").find("tbody").append(tr);
    };
}

var CaseShowParmas = function(data){
	//参数设置
    $("#tb_case_parmas").find("tbody").html("");
    var parmasObj = {};
    var phasData = true;
    try{
    	parmasObj = JSON.parse(data.parmasData);
    }catch(e){
    	phasData = false;
    }
    if("json" == data.apiParmasType){
    	$("#div_case_form_parmas").hide();
    	$("#div_case_json_parmas").show();
    	$("#textarea_case_parmas").val("");
    	if(0==data.dataType && phasData){//0代表存储的数据是json
    		$("#textarea_case_parmas").val(JSON.stringify(parmasObj, null, 8));
    	}else{
    		var json = $.form2json(data.apiParmas);
    		$("#textarea_case_parmas").val(JSON.stringify(json, null, 8)); 
    	}
//    	PIBase.setStyle('textarea_inter_parmas');
    }else{
	    $("#div_case_form_parmas").show();
	    $("#div_case_json_parmas").hide();
	    for(var i=0;i<data.apiParmas.length;i++){
    		var name = data.apiParmas[i].name;
    		var value = "";
    		if(phasData && 1==data.dataType){
    			value = parmasObj[name];
    			if(undefined==value){
    				value="";
    			}
    		}
	    	tr = '<tr>\
					<td width="20%" style="padding:5px;">\
						<input type="text" readonly="readonly" style="color:black;cursor:text" value="'+name+'" class="form-control" id="case_parmas_name" placeholder="key"/>\
					</td>\
					<td width="80%"  style="padding:5px;" >\
						<input type="text" class="form-control" style="color:black" value="'+value+'" id="case_parmas_value" placeholder="value"/>\
					</td>\
				  </tr>';
			$("#tb_case_parmas").find("tbody").append(tr);
	    };
    };
}

var CaseShowPublicAssert =function(data){
	//系统断言
    $("#div_case_pre_assert").html("");
    var preAssertObj=[];
    var newpreAssert = data.preAssert;

    for(var i=0;i<data.allPreAssert.length;i++){
    	tr_check = '<div style="margin-right:10px">\
				<label class="label_check" for="checkbox-01">\
                	<input name="" id="" style="color:black" type="checkbox" sId='+data.allPreAssert[i].sId+' checked /> '+data.allPreAssert[i].name+' \
                </label>\
			 </div>';
    	tr = '<div style="margin-right:10px">\
			<label class="label_check" for="checkbox-01">\
            	<input name="" id="" style="color:black" type="checkbox" sId='+data.allPreAssert[i].sId+' /> '+data.allPreAssert[i].name+' \
            </label>\
		 </div>';
    	var r = false;
    	for(var j=0;j<newpreAssert.length;j++){
    		if(newpreAssert[j]==data.allPreAssert[i].sId){
    			r=true;
    			break;
    		}
    	};
    	if(r){
    		$("#div_case_pre_assert").append(tr_check);
    	}else{
    		$("#div_case_pre_assert").append(tr);
    	};
    };
}

var CaseShowOtherAssert = function(data){
	//自定义断言
    $("#tb_case_other_assert").find("tbody").html("");
    var otherAssert=data.otherAssert
    for(var i=0;i<otherAssert.length;i++){
    	var tr = CaseHandle.make_assert_tr(otherAssert[i].name,otherAssert[i].value,otherAssert[i].type,otherAssert[i].caId);
    	$("#tb_case_other_assert").find("tbody").append(tr);
    }
}

var CaseShowSqlAssert = function(data){
	//sql断言
    $("#tb_case_sql_assert").find("tbody").html("");
    var sqlAssert=data.sqlAssert;
    for(var i=0;i<sqlAssert.length;i++){
    	var tr = CaseHandle.make_sql_assert_tr(sqlAssert[i].name,sqlAssert[i].sql,sqlAssert[i].sqlAssert,sqlAssert[i].caId);
    	$("#tb_case_sql_assert").find("tbody").append(tr);
    }
}

var CaseShowPicker = function(data){
	//变量提取
    $("#tb_case_value_picker").find("tbody").html("");
    for(var i=0;i<data.valuePicker.length;i++){
    	var tr = CaseHandle.make_picker_tr(data.valuePicker[i].name,data.valuePicker[i].expression);
	$("#tb_case_value_picker").find("tbody").append(tr);
    }
}

var CaseHandle= (function () {
	var main={};
//	PIBase.textAreaAutoHeight("textarea_case_parmas");
	$("#textarea_case_parmas").autoTextarea();

	//创建案例
	main.a_add_case = function(){
		var nodes = $("#ztree").getSelectedNodes();
		var node = nodes[0];
		if("api"==node.type){
			$("#caseModal").modal("show");
		}
	};
	main.get_case_detail = function(cId){
		var callback = function(datao){
 		   if(datao["success"] == "true"|| datao["success"] == true){
 			    GlobalData["select_case_info"] = datao.data;
 			    var data = datao.data;			    
 			    CaseShowBase(data);
 			    CaseShowHead(data);
 			    CaseShowParmas(data);			    
 			    CaseShowPublicAssert(data);
 			    CaseShowOtherAssert(data);
 			    CaseShowSqlAssert(data);
 			    CaseShowPicker(data);
//			    PIBase.setScroll();
 		   }else{
 			   $.fail_prompt("查询数据失败："+datao["message"],5000);
 		   }
         }
	 	$.requestJson("/case/detail","POST",{"cId":cId},callback);
	};

	//保存变量提取
	main.make_picker_tr = function(name="",value=""){
		var tr = '<tr>\
					<td width="40%" style="padding:5px;">\
						<input type="text" style="color:black" id="case_picker_name" class="form-control" value="'+name+'" placeholder="key"/>\
					</td>\
					<td width="57%"  style="padding:5px;" >\
						<input type="text" class="form-control" style="color:black" id="case_picker_value" value="'+value+'" placeholder="value"/>\
					</td>\
						<td width="3%"  style="padding:5px;">\
						<button class="btn btn-danger" type="button" onclick="$(this).parent().parent().remove()"><i class="icon-trash "></i></button>\
					</td>\
				</tr>';
		return tr;
	}
	
	//断言设置
	main.make_sql_assert_tr = function(name="",value="",assert="",caId=-1){
		tr = '<tr caId='+caId+'>\
				<td width="25%" style="padding: 5px;">\
					<input type="text" id="input_case_sql_assert_name" style="color:black" class="form-control" placeholder="name" value="'+name+'" /></td>\
				<td width="52%" style="padding: 5px;">\
					<input type="text" id="input_case_sql_assert_sql" style="color:black" class="form-control" placeholder="请输入sql语句" value="'+value+'"/>\
				</td>\
				<td width="20%" style="padding: 5px;">\
					<input type="text" id="input_case_sql_assert_assert" style="color:black" class="form-control" value="'+assert+'" placeholder="格式=0,<0,>0,<=0,>=0"/>\
				</td>\
				<td width="4%" style="padding: 5px;">\
					<button type="button" class="btn btn-danger" onclick="$(this).parent().parent().remove()">\
						<i class="icon-trash"></i>\
					</button>\
				</td>\
			</tr>';
		return tr;
	}
	
	main.ul_assert_click=function(obj){
		var value = $(obj).attr("value");
		var text = ""
		if(0==value){
			text = 'include<span class="caret"></span>';
		}else{
			text = 'exclude<span class="caret"></span>';
		}
		$(obj).parent().prev().html(text);
		$(obj).parent().prev().attr("value",value);
//		PIBase.setScroll();
	}
	
	main.make_assert_tr = function(name="",value="",t=0,caId=-1){
		var type="include";
		if(t==1){
			type = "exclude";
		}
		tr = '<tr caId='+caId+'>\
			<td width="40%" style="padding:5px;">\
				<input type="text" class="form-control" id="case_assert_name" style="color:black" placeholder="key"  value="'+name+'"/>\
			</td>\
			<td width="47%"  style="padding:5px;" >\
				<input type="text" class="form-control" id="case_assert_value" style="color:black" placeholder="value"  value="'+value+'"/>\
			</td>\
			<td width="9%" style="padding:5px;">\
				<div class="btn-group" style="width: 100%">\
					<button type="button" class="btn btn-white dropdown-toggle" id="case_assert_type" value='+t+' data-toggle="dropdown">'+type+'<span class="caret"></span>\
					</button>\
					<ul class="dropdown-menu">\
						<li onclick="CaseHandle.ul_assert_click(this)" value=0><a>include</a></li>\
						<li onclick="CaseHandle.ul_assert_click(this)" value=1><a>exclude</a></li>\
					</ul>\
				</div>\
			</td>\
			<td width="4%" style="padding:5px;">\
				<button type="button" class="btn btn-danger" onclick="$(this).parent().parent().remove()"><i class="icon-trash"></i></button>\
			</td>\
		</tr>';
		return tr;
	}
	
	//delete case
	main.a_delete_case = function(){
		var nodes = $("#ztree").getSelectedNodes();
		if(nodes.length==0){
			return;
		}
		var node = nodes[0];
		if(node.type!="case"){
			return;
		}else{
			swal({ 
	   	        title: "您确定要删除案例吗？",  
	   	        text: "您确定要删除这个案例吗？",  
	   	        type: "warning", 
	   	        showCancelButton: true, 
	   	        closeOnConfirm: true, 
	   	        confirmButtonText: "是的，我要删除", 
	   	        confirmButtonColor: "#ec6c62" 
	   	    }, function() {
	   	    	var callback = function(data){
	     		  if(data["success"] == "true"|| data["success"] == true){
	     			 $("#ztree").removeNode(node);
	         		 $("#section_api_detail").hide();
	         		 $("#section_case_detail").hide();
	         		 $("#section_api_detail_nodata").show();
	     		   }else{
	     			   $.fail_prompt("执行失败："+data["message"],5000);
	     		   }
	        	 }
	     	   $.requestJson("/case/delete","POST",{"cId":node.cId},callback);
	   	    }); 
		}
	};
	
	//copy case
	main.copy_case = function(){
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			   $("#ztree").addZTreeBrotherNode(data.data);
 		   }else{
 			   $.fail_prompt("copy接口失败："+data["message"],5000);
 		   }
         }
 		$.requestJson("/case/copy","POST",{"cId":GlobalData["select_case_info"].cId},callback);
	};
	
	CasePartDisplaySetting();
	CaseAddSetting();
	CaseSaveBaseSetting();
	CaseSaveHeadSetting();
	CaseSaveParmasSetting();
	CaseSavePickerSetting();
	CaseAssertSetting();
	CaseSqlSetting();

	return main;
}());
