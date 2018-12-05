/**
 * author:anonymous
 */
var SelectSuite={
};
var SelectSuiteDetail={//选择的suiteDetail
};
var PanelTmpHtml = "";
var SelectRequirement = {};
var SelectRequirePicker = {};

var SuiteAddSetting = function(){
	// modal表单验证定义,添加suite
    $('#new_suite_form').bootstrapValidator({
　　　　　message: '参数不正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_new_suite_name: {
                validators: {
                    notEmpty: {
                        message: '名称不能为空'
                    }
                }
            },
            input_new_suite_dec: {
                validators: {
                    notEmpty: {
                        message: '描述不能为空'
                    }
                }
            }
        }
    });
  //创建套件
	$("#bt_create_suite").on("click",function(){
		var bootstrapValidator = $("#new_suite_form").data('bootstrapValidator');
	    // 手动触发验证
	    bootstrapValidator.validate();
	    if(!bootstrapValidator.isValid()){
	    	return;
	    }
		var name = $("#input_new_suite_name").val();
		var dec = $("#input_new_suite_dec").val();
		var pId = ProjectInfo["pId"];
		var uId = UserInfo["userId"];
		if(""==name||""==dec){
			return;
		}
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
              $("#suiteModal").modal('toggle');
//              $.success_prompt("新建成功",2000);
              var tr = SuiteHandle.make_suite_tr(data.data.name,data.data.suId,data.data.dec);
              $("#div_suite_list").append(tr);
 		   }else{
 			   $.fail_prompt("新建失败："+data["message"],5000);
 		   }
	    }
		var data={};
		data["name"] = name;
		data["dec"]=dec;
		data["pId"] = pId;
		data["uId"] = uId;
	 	$.requestJson("/suite/add","POST",data,callback);
	});
}

var SuiteUpdateSetting = function(){
	 // modal表单验证定义,添加suite
    $('#update_suite_form').bootstrapValidator({
　　　　　message: '参数不正确！',
        feedbackIcons: {
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	input_update_suite_name: {
                validators: {
                    notEmpty: {
                        message: '名称不能为空'
                    }
                }
            },
            input_update_suite_dec: {
                validators: {
                    notEmpty: {
                        message: '描述不能为空'
                    }
                }
            }
        }
    });
	$("#bt_update_suite").on('click',function(){
		var name=$("#input_update_suite_name").val();
		var dec=$("#input_update_suite_dec").val();
		var suId=SelectSuite.suId;
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			  var a = $("#div_suite_list").find("a[suId="+data.data.suId+"]")
 			  $(a).attr("dec",data.data.dec);
 			  $(a).attr("text",data.data.name);
 			  $(a).find("label").html($.textlength_settting(data.data.name,15));
 			  $("#suiteUpdateModal").modal("toggle");
 		   }else{
 			   $.fail_prompt("更新失败："+data["message"],5000);
 		   }
		}
	 	$.requestJson("/suite/update/base","POST",{"suId":suId,"name":name,"dec":dec},callback);
	});
}

var SuiteMakeSuiteProfile = function(data){
	var base = $("#div_suite_case_base_model").html();
	var pre = $("#div_suite_case_pre_model").html();
	var head = $("#div_suite_case_head_model").html();
	var parmas = $("#div_suite_case_parmas_model").html();
	var picker = $("#div_suite_case_picker_model").html();
	var response = $("#div_suite_case_response_model").html();
	var post = $("#div_suite_case_post_model").html();
	var div ='<div class="panel panel-default panel-py-mark" ready_delete="no" cId='+data.cId+'>\
				<div class="panel-heading" style="background: #edeef5">\
				   <div style="display: flex; justify-content: space-between">\
					  <div>\
						<h4 class="panel-title">\
							<a data-toggle="collapse" data-parent="#accordion"\
								style="vertical-align: middle;" href="#collapse'+data.cId+'">\
								'+data.name+' <span class="badge bg-info">'+data.apiMethod+'</span>\
							</a>\
						</h4>\
					  </div>\
					  <div style="margin-top:-3px">\
						<span class="label label-info" style="cursor: pointer;" onclick="SuiteHandle.suite_turn_up(this)"><i class="icon-long-arrow-up"></i></span>\
						<span class="label label-info" style="cursor: pointer;" onclick="SuiteHandle.suite_turn_down(this)"><i class="icon-long-arrow-down"></i></span>\
						<label><span class="label label-danger" style="cursor: pointer;" onclick="SuiteHandle.delete_case(this)"><i class="icon-trash"></i></span></label>\
					  </div>\
					</div>\
				</div>\
				<div id="collapse'+data.cId+'" cId='+data.cId+' class="panel-collapse collapse panel-collapse-mark">\
					<div class="panel-body" id="div_suite_panel_body"> \
						<ul id="myTab" class="nav nav-tabs">\
							<li class="active"><a href="#tab_base'+data.cId+'" data-toggle="tab"> 基本信息</a></li>\
							<li><a href="#tab_pre'+data.cId+'" data-toggle="tab"> 前置条件</a></li>\
							<li><a href="#tab_head'+data.cId+'" data-toggle="tab">头部设置</a></li>\
							<li><a href="#tab_parmas'+data.cId+'" data-toggle="tab">参数设置</a></li>\
							<li><a href="#tab_picker'+data.cId+'" data-toggle="tab">参数提取</a></li>\
							<li><a href="#tab_response'+data.cId+'" data-toggle="tab">响应断言</a></li>\
							<li><a href="#tab_post'+data.cId+'" data-toggle="tab">后置条件</a></li>\
						</ul>\
						<div id="myTabContent" class="tab-content">\
							<div class="tab-pane fade in active" id="tab_base'+data.cId+'">'+base+'</div>\
							<div class="tab-pane fade" id="tab_pre'+data.cId+'">'+pre+'</div>\
							<div class="tab-pane fade" id="tab_head'+data.cId+'">'+head+'</div>\
							<div class="tab-pane fade" id="tab_parmas'+data.cId+'">'+parmas+'</div>\
							<div class="tab-pane fade" id="tab_picker'+data.cId+'">'+picker+'</div>\
							<div class="tab-pane fade" id="tab_response'+data.cId+'">'+response+'</div>\
							<div class="tab-pane fade" id="tab_post'+data.cId+'">'+post+'</div>\
						</div>\
					</div>\
				</div>\
			</div>';
	   return div;
}

var SuiteShowCaseBase = function(obj,data){
	//基础信息
	$(obj).find("#input_suite_case_api_name").val(data.apiName);
	$(obj).find("#input_suite_case_api_method").val(data.apiMethod);
	$(obj).find("#input_suite_case_api_url").val(data.apiUrl);
	$(obj).find("#input_suite_case_name").val(data.name);
	$(obj).find("#input_suite_case_label").val(data.label);
	$(obj).find("#textarea_suite_case_dec").val(data.dec);
	//前置后置
	$(obj).find("#textarea_suite_pre_sql").val(data.preSql);
	$(obj).find("#textarea_suite_case_post_sql").val(data.postSql);
}


var SuiteShowCaseHead = function(obj,caseDeatail){
	var headtbody = $(obj).find("#tb_suite_case_header").find("tbody");
	$(headtbody).html("");
    var headObj = {};
    try{
    	headObj = JSON.parse(caseDeatail.headerData);
    }catch(e){}
    for(var i=0;i<caseDeatail.apiHeader.length;i++){
    	var name = caseDeatail.apiHeader[i].name;
    	var value = headObj[name];
    	if(undefined == value){
    		value="";
    	}
    	tr = '<tr>\
				<td width="30%" style="color:black;">'+name+'</td>\
				<td width="70%" style="color:black;">'+value+'</td>\
			  </tr>';
    	$(headtbody).append(tr);
    };
}

var SuiteShowCaseParmas= function(obj,caseDeatail){
	var parmastbody = $(obj).find("#tb_suite_case_parmas").find("tbody");
    $(parmastbody).html("");
    var parmasObj = {};
    var phasData = true;
    try{
    	parmasObj = JSON.parse(caseDeatail.parmasData);
    }catch(e){
    	phasData = false;
    }
    if("json" == caseDeatail.apiParmasType){
    	
    	$(obj).find("#div_suite_case_parmas_model_form").hide();
    	$(obj).find("#div_suite_case_parmas_model_json").show();
    	if(0==caseDeatail.dataType && phasData){//0代表存储的数据是json
    		$(obj).find("#textarea_suite_case_parmas").val(JSON.stringify(parmasObj, null, 8));
    	}else{
    		var json = $.form2json(caseDeatail.apiParmas);
    		$(obj).find("#textarea_suite_case_parmas").val(JSON.stringify(json, null, 8)); 
    	}
//    	PIBase.setStyle('textarea_inter_parmas');
    }else{
    	$(obj).find("#div_suite_case_parmas_model_form").show();
    	$(obj).find("#div_suite_case_parmas_model_json").hide();
	    for(var i=0;i<caseDeatail.apiParmas.length;i++){
    		var name = caseDeatail.apiParmas[i].name;
    		var value = "";
    		if(phasData && 1==caseDeatail.dataType){
    			value = parmasObj[name];
    			if(undefined==value){
    				value="";
    			}
    		}
	    	tr = '<tr>\
					<td width="30%" style="color:black">'+name+'</td>\
					<td width="70%"  style="color:black" >'+value+'</td>\
				  </tr>';
	    	$(parmastbody).append(tr);
	    };
    };
}

var SuiteShowCasePicker = function(obj,caseDeatail){
	var pickertbody = $(obj).find("#tb_suite_case_value_picker").find("tbody");
	$(pickertbody).html("");
    for(var i=0;i<caseDeatail.valuePicker.length;i++){
    	tr = '<tr>\
				<td width="30%" style="color:black;">'+caseDeatail.valuePicker[i].name+'</td>\
				<td width="70%" style="color:black;">'+caseDeatail.valuePicker[i].expression+'</td>\
			  </tr>';
    	$(pickertbody).append(tr);
    };
}

var SuiteSHowCaseAssert = function(obj,caseDeatail){
	var preastbody = $(obj).find("#tb_suite_case_pre_assert").find("tbody");
	$(preastbody).html("");
	var newpreAssert = caseDeatail.preAssert;
    for(var i=0;i<caseDeatail.allPreAssert.length;i++){
    	tr = '<tr>\
				<td width="30%" style="color:black;">'+caseDeatail.allPreAssert[i].name+'</td>\
			  </tr>';
    	var r = false;
    	for(var j=0;j<newpreAssert.length;j++){
    		if(newpreAssert[j]==caseDeatail.allPreAssert[i].sId){
    			r=true;
    			break;
    		}
    	};
    	if(r){
    		$(preastbody).append(tr);
    	}
    };
    
    var otherasstbody = $(obj).find("#tb_suite_case_other_assert").find("tbody");
	$(otherasstbody).html("");
    var otherAssert=caseDeatail.otherAssert;
    for(var i=0;i<otherAssert.length;i++){
    	var type ="include";
    	if(1==otherAssert[i].type){
    		type ="exclude";
    	}
    	var tr = '<tr>\
					<td style="color:black" width=40%>'+otherAssert[i].name+'</td>\
					<td style="color:black" width=50%>'+otherAssert[i].value+'</td>\
					<td style="color:black" width=10%>'+type+'</td>\
				 </tr>';
    	$(otherasstbody).append(tr);
    }
    
    var sqlasstbody = $(obj).find("#tb_suite_case_sql_assert").find("tbody");
	$(sqlasstbody).html("");
    var sqlAssert=caseDeatail.sqlAssert;
    for(var i=0;i<sqlAssert.length;i++){
    	var tr = '<tr>\
			<td width="25%" style="padding: 5px;">'+sqlAssert[i].name+'</td>\
			<td width="55%" style="padding: 5px;">'+sqlAssert[i].sql+'</td>\
			<td width="20%" style="padding: 5px;">'+sqlAssert[i].sqlAssert+'</td>\
		</tr>';
    	$(sqlasstbody).append(tr);
    }
}

var MakeRequireDivHtml = function(rId,caseNme){
	var div = '<div class="panel panel-success div_requirement_class" rId="'+rId+'">\
	<div class="panel-heading">\
		<div style="display: flex; justify-content: space-between">\
			<div>\
				<h4 class="panel-title">\
					<a data-toggle="collapse" data-parent="#panel_suite_requirement" href="#requirepicker'+rId+'">'+caseNme+'</a>\
				</h4>\
			</div>\
			<div style="margin-top: -3px">\
				<button type="button" class="btn btn-danger btn-xs"><i class="icon-trash" onclick="SuiteHandle.delete_requirement(this)"></i></button>\
			</div>\
		</div>\
	</div>\
	<div id="requirepicker'+rId+'" class="panel-collapse collapse requirementclass">\
		<div class="panel-body">\
			<label>变量提取:</label>\
			<form role="form">\
                <div class="form-group">\
                    <input type="text" style="color:black" class="form-control" id="input_suite_requirement_picker_name" placeholder="变量名">\
                </div>\
                <div class="form-group" style="margin-top:-10px">\
                    <input type="text" style="color:black" class="form-control" id="input_suite_requirement_picker_rule" placeholder="规则">\
                </div>\
                <button style="margin-top:-10px" type="button" class="btn btn-info btn-sm" onclick="SuiteHandle.bt_add_require_picker(this)">添加</button>\
            </form>\
			<table class="table table-hover table-bordered" style="margin-top:20px">\
				<tbody>\
				</tbody>\
			</table>\
			<div >\
				<div class="col-lg-12" style="background:#d8eecf;margin-bottom:10px;border-radius: 5px;;padding:10px">\
					说明：目前只能接受json格式的响应的变量提取，例如一个响应为{code:xxx,result:{success:true,otherdata:xx}},要想提取code，只需要输入code即可，如果需要提取success\
					则需要输入result.success。\
				</div>\
			</div>\
		</div>\
	</div>\
</div>';
return div;
}
//前置条件
var SuitePreRequireSetting = function(){
	//前置条件
//	PIBase.textAreaAutoHeight("textarea_suite_pre");
	$("#textarea_suite_pre").autoTextarea();
	$("#bt_suite_save_pre").on("click",function(){
		var suId=SelectSuite.suId;
		if(undefined==suId){
			return;
		}
		var pre = $("#textarea_suite_pre").val();
		var callback = function(data){
  		   if(data["success"] == "true"|| data["success"] == true){
  		   }else{
  			   $.fail_prompt("获取模块数据失败："+data["message"],5000);
  		   }
    	}
		$.requestJson("/suite/update/pre","POST",{"suId":suId,"preSql":pre},callback);
	});
	$('#div_pre_sql').on('shown.bs.collapse', function () {
//		PIBase.setStyle('textarea_suite_pre');
	});
	//requirement,添加 
	$("#bt_suite_add_require").on("click",function(){
		$("#selectCaseModal").modal("show");
		SuiteHandle.add_require_tree();
	});
}

//后置条件
var SuitePostRequireSetting = function(){
	$('#div_post_sql').on('shown.bs.collapse', function () {
//		PIBase.setStyle('textarea_suite_post');
	});
//	PIBase.textAreaAutoHeight("textarea_suite_post");
	$("#textarea_suite_post").autoTextarea();
	$("#bt_suite_save_post").on("click",function(){
		var suId=SelectSuite.suId;
		if(undefined==suId){
			return;
		}
		var post = $("#textarea_suite_post").val();
		var callback = function(data){
  		   if(data["success"] == "true"|| data["success"] == true){
//  			 PIBase.success_prompt("保存成功",2000);
  		   }else{
  			   $.fail_prompt("获取模块数据失败："+data["message"],5000);
  		   }
    	}
		$.requestJson("/suite/update/post","POST",{"suId":suId,"postSql":post},callback);
	});
}

//添加案例
var SuiteAddCaseSetting = function(){
	//添加案例
	$("#bt_suite_add_cases").on("click",function(){
		$("#selectCaseModal").modal("show");
		SuiteHandle.add_cases_tree();
	});
}

var SuiteMakeCaseTree = function(data){
	var defaluts = {
	        dataList: data,
	        setting:{
	        	view: {
    				dblClickExpand: false,
    				showTitle:true, //是否显示节点title信息提示 默认为true
    			},
    			data: {
    	        	simpleData: {
    	        		enable: true
    	        	},
    	    		key: {
    	    			title: "title",
    	    			name: "name"
    	    		}
    	    	},
    	    	check: {
    	    		enable: true
    	    	}
	        }
	};
	$("#selectCaseTree").initZTree(defaluts);
}

var SuiteHandle= (function () {
	var main = {};

	main.make_suite_tr=function(name,suId,dec){
		var tr = '<a class="list-group-item" suId='+suId+' dec="'+dec+'" text="'+name+'" onclick="SuiteHandle.get_suite_detail(this)">\
					<label>'+$.textlength_settting(name,15)+'</label>\
					<span class="badge badger-info" onclick="SuiteHandle.update_suite_base(this)">\
						<i class="icon-edit-sign"></i>\
					</span>\
					<span class="badge badger-danger" onclick="SuiteHandle.delete_suite(this)">\
						<i class="icon-trash"></i>\
					</span>\
				 </a>';
		return tr;
	};

	//更新suite base
	main.update_suite_base=function(obj){
		$("#input_update_suite_name").val($(obj).parent().attr("text"));
		$("#input_update_suite_dec").val($(obj).parent().attr("dec"));
		$("#suiteUpdateModal").modal("show");
	}

	//删除suite
	main.delete_suite=function(obj){
		swal({
   	        title: "您确定要删除测试套件吗？",  
   	        text: "您确定要删除测试套件吗？",  
   	        type: "warning", 
   	        showCancelButton: true, 
   	        closeOnConfirm: true, 
   	        confirmButtonText: "是的，我要删除", 
   	        confirmButtonColor: "#ec6c62" 
   	    }, function() {
   	    	var callback = function(data){
   	 		   if(data["success"] == "true"|| data["success"] == true){
   	              $(obj).parent().remove();
   	              SuiteHandle.no_data("show");
   	 		   }else{
   	 			   $.fail_prompt("新建失败："+data["message"],5000);
   	 		   }
   			}
   			var data={};
   			data["suId"] = SelectSuite.suId;
   		 	$.requestJson("/suite/delete","POST",data,callback);
   	    }); 
		
	}
	//获取suite list
	main.get_suite_list=function(){
		$("#div_suite_list").html("");
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			    list = data.data;
 			    if(0==list.length){
// 			    	$("#div_suite_list").append('<div style="text-align:center">无数据</div>');
 			    }else{
 			    	for(var i=0;i<list.length;i++){
 						var tr = SuiteHandle.make_suite_tr(list[i].name,list[i].suId,list[i].dec);
 						$("#div_suite_list").append(tr);
 					}
 			    }
 		   }else{
 			   $.fail_prompt("新建失败："+data["message"],5000);
 		   }
		}
	 	$.requestJson("/suite/list","POST",{"pId":ProjectInfo.pId},callback);
	}
	
	main.no_data = function(model){
		if("show"==model){
			$("#div_suite_detail_nodata").show();
			$("#div_suite_detail").hide();
		}else{
			$("#div_suite_detail_nodata").hide();
			$("#div_suite_detail").show();
		}
	}
	
	//获取suite的详情
	main.get_suite_detail=function(obj){
		$("#div_suite_list").find("a").removeClass("active");
		$(obj).addClass("active");
		SelectSuite.suId=Number($(obj).attr("suId"));
		SelectSuite.name=$(obj).find("label").html();
		SelectSuite.dec=$(obj).attr("dec");
		
		SuiteHandle.no_data("hide");
		
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			   SelectSuiteDetail = data.data;
 			   var suite = data.data;

 			   $("#textarea_suite_pre").val(suite.preSql);
 			   $("#textarea_suite_post").val(suite.postSql);
 			   
 			   $("#accordion").html("");
 			   for(var i=0;i<suite.cases.length;i++){
 				   var div = SuiteHandle.make_suite_profile_panel(suite.cases[i]);
				   $("#accordion").append(div);
 			   }
 			   
			   $("#panel_suite_requirement").html("");//前置条件
			   for(var i=0;i<suite.preRequirement.length;i++){
				   var div = SuiteHandle.make_require_div(suite.preRequirement[i].rId,suite.preRequirement[i].name);
				   $("#panel_suite_requirement").append(div);
			   }
 			   
 			   SuiteHandle.event_collapse_show();
 			   SuiteHandle.event_show_require_picker();
 		   }else{
 			   //$.fail_prompt("新建失败："+data["message"],5000);
 		   }
		}
	 	$.requestJson("/suite/detail","POST",{"suId":SelectSuite.suId},callback);
	}
	
	//构造case 预览的panel
	main.make_suite_profile_panel = function(data){
		return SuiteMakeSuiteProfile(data);
	}
	//case 详细显示的时间
	main.event_collapse_show=function(){
		$(".panel-collapse-mark").on('show.bs.collapse', function () {
			
			var cId = Number($(this).attr("cId"));
			var caseDeatail = {};
			for(var i=0;i<SelectSuiteDetail.cases.length;i++){
				if(cId==SelectSuiteDetail.cases[i].cId){
					//console.log(SelectSuiteDetail.cases[i]);
					caseDeatail = SelectSuiteDetail.cases[i];
					break
				}
			}
			SuiteShowCaseBase(this,caseDeatail);
			SuiteShowCaseHead(this,caseDeatail);
			SuiteShowCaseParmas(this,caseDeatail);
			SuiteShowCasePicker(this,caseDeatail);
			SuiteSHowCaseAssert(this,caseDeatail);

		    $(".panel-collapse-mark").on('shown.bs.collapse', function(){
				$(".autotext").autoTextarea({maxHeight:22000});
				$(".autotext").setTextareaHeight({maxHeight:2200});
			})
		});
	}
	
	//案例树形结构
	main.makeCaseTree=function(data){ 	
		SuiteMakeCaseTree(data);
    	$("#bt_confirm_select_case").attr('onclick','').unbind('click').click(function(){
    		var selectCases = $("#selectCaseTree").getCheckNodes();
    		var casesId = [];
    		for(var i=0;i<SelectSuiteDetail.cases.length;i++){
    			casesId.push(SelectSuiteDetail.cases[i].cId);
    		}
    		for(var i=0;i<selectCases.length;i++){
    			if("case"==selectCases[i].type){
    				casesId.push(selectCases[i].cId);
    			}
    		}
    		var callback = function(data){
			   if(data["success"] == "true"|| data["success"] == true){
				   var cases = data.data.cases;
				   SelectSuiteDetail.cases = cases;
				   
				   $("#accordion").html("");
	 			   for(var i=0;i<cases.length;i++){
	 				   var div = SuiteHandle.make_suite_profile_panel(cases[i]);
					   $("#accordion").append(div);
	 			   }
	 			   SuiteHandle.event_collapse_show();
	 			  $("#selectCaseModal").modal("hide");
			   }else{
				   $.fail_prompt("设置案例数据失败："+data["message"],5000);
			   }
			}
			$.requestJson("/suite/update/cases","POST",{"casesId":JSON.stringify(casesId),"suId":SelectSuite.suId},callback);
    	});
	}
	
	main.add_cases_tree = function(){
		var callback = function(data){
		   if(data["success"] == "true"|| data["success"] == true){
			   SuiteHandle.makeCaseTree(data.data.data);
		   }else{
			   $.fail_prompt("获取模块数据失败："+data["message"],5000);
		   }
		}
		$.requestJson("/module/lists","POST",{"pId":ApiHandle.pId},callback);
	}
	
	main.add_require_tree = function(){
		var callback = function(data){
		   if(data["success"] == "true"|| data["success"] == true){
			   SuiteHandle.makeRequireTree(data.data.data);
		   }else{
			   $.fail_prompt("获取模块数据失败："+data["message"],5000);
		   }
		}
		$.requestJson("/module/lists","POST",{"pId":ApiHandle.pId},callback);
	}
	
	main.makeRequireTree=function(data){
		SuiteMakeCaseTree(data);
    	$("#bt_confirm_select_case").attr('onclick','').unbind('click').click(function(){
    		var selectCases = $("#selectCaseTree").getCheckNodes();
    		var cases = []
    		for(var i=0;i<selectCases.length;i++){
    			if("case"==selectCases[i].type){
    				cases.push({"cId":selectCases[i].cId,"type":"pre"});
    			}
    		}
    		var callback = function(data){
			   if(data["success"] == "true"|| data["success"] == true){
				   var suId = SelectSuite.suId;
				   var rIds = [];
				   var divs = $("#panel_suite_requirement").children();
				   for(var i=0;i<divs.length;i++){
					   rId = $(divs[i]).attr("rId");
					   rIds.push(Number(rId));
				   }
				   for(var i=0;i<data.data.requirements.length;i++){
					   rIds.push(data.data.requirements[i].rId);
				   }
				   var callback = function(data){
					   if(data["success"] == "true"|| data["success"] == true){
						   $("#selectCaseModal").modal("hide");
						   $("#panel_suite_requirement").html("");
						   for(var i=0;i<data.data.preRequirement.length;i++){
							   var div = SuiteHandle.make_require_div(data.data.preRequirement[i].rId,data.data.preRequirement[i].name);
							   $("#panel_suite_requirement").append(div);
							   SuiteHandle.event_show_require_picker();
						   }
					   }else{
						   $.fail_prompt("新建前置条件失败："+data["message"],5000);
					   }
					}
					$.requestJson("/suite/update/requirement","POST",{"suId":suId,"rIds":rIds},callback);//然后就修改requireid
					
			   }else{
				   $.fail_prompt("新建前置条件失败："+data["message"],5000);
			   }
			}
			$.requestJson("/requirement/add","POST",{"cases":cases},callback);//先创建requirement
    	});
	}
	main.make_require_div = function(rId,caseName){
		return MakeRequireDivHtml(rId,caseName);
	}
	
	//requirement,删除
	main.delete_requirement = function(obj){
		var div = $(obj).parents(".div_requirement_class");
		var rId = Number($(div).attr("rId"));
		$(div).remove();
		PanelTmpHtml = $("#panel_suite_requirement").html();
		var callback = function(data){
  		   if(data["success"] == "true"|| data["success"] == true){
  			   var suId = SelectSuite.suId;
			   var rIds = [];
			   var divs = $("#panel_suite_requirement").children();
			   for(var i=0;i<divs.length;i++){
				   rId = $(divs[i]).attr("rId");
				   rIds.push(Number(rId));
			   }
			   var callback = function(data){
				   if(data["success"] == "true"|| data["success"] == true){
					   $("#selectCaseModal").modal("hide");
					   $("#panel_suite_requirement").html("");
					   for(var i=0;i<data.data.preRequirement.length;i++){
						   var div = SuiteHandle.make_require_div(data.data.preRequirement[i].rId,data.data.preRequirement[i].name);
						   $("#panel_suite_requirement").append(div);
					   }
					   SuiteHandle.event_show_require_picker();
				   }else{
					   $("#panel_suite_requirement").html(PanelTmpHtml);
					   $.fail_prompt("删除前置条件失败："+data["message"],5000);
				   }
				}
				$.requestJson("/suite/update/requirement","POST",{"suId":suId,"rIds":rIds},callback);//然后就修改requireid
  		   }else{
  			   $("#panel_suite_requirement").html(PanelTmpHtml);
  			   $.fail_prompt("删除前置条件失败："+data["message"],5000);
  		   }
    	}
		$.requestJson("/requirement/delete","POST",{"rId":rId},callback);
	}
	//给require添加picker
	main.bt_add_require_picker=function(obj){
		var form = $(obj).parent();
		var name = $(form).find("#input_suite_requirement_picker_name").val();
		var expression = $(form).find("#input_suite_requirement_picker_rule").val();
		if(""==name||""==expression){
			return;
		}
		var data = {}
		var div = $(form).parent().parent().parent();
		SelectRequirement = div;
		var rId = Number($(div).attr("rId"));
		data["rId"] = rId;
		data["name"] = name;
		data["value"] = name;
		data["expression"] = expression;
		
		var callback = function(data){
		   if(data["success"] == "true"|| data["success"] == true){
			   var tbody = $(SelectRequirement).find("tbody");
			   var rId = Number($(SelectRequirement).attr("rId"));
			   for(var i=0;i<SelectSuiteDetail.preRequirement.length;i++){
				   if(rId == SelectSuiteDetail.preRequirement[i].rId){
					   SelectSuiteDetail.preRequirement[i].pickerValue.push(data.data);
				   }
			   }
			   $(tbody).append(SuiteHandle.make_require_picker_tr(data.data.vId,data.data.value,data.data.expression));
		   }else{
			   $.fail_prompt("删除前置条件失败："+data["message"],5000);
		   }
		}
		$.requestJson("/requirement/add/picker","POST",data,callback);//然后就修改requireid
	}
	main.make_require_picker_tr=function(vId,name,expression){
		var tr = '<tr vId='+vId+'>\
					<td width="25%" style="padding: 5px;">'+name+'</td>\
				  	<td width="72%" style="padding: 5px;">'+expression+'</td>\
				  	<td width="3%" style="padding: 5px;margin-top:20px">\
						<button class="btn btn-danger btn-xs" type="button" onclick="SuiteHandle.delete_require_picker(this)">\
							<i class="icon-trash"></i>\
						</button>\
				  	</td></tr>';
		return tr;
	}
	//显示变量提取
	main.event_show_require_picker = function(){
		$(".requirementclass").on("show.bs.collapse",function(){
			var rId = Number($(this).parent().attr("rId"));
			for(var i=0;i<SelectSuiteDetail.preRequirement.length;i++){
				if(SelectSuiteDetail.preRequirement[i].rId == rId){
					var tbody = $(this).find("tbody");
					$(tbody).html("");
					var picker = SelectSuiteDetail.preRequirement[i].pickerValue;
					for(var j=0;j<picker.length;j++){
						$(tbody).append(SuiteHandle.make_require_picker_tr(picker[j].vId,picker[j].value,picker[j].expression));
					}
					break;
				}
			}
		});
	}
	//删除变量提取
	main.delete_require_picker = function(obj){
		var tr = $(obj).parent().parent();
		SelectRequirePicker = tr;
		var vId = Number($(tr).attr("vId"));
		var div = $(tr).parents(".div_requirement_class");
		var rId = Number($(div).attr("rId"));
		var callback = function(data){
		   if(data["success"] == "true"|| data["success"] == true){
			   SelectSuiteDetail.preRequirement = data.data;
			   $(SelectRequirePicker).remove();
		   }else{
			   $.fail_prompt("删除前置条件失败："+data["message"],5000);
		   }
		}
		$.requestJson("/requirement/delete/picker","POST",{"vId":vId,"rId":rId},callback);//然后就修改requireid
	}
	
	
	//删除案例
	main.delete_case = function(obj){
		PanelTmpHtml = $("#accordion").html();
		$(obj).parents(".panel-py-mark").remove();
		
		var suId=SelectSuite.suId;
		if(undefined==suId){
			return;
		}
		var all_panels = $(".panel-py-mark");
		var casesId = [];
		for(var i=0;i<all_panels.length;i++){
			var cId = Number($(all_panels[i]).attr("cId"));
			if(isNaN(cId)){
				continue;
			}else{
				casesId.push(cId);
			}
		}
		var callback = function(data){
  		   if(data["success"] == "true"|| data["success"] == true){
  			   var cases = data.data.cases;
			   SelectSuiteDetail.cases = cases;
			   
			   $("#accordion").html("");
			   for(var i=0;i<cases.length;i++){
				   var div = SuiteHandle.make_suite_profile_panel(cases[i]);
				   $("#accordion").append(div);
			   }
			   SuiteHandle.event_collapse_show();
  		   }else{
  			   $.fail_prompt("删除失败："+data["message"],5000);
  			   $("#accordion").html(PanelTmpHtml);
  		   }
    	}
		$.requestJson("/suite/update/cases","POST",{"suId":suId,"casesId":JSON.stringify(casesId)},callback);
	}
	//上移案例
	main.suite_turn_up = function(obj){
		PanelTmpHtml = $("#accordion").html();
		
		var panel = $(obj).parents(".panel-py-mark");
		var prev = panel.prev();
		if(prev.length<1){
			return;
		}
		prev.before(panel);
		var suId=SelectSuite.suId;
		if(undefined==suId){
			return;
		}
		var all_panels = $(".panel-py-mark");
		var casesId = [];
		for(var i=0;i<all_panels.length;i++){
			var cId = Number($(all_panels[i]).attr("cId"));
			if(isNaN(cId)){
				continue;
			}else{
				casesId.push(cId);
			}
		}

		var callback = function(data){
  		   if(data["success"] == "true"|| data["success"] == true){
  			   var cases = data.data.cases;
			   SelectSuiteDetail.cases = cases;
			   
			   $("#accordion").html("");
			   for(var i=0;i<cases.length;i++){
				   var div = SuiteHandle.make_suite_profile_panel(cases[i]);
				   $("#accordion").append(div);
			   }
			   SuiteHandle.event_collapse_show();
  		   }else{
  			   $.fail_prompt("上移失败："+data["message"],5000);
  			   $("#accordion").html(PanelTmpHtml);
  		   }
    	}
		$.requestJson("/suite/update/cases","POST",{"suId":suId,"casesId":JSON.stringify(casesId)},callback);
	}
	//下移案例
	main.suite_turn_down = function(obj){
		var pre_html = $("#accordion").html();
		var panel = $(obj).parents(".panel-py-mark");
		var next = panel.next();
		if(next.length<1){
			return;
		}
		next.after(panel);
		
		var suId=SelectSuite.suId;
		if(undefined==suId){
			return;
		}
		var all_panels = $(".panel-py-mark");
		var casesId = [];
		for(var i=0;i<all_panels.length;i++){
			var cId = Number($(all_panels[i]).attr("cId"));
			if(isNaN(cId)){
				continue;
			}else{
				casesId.push(cId);
			}
		}
		var callback = function(data){
  		   if(data["success"] == "true"|| data["success"] == true){
  			   var cases = data.data.cases;
			   SelectSuiteDetail.cases = cases;
			   
			   $("#accordion").html("");
			   for(var i=0;i<cases.length;i++){
				   var div = SuiteHandle.make_suite_profile_panel(cases[i]);
				   $("#accordion").append(div);
			   }
			   SuiteHandle.event_collapse_show();
  		   }else{
  			   $.fail_prompt("下移失败："+data["message"],5000);
  			   $("#accordion").html(PanelTmpHtml);
  		   }
    	}
		$.requestJson("/suite/update/cases","POST",{"suId":suId,"casesId":JSON.stringify(casesId)},callback);
	}
	
	$("#suite_tab").on("click",function(){
		SuiteHandle.get_suite_list();
		SuiteHandle.no_data("show");
	});
	SuiteAddSetting();
	SuiteUpdateSetting();
	SuitePreRequireSetting();
	SuitePostRequireSetting();
	SuiteAddCaseSetting();
	
	return main;
}());


