/**
 * author:anonymous
 */

var moduleSetting = function(){
	// modal表单验证定义
    $('#modal_module_form').bootstrapValidator({
　　　　　message: '参数不能正确！',
        feedbackIcons: {
　　　　　　　/*
		 * valid: 'glyphicon glyphicon-ok', invalid: 'glyphicon
		 * glyphicon-remove',
		 */
　　　　　　　　validating: 'glyphicon glyphicon-refresh'
　　　　　},
        fields: {
        	inputModuleName: {
                validators: {
                    notEmpty: {
                        message: '模块名不能为空'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: '模块名长度必须在1到30位之间'
                    },
                }
            }
        }
    });
	//创建模块
    $("#bt_add_module_interface").on('click',function(){
    	var nodes = $("#ztree").getSelectedNodes();
    	if(nodes.length>0 && "module"!=nodes[0].type){
    		$.fail_prompt("请先选择模块！！！",3000);//如果选择的是接口，则不能操作
    		return;
    	}
		$("#moduleModal").modal('toggle');
    	$("#bt_create_module").show();
    	$("#bt_update_module").hide();
    	$("#modal_module_title").html("新建模块");
    });
	// 编辑模块
	$("#bt_update_module").on('click',function(){
	 // 获取表单对象
       var bootstrapValidator = $("#modal_module_form").data('bootstrapValidator');
           // 手动触发验证
       bootstrapValidator.validate();
       if(!bootstrapValidator.isValid()){
    	   return;
       }
 	   	var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			  $("#moduleModal").modal('toggle');
 			  $("#ztree").updateCurrentZTreeNode(data.data.name);
 		   }else{
 			   $.fail_prompt("执行失败："+data["message"],5000);
 		   }
    	}
 	   var nodes = $("#ztree").getSelectedNodes();
 	   var data = {};
 	   data["name"] =  $('#inputModuleName').val();
 	   data["mId"] = nodes[0].mId;
 	   $.requestJson("/module/update","POST",data,callback);
	});
	
	//创建模块
	$("#bt_create_module").on('click',function(){
   	 // 获取表单对象
      var bootstrapValidator = $("#modal_module_form").data('bootstrapValidator');
          // 手动触发验证
      bootstrapValidator.validate();
      if(bootstrapValidator.isValid()){
          // 表单提交的方法、创建项目
   	   var callback = function(data){
   		   if(data["success"] == "true"|| data["success"] == true){
   			   $("#moduleModal").modal('toggle');
//       		   $.success_prompt("新建成功",2000);
   			   $("#ztree").addZTreeChildNode(data.data);   
   		   }else{
   			   $.fail_prompt("执行失败："+data["message"],5000);
   		   }
      	   }
   	   var data = {};
   	   var nodes = $("#ztree").getSelectedNodes();
   	   if(nodes.length==0){
   		   data["parentId"] = 0;
   	   }else{
   		   data["parentId"] = nodes[0].mId;
   	   }
   	   
   	   data["name"] = $("#inputModuleName").val();
   	   if(""==$("#inputModuleName").val()){
   		   return;
   	   }
   	   data["pId"] = ApiHandle.pId;
   	   
   	   $.requestJson("/module/add","POST",data,callback);
      }
   });
}

var ApiSetting = function(){
	 // 新建接口表单验证
    $('#new_inter_form').bootstrapValidator({
   　　　　　message: '参数不能正确！',
           feedbackIcons: {
   　　　　　　　　validating: 'glyphicon glyphicon-refresh'
   　　　　　},
           fields: {
        	   input_new_inter_name: {
                   validators: {
                       notEmpty: {
                           message: '接口名称不能为空'
                       }
                   }
               },
               input_new_inter_url: {
                   validators: {
                       notEmpty: {
                           message: '接口url不能为空'
                       }
                   }
               },
               input_new_inter_dec: {
                   validators: {
                       notEmpty: {
                           message: '接口描述不能为空'
                       }
                   }
               }
           }
       });
 // 创建api接口
    $('#bt_create_inter').on('click',function(){
    	var bootstrapValidator = $("#new_inter_form").data('bootstrapValidator');
	    // 手动触发验证
	    bootstrapValidator.validate();
	    if(bootstrapValidator.isValid()){	    	
	    	var callback = function(data){
    		   if(data["success"] == "true"|| data["success"] == true){
				    $("#interModal").modal('toggle');
				    $("#ztree").addZTreeChildNode(data.data);
    		   }else{
    			   $.fail_prompt("执行失败："+data["message"],5000);
    		   }
       	   }
    	   var data = {};
    	   data["name"] = $("#input_new_inter_name").val();
    	   data["url"] = $("#input_new_inter_url").val();
    	   data["dec"] = $("#input_new_inter_dec").val();
    	   data["method"] = $('input:radio[name="input_new_inter_method"]:checked').val();
    	   data["pId"] = ApiHandle.pId;
    	   var nodes=$('#ztree').getSelectedNodes();
    	   data["mId"] = nodes[0].mId;
    	   data["uId"] = PIBase.userInfo["userId"];
    	   $.requestJson("/api/add","POST",data,callback);
	    }
    });
}

var TongleSetting = function(){
    $("#a_tonggle_header").on('click',function(){
    	var display =$('#div_header').css('display');
    	$(this).find("i").hide();
    	if(display == 'none'){
    		$('#div_header').show();
    		$(this).find("i.icon-chevron-down").show();
    	}else{
    		$('#div_header').hide();
    		$(this).find("i.icon-chevron-up").show();
    	}
//    	PIBase.setScroll();
    });
    $("#a_tonggle_parmas").on('click',function(){
    	var display =$('#div_parmas').css('display');
    	$(this).find("i").hide();
    	if(display == 'none'){
    		$('#div_parmas').show();
    		$(this).find("i.icon-chevron-down").show();
    		apiedit.parmas_2_json();//进行json转换
    	}else{
    		$('#div_parmas').hide();
    		$(this).find("i.icon-chevron-up").show();
    	}
//    	PIBase.setScroll();
    	
    });
    $("#a_tonggle_response").on('click',function(){
    	var display =$('#div_response').css('display');
    	$(this).find("i").hide();
    	if(display == 'none'){
    		$('#div_response').show();
    		$(this).find("i.icon-chevron-down").show();
    		apiedit.response_2_json();;//进行json转换
    	}else{
    		$('#div_response').hide();
    		$(this).find("i.icon-chevron-up").show();
    	}
//    	PIBase.setScroll();
    });
}

var ApiHandle = (function () {
    var main = {};
    main.pId=-1;
    main.current_node={};
    main.current_mName="test";
    
    main.isEmpty = function (obj){
    	if(obj==undefined){
    		return true;
    	}
        for (var name in obj) 
        {
            return false;
        }
        return true;
    };
    
    // 刷新模块列表
    main.freshModules=function(data){
    	
    	var selectNode = function(node){
    		if(node.type=="module"){
    			$("#section_api_detail").hide();
        		$("#section_case_detail").hide();
        		$("#section_api_detail_nodata").show();
    			return;
    		}
    		if(node.type=="api"){
    			var callback = function(data){
    	    		   if(data["success"] == "true"|| data["success"] == true){
    	    			   GlobalData["select_api_info"] = data.data
    	    			   $("#aId").attr("aId",data.data.aId);
    	    			   $("#lable_Inter_name").html(data.data.name);
    	    			   $("#lable_Inter_url").html(data.data.url);
    	    			   $("#lable_Inter_method").html(data.data.method);
    	    			   $("#div_inter_dec").html(data.data.dec);
    	    			   $("#lable_Inter_parmas_type").html(data.data.parmasType);
    	    			   $("#lable_Inter_response_type").html(data.data.responseType);
    	    			   var headlist = data.data.header
    	    			   last = $("#tb_header tr:last");
    	    			   html = last[0].outerHTML
    	    			   $("#tb_header tbody").html("");
    	    			   $("#tb_header tbody").append(html);
    	    			   for(var i=0;i<headlist.length;i++){
    	    				   ApiHandle.add_head_row(headlist[i].hId,headlist[i].name,headlist[i].value,headlist[i].dec);
    	    			   };
    	    			   var parmas = data.data.parmas
    	    			   last = $("#tb_parmas tr:last");
    	    			   html = last[0].outerHTML
    	    			   $("#tb_parmas tbody").html("");
    	    			   $("#tb_parmas tbody").append(html);
    	    			   for(var i=0;i<parmas.length;i++){
    	    				   ApiHandle.add_parmas_row(parmas[i].pId,parmas[i].name,parmas[i].type,parmas[i].dec);
    	    			   };
    	    			   var response = data.data.response
    	    			   last = $("#tb_response tr:last");
    	    			   html = last[0].outerHTML
    	    			   $("#tb_response tbody").html("");
    	    			   $("#tb_response tbody").append(html);
    	    			   for(var i=0;i<response.length;i++){
    	    				   ApiHandle.add_response_row(response[i].rId,response[i].name,response[i].type,response[i].dec);
    	    			   }
    	    			   $("#section_api_detail").show();
    	    			   $(".inter_edit").hide();
    	    			   $(".inter_save").show();
    	    			   $("#section_api_detail_nodata").hide();
    	    			   $("#section_case_detail").hide();
    	    			   
    	    			   ApiHandle.set_select_type_click();
    	    			   apiedit.parmas_2_json();
    	    			   apiedit.response_2_json();
    	    		   }else{
    	    			   $.fail_prompt("查询数据失败："+data["message"],5000);
    	    		   }
    	            }
    	    		$.requestJson("/api/detail","POST",{"aId":node.aId},callback);
    		}else{
    			//TODO case
    			CaseHandle.get_case_detail(node.cId);
    			$("#section_api_detail").hide();
 			    $("#section_api_detail_nodata").hide();
 			    $("#section_case_detail").show();
    		}
    	}
    	
    	var OnRightClick = function(event, treeId, treeNode) {
//    		console.log(event);
    		if (!treeNode && event.target.tagName.toLowerCase() != "button" && $(event.target).parents("a").length == 0) {
    	        //showRMenu("root", event.clientX, event.clientY);	
    	    } else if (treeNode && !treeNode.noR) {
    	    	showRMenu("node", event.screenX, event.target.offsetTop);
    	    }
    		$("#rMenu ul li").hide();
    		switch(treeNode.type){
    		case "module":
    			$("#m_add_module").show();
    			$("#m_edit_module").show();
    			$("#m_add_api").show();
    			$("#m_del_module").show();
    			break;
    		case "api":
    			$("#m_add_case").show();
    			$("#m_copy_api").show();
    			$("#m_del_api").show();
    			break;
    		case "case":
    			$("#m_copy_case").show();
    			$("#m_del_case").show();
    			break;
    		}
    		$("#ztree").selectedNodes(treeNode)
    	}
    	//显示右键菜单
    	function showRMenu(type, x, y) {
//    		y = y-130;
    	    $("#rMenu ul").show();
    	    $("#rMenu").css({"top":y+"px", "left":x+"px", "visibility":"visible"}); //设置右键菜单的位置、可见
    	    $("body").bind("mousedown", onBodyMouseDown);
    	}
    	//隐藏右键菜单
    	function hideRMenu() {
    		$("#rMenu").css({"visibility": "hidden"}); //设置右键菜单不可见
    	    $("body").unbind("mousedown", onBodyMouseDown);
    	}
    	//鼠标按下事件
    	function onBodyMouseDown(event){
    	    if (!(event.target.id == "rMenu" || $(event.target).parents("#rMenu").length>0)) {
    	    	$("#rMenu").css({"visibility" : "hidden"});
    	    }
    	}

    	var defaluts = {
    	        dataList: data,
    	        setting:{
    	        	view: {
        				dblClickExpand: false,
        				showTitle:true, //是否显示节点title信息提示 默认为true
        			},
    	        	callback:{
    	        		onClick: function zTreeOnClick(event, treeId, treeNode) {
    	        		    selectNode(treeNode);
    	        		},
    	        		onRightClick: OnRightClick
    	        	},
        			data: {
        	        	simpleData: {
        	        		enable: true
        	        	},
        	    		key: {
        	    			title: "title",
        	    			name: "name"
        	    		}
        	    	}
    	        }
    	        
    	};
    	$("#ztree").initZTree(defaluts);
    	$("#rMenu ul li").on("click",function(){
    		$("#rMenu").css({"visibility": "hidden"}); //设置右键菜单不可见
    	    $("body").unbind("mousedown", onBodyMouseDown);
    	});
    	
    	$("#section_api_detail").hide();
		$("#section_api_detail_nodata").show();
		$("#section_case_detail").hide();
    };
    
 // 编辑模块
    main.a_edit_module = function(){
    	var nodes = $("#ztree").getSelectedNodes();
    	if(nodes.length==0){
    		return;
    	}
	 	var node = nodes[0];
	 	if("module"!=node.type){
	 		return
	 	}
    	$("#bt_create_module").hide();
    	$("#bt_update_module").show();
    	$("#inputModuleName").val(node.alltext);
    	$("#moduleModal").modal('toggle');
    	$("#modal_module_title").html("编辑模块");
    };

  // 删除模块
	main.a_delete_module = function(){
		var nodes = $("#ztree").getSelectedNodes();
		if(nodes.length==0){
			return;
		}
		var node = nodes[0];
		if(node.type=="module"){
			swal({
	   	        title: "您确定要删除模块吗？",  
	   	        text: "您确定要删除这个模块吗？",  
	   	        type: "warning", 
	   	        showCancelButton: true, 
	   	        closeOnConfirm: true, 
	   	        confirmButtonText: "是的，我要删除", 
	   	        confirmButtonColor: "#ec6c62" 
	   	    }, function() {
	     	   	var callback = function(data){
	     		  if(data["success"] == "true"|| data["success"] == true){
	         		 var nodes = $("#ztree").getSelectedNodes();
	         		 if(nodes.length > 0){
	         			$("#ztree").removeNode(nodes[0]);
	         		 }
	         		 $("#section_api_detail").hide();
	         		 $("#section_case_detail").hide();
	         		 $("#section_api_detail_nodata").show();
	     		   }else{
	     			   $.fail_prompt("执行失败："+data["message"],5000);
	     		   	}
	     	   	}
	     	   $.requestJson("/module/delete","POST",{"mId":node.mId},callback);
	   	    }); 
		}
	};
	main.a_delete_interface = function(){
		var nodes=$('#ztree').getSelectedNodes();
		if(nodes.length==0){
			return;
		}
		var node = nodes[0];
		if(node.type=="module"){
			return;
		}else{
			swal({ 
	   	        title: "您确定要删除接口吗？",  
	   	        text: "删除接口会同时把它的下面的案例一并删除",  
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
	     	   $.requestJson("/api/delete","POST",{"aId":node.aId},callback);
	   	    }); 
		}
	};
	
    // 获取模块数据
    main.getModules=function(){
    	var callback = function(data){
  		   if(data["success"] == "true"|| data["success"] == true){
  			   GlobalData["tree_list"] = data.data.data;
      		   ApiHandle.freshModules(data.data.data);
  		   }else{
  			   $.fail_prompt("获取模块数据失败："+data["message"],5000);
  		   }
    	}
  	   	$.requestJson("/module/lists","POST",{"pId":ApiHandle.pId},callback);
    };  
    
    // 添加模块或者接口
    main.a_add_module = function(){
    	var nodes = $("#ztree").getSelectedNodes();
    	var mark = false;
        for(var i=0;i<nodes.length;i++){
	        if("module"==nodes[i].type){
	        	mark = true;
	        	break;
	        }
        }
    	if(mark){
    		$("#moduleModal").modal('toggle');
        	$("#bt_create_module").show();
        	$("#bt_update_module").hide();
        	$("#modal_module_title").html("新建模块")
    	}else{
    		$.fail_prompt("请先选择模块！！！",3000);//如果选择的是接口，则不能操作
    		return;
    	}
    }
    main.a_add_interface = function(){
    	var nodes = $("#ztree").getSelectedNodes();
    	if(nodes.length==0 || "module"!=nodes[0].type){
    		$.fail_prompt("请先选择模块！！！",3000);
    	}else{
    		$('#interModal').modal('toggle');
    	}
    };
    
    // 这是添加头部
    main.delete_head_row=function(obj){
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$(obj).parent().parent().remove();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		data["aId"] = $("#aId").attr("aId");
		data["hId"] = $(obj).parent().parent().attr("hId");
		$.requestJson("/api/update/delHeader","POST",data,callback);
// alert(1);
    };
    main.add_head_row=function(hId,name,value,dec){
    	var new_row = '<tr hId='+hId+'>\
		<td width="5%"><button class="btn btn-danger btn-xs" type="button" onclick="ApiHandle.delete_head_row(this)"><i class="icon-trash "></i></button></td>\
		<td width="20%" class="head_name">'+name+'</td>\
		<td width="35%" class="head_value">'+value+'</td>\
		<td width="35%">'+dec+'</td>\
		<td width="5%">\
			<a onclick="ApiHandle.table_tr_up(this)"><i class="icon-chevron-sign-up" ></i> </a>\
			<a onclick="ApiHandle.table_tr_down(this)"><i class="icon-chevron-sign-down" ></i></a>\
		</td></tr>';
		$("#tb_header tr:last").before(new_row);
    }
    main.bt_add_header = function(){
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				ApiHandle.add_head_row(data.data.hId,data.data.name,data.data.value,data.data.dec);
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		
		data["name"] = $("#input_head_name").val();
		if(data["name"]==""||data["name"]==undefined){
			return;
		}
		data["aId"] = $("#aId").attr("aId");
		data["value"] = $("#input_head_value").val();
		data["dec"] = $("#input_head_dec").val();
		$.requestJson("/api/update/addHeader","POST",data,callback);
    }
    
  // 改变顺序
    main.tmpobj = "";
    main.table_tr_up=function(obj){
    	var objParentTR=$(obj).parent().parent(); 
    	var prevTR=objParentTR.prev(); 
    	if(prevTR.length==0){ 
    		return;
    	}
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var objParentTR=$(ApiHandle.tmpobj).parent().parent(); 
		    	var prevTR=objParentTR.prev(); 
		    	if(prevTR.length>0){ 
		    		prevTR.before(objParentTR); 
		    	}
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		ApiHandle.tmpobj = obj;
		data["aId"] = $("#aId").attr("aId");
		data["hId"] = $(objParentTR).attr("hId");
		data["direction"] = "up";
		$.requestJson("/api/update/changeHeader","POST",data,callback);
    	
    };
    main.table_tr_down=function(obj){
    	var objParentTR=$(obj).parent().parent(); 
    	var nextTR=objParentTR.next();
    	var nexeNextTR = nextTR.next()
    	if(nexeNextTR.length==0) {
    		return;
    	}
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
		    	var objParentTR=$(ApiHandle.tmpobj).parent().parent(); 
		    	var nextTR=objParentTR.next();
		    	var nexeNextTR = nextTR.next()
		    	if(nexeNextTR.length>0) {
		    		nextTR.after(objParentTR); 
		    	}
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		ApiHandle.tmpobj = obj;
		data["aId"] = $("#aId").attr("aId");
		data["hId"] = $(objParentTR).attr("hId");
		data["direction"] = "down";
		$.requestJson("/api/update/changeHeader","POST",data,callback);
    };
    
  // 这是添加parmas
    main.bt_add_parmas = function(){
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				ApiHandle.add_parmas_row(data.data.pId,data.data.name,data.data.type,data.data.dec);
				GlobalData["select_api_info"].parmas.push(data.data);//更新全局数据
				apiedit.parmas_2_json();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		data["name"] = $("#input_parmas_name").val();
		if(data["name"]==""||data["name"]==undefined){
			return;
		}
		data["aId"] = $("#aId").attr("aId");
		data["type"] = $("#input_parmas_type").html();
		data["dec"] = $("#input_parmas_dec").val();
		$.requestJson("/api/update/addParmas","POST",data,callback);
    };
    main.add_parmas_row=function(pId,name,type,dec){
		var new_row = '<tr pId='+pId+'>\
			<td width="5%"><button class="btn btn-danger btn-xs" type="button" onclick="ApiHandle.delete_parms_row(this)">\
    		<i class="icon-trash "></i></button></td>\
			<td width="30%" class="parmas_name">'+name+'</td>\
			<td width="20%">'+type+'</td>\
			<td width="40%">'+dec+'</td>\
			<td width="5%">\
				<a onclick="ApiHandle.table_tr_parmas_up(this)"><i class="icon-chevron-sign-up" ></i> </a>\
				<a onclick="ApiHandle.table_tr_parmas_down(this)"><i class="icon-chevron-sign-down" ></i></a>\
			</td>\</tr>';
    	$("#tb_parmas tr:last").before(new_row);
    };
    main.delete_parms_row = function(obj){
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$(obj).parent().parent().remove();
				var del_id = data.data.delId;
				var parmas = GlobalData["select_api_info"].parmas;
				for(var i=0;i<parmas.length;i++){
					if(parmas[i].pId==del_id){
						parmas.splice(i,1);
						GlobalData["select_api_info"].parmas = parmas;
						break;
					}
				};
				apiedit.parmas_2_json();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		data["aId"] = $("#aId").attr("aId");
		data["pId"] = $(obj).parent().parent().attr("pId");
		$.requestJson("/api/update/delParmas","POST",data,callback);
    };
    
    main.table_tr_parmas_up=function(obj){
    	var objParentTR=$(obj).parent().parent(); 
    	var prevTR=objParentTR.prev(); 
    	if(prevTR.length==0){ 
    		return;
    	}
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var objParentTR=$(ApiHandle.tmpobj).parent().parent(); 
		    	var prevTR=objParentTR.prev(); 
		    	if(prevTR.length>0){ 
		    		prevTR.before(objParentTR); 
		    	}
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		ApiHandle.tmpobj = obj;
		data["aId"] = $("#aId").attr("aId");
		data["pId"] = $(objParentTR).attr("pId");
		data["direction"] = "up";
		$.requestJson("/api/update/changeParmas","POST",data,callback);
    	
    };
    main.table_tr_parmas_down=function(obj){
    	var objParentTR=$(obj).parent().parent(); 
    	var nextTR=objParentTR.next();
    	var nexeNextTR = nextTR.next()
    	if(nexeNextTR.length==0) {
    		return;
    	}
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
		    	var objParentTR=$(ApiHandle.tmpobj).parent().parent(); 
		    	var nextTR=objParentTR.next();
		    	var nexeNextTR = nextTR.next()
		    	if(nexeNextTR.length>0) {
		    		nextTR.after(objParentTR); 
		    	}
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		ApiHandle.tmpobj = obj;
		data["aId"] = $("#aId").attr("aId");
		data["pId"] = $(objParentTR).attr("pId");
		data["direction"] = "down";
		$.requestJson("/api/update/changeParmas","POST",data,callback);
    };
    
    // 这是添加response
    main.add_response_row=function(rId,name,type,dec){
		var new_row = '<tr rId='+rId+'>\
			<td width="5%"><button class="btn btn-danger btn-xs" type="button" onclick="ApiHandle.delete_response_row(this)">\
    		<i class="icon-trash "></i></button></td>\
			<td width="30%">'+name+'</td>\
			<td width="20%">'+type+'</td>\
			<td width="40%">'+dec+'</td>\
			<td width="5%">\
				<a onclick="ApiHandle.table_tr_response_up(this)"><i class="icon-chevron-sign-up" ></i> </a>\
				<a onclick="ApiHandle.table_tr_response_down(this)"><i class="icon-chevron-sign-down" ></i></a>\
			</td>\</tr>';
		$("#tb_response tr:last").before(new_row);
    };
    main.bt_add_response = function(){
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				ApiHandle.add_response_row(data.data.rId,data.data.name,data.data.type,data.data.dec);
				GlobalData["select_api_info"].response.push(data.data);
				apiedit.response_2_json();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		data["name"] = $("#input_response_name").val();;
		if(data["name"]==""||data["name"]==undefined){
			return;
		}
		data["aId"] = $("#aId").attr("aId");
		data["type"] = $("#input_response_type").html();
		data["dec"] = $("#input_response_dec").val();
		$.requestJson("/api/update/addResponse","POST",data,callback);
    };
    main.delete_response_row = function(obj){
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$(obj).parent().parent().remove();
				var del_id = data.data.delId;
//				console.log(GlobalData["select_api_info"].response);
				var response = GlobalData["select_api_info"].response;
				for(var i=0;i<response.length;i++){
					if(response[i].rId==del_id){
						response.splice(i,1);
						GlobalData["select_api_info"].response;
						break;
					}
				}
				apiedit.response_2_json();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		data["aId"] = $("#aId").attr("aId");
		data["rId"] = $(obj).parent().parent().attr("rId");
		$.requestJson("/api/update/delResponse","POST",data,callback);
    };
    main.table_tr_response_up=function(obj){
    	var objParentTR=$(obj).parent().parent(); 
    	var prevTR=objParentTR.prev(); 
    	if(prevTR.length==0){ 
    		return;
    	}
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var objParentTR=$(ApiHandle.tmpobj).parent().parent(); 
		    	var prevTR=objParentTR.prev(); 
		    	if(prevTR.length>0){ 
		    		prevTR.before(objParentTR); 
		    	}
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		ApiHandle.tmpobj = obj;
		data["aId"] = $("#aId").attr("aId");
		data["rId"] = $(objParentTR).attr("rId");
		data["direction"] = "up";
		$.requestJson("/api/update/changeResponse","POST",data,callback);
    	
    };
    main.table_tr_response_down=function(obj){
    	var objParentTR=$(obj).parent().parent(); 
    	var nextTR=objParentTR.next();
    	var nexeNextTR = nextTR.next()
    	if(nexeNextTR.length==0) {
    		return;
    	}
    	var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
		    	var objParentTR=$(ApiHandle.tmpobj).parent().parent(); 
		    	var nextTR=objParentTR.next();
		    	var nexeNextTR = nextTR.next()
		    	if(nexeNextTR.length>0) {
		    		nextTR.after(objParentTR); 
		    	}
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var data={};
		ApiHandle.tmpobj = obj;
		data["aId"] = $("#aId").attr("aId");
		data["rId"] = $(objParentTR).attr("rId");
		data["direction"] = "down";
		$.requestJson("/api/update/changeResponse","POST",data,callback);
    };

    // 下拉框
    main.set_select_type_click = function(){
    	$(".select_type").on('click',function(){
        	var text = $(this).find("a").html();
        	var bt = $(this).parent().prev().prev();
        	$(bt).html(text);
//        	PIBase.setScroll();
        });
    	
    };
//    $(".select_add_type").on('click',function(){//用于新建模块还是接口
//    	var text = $(this).find("a").html();
//    	var bt = $(this).parent().prev();
//    	$(bt).html(text + '<span class="caret"></span>');
//    });
//    
  //拷贝api
	main.copy_api=function(){
		var callback = function(data){
 		   if(data["success"] == "true"|| data["success"] == true){
 			   $("#ztree").addZTreeBrotherNode(data.data);
 		   }else{
 			   $.fail_prompt("执行失败："+data["message"],5000);
 		   }
		}
		var nodes = $("#ztree").getSelectedNodes();
		var aId = nodes[0].aId;
		$.requestJson("/api/copy","POST",{"aId":aId},callback);
	}
    
	// 获取树形结构
    $("#apiDefine").on('click',function(){
    	ApiHandle.getModules();
    });
    
    moduleSetting();
    ApiSetting();
    TongleSetting();
    return main;
}());


//api名字设置
var ApiNameSetting = function(){
	//api名称控件点击设置
	$("#lable_Inter_name").on('click',function(){
    	$(".inter_edit_name").show();
    	$(".inter_save_name").hide();
    	var name = $("#lable_Inter_name").html();
    	$("#input_inter_name").val(name)
    	$("#input_inter_name").focus();
    });
	// 修改api名称
	$("#save_inter_name").on('click',function(){
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var name = $("#input_inter_name").val();
				$("#lable_Inter_name").html(name);
				$(".inter_edit_name").hide();
				$(".inter_save_name").show();

				$("#ztree").updateCurrentZTreeNode(name);
	     		  
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var name = $("#input_inter_name").val();
		if(name==""||name==undefined){
			return;
		}
		$.requestJson("/api/update/name","POST",{"aId":$("#aId").attr("aId"),"name":name},callback);
	});
	$("#dismiss_inter_name").on('click',function(){
		$(".inter_edit_name").hide();
    	$(".inter_save_name").show();
	});
}

//修改api的url
var ApiUrlSetting = function(){
	$("#lable_Inter_url").on('click',function(){
    	$(".inter_edit_url").show();
    	$(".inter_save_url").hide();
    	var name = $("#lable_Inter_url").html();
    	$("#input_inter_url").val(name)
    	$("#input_inter_url").focus();
    });
	$("#save_inter_url").on('click',function(){
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
		    	var url = $("#input_inter_url").val();
		    	$("#lable_Inter_url").html(url);
		    	$(".inter_edit_url").hide();
		    	$(".inter_save_url").show();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var url = $("#input_inter_url").val();
		if(url==""||url==undefined){
			return;
		}
		$.requestJson("/api/update/url","POST",{"aId":$("#aId").attr("aId"),"url":url},callback);
	});
	$("#dismiss_inter_url").on('click',function(){
		$(".inter_edit_url").hide();
    	$(".inter_save_url").show();
	})
}
//修改api的dec
var ApiDecSetting = function(){
	$("#div_inter_dec").on('click',function(){
    	$(".inter_edit_dec").show();
    	$(".inter_save_dec").hide();
    	var name = $("#div_inter_dec").html();
    	$("#textarea_inter_dec").val(name)
    	$("#textarea_inter_dec").focus();
    });
	$("#save_inter_dec").on('click',function(){
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
		    	var name = $("#textarea_inter_dec").val();
		    	$("#div_inter_dec").html(name);
		    	$(".inter_edit_dec").hide();
		    	$(".inter_save_dec").show();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var dec = $("#textarea_inter_dec").val();
		if(dec==""||dec==undefined){
			return;
		}
		$.requestJson("/api/update/dec","POST",{"aId":$("#aId").attr("aId"),"dec":dec},callback);
	});
	$("#dismiss_inter_dec").on('click',function(){
		$(".inter_edit_dec").hide();
    	$(".inter_save_dec").show();
	});
}

//修改api的方法
var ApiMethodSetting = function(){
	$("#lable_Inter_method").on('click',function(){
    	$(".inter_edit_method").show();
    	$(".inter_save_method").hide();
    	var method = $("#lable_Inter_method").html();
    	$('input:radio[name="method"][value="'+method+'"]').prop("checked",true);
    });
	$("#save_inter_method").on('click',function(){
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var method = $('input:radio[name="method"]:checked').val();
		    	$("#lable_Inter_method").html(method);
		    	$(".inter_edit_method").hide();
		    	$(".inter_save_method").show();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var method = $('input:radio[name="method"]:checked').val();
		$.requestJson("/api/update/method","POST",{"aId":$("#aId").attr("aId"),"method":method},callback);
	});
	$("#dismiss_inter_method").on('click',function(){
		$(".inter_edit_method").hide();
    	$(".inter_save_method").show();
	});
}

//修改api的参数类型
var ApiParmasTypeSetting = function(){	
	$("#lable_Inter_parmas_type").on('click',function(){
    	$(".inter_edit_parmas_type").show();
    	$(".inter_save_parmas_type").hide();
    	var parmasType = $("#lable_Inter_parmas_type").html();
    	$('input:radio[name="parmas"][value="'+parmasType+'"]').prop("checked",true);
    });
	$("#save_inter_parmas_type").on('click',function(){
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var parmasType = $('input:radio[name="parmas"]:checked').val();
		    	$("#lable_Inter_parmas_type").html(parmasType);
		    	$(".inter_edit_parmas_type").hide();
		    	$(".inter_save_parmas_type").show();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var parmasType = $('input:radio[name="parmas"]:checked').val();
		$.requestJson("/api/update/parmasType","POST",{"aId":$("#aId").attr("aId"),"parmasType":parmasType},callback);
	});
	$("#dismiss_inter_parmas_type").on('click',function(){
		$(".inter_edit_parmas_type").hide();
    	$(".inter_save_parmas_type").show();
	});
}

// 修改api的响应的参数类型
var ApiResponseTypeSetting = function(){
	$("#lable_Inter_response_type").on('click',function(){
    	$(".inter_edit_response_type").show();
    	$(".inter_save_response_type").hide();
    	var responseType = $("#lable_Inter_response_type").html();
    	$('input:radio[name="response"][value="'+responseType+'"]').prop("checked",true);
    });
	$("#save_inter_response_type").on('click',function(){
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var response = $('input:radio[name="response"]:checked').val();
		    	$("#lable_Inter_response_type").html(response);
		    	$(".inter_edit_response_type").hide();
		    	$(".inter_save_response_type").show();
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		var responseType = $('input:radio[name="response"]:checked').val();
		$.requestJson("/api/update/responseType","POST",{"aId":$("#aId").attr("aId"),"responseType":responseType},callback);
	});
	$("#dismiss_inter_response_type").on('click',function(){
		$(".inter_edit_response_type").hide();
    	$(".inter_save_response_type").show();
	});
}

var ApiParmasTransforSetting = function(){
	//参数装换
	$("#button_sync_parmas_2_json").on('click',function(){
		apiedit.parmas_2_json();
	});
	$("#button_sync_json_2_parmas").on('click',function(){
		apiedit.json_2_parmas();
	});
	//响应转换
	$("#button_sync_response_2_json").on('click',function(){
		apiedit.response_2_json();
	});
	$("#button_sync_json_2_response").on('click',function(){
		apiedit.json_2_response();
	});
}

var apiedit = (function () {
	var main={};
	//参数转换
//	PIBase.textAreaAutoHeight("textarea_inter_parmas");
//	PIBase.textAreaAutoHeight("textarea_inter_response");
	$("#textarea_inter_parmas").autoTextarea();
	$("#textarea_inter_response").autoTextarea();
	
	$(function () { $("[data-toggle='tooltip']").tooltip(); });
	//json转换
	main.parmas_2_json=function(){
		var parmas = GlobalData["select_api_info"].parmas;
		var json = $.form2json(parmas);
		$("#textarea_inter_parmas").val(JSON.stringify(json, null, 8)); 
//		PIBase.setStyle('textarea_inter_parmas');
	};
	main.json_2_parmas=function(){
		var json={};
		try{
			json = JSON.parse($("#textarea_inter_parmas").val());
		}catch(err){
			$.fail_prompt("json格式不正确，请重新检查输入");
			return;
		}
		$("#textarea_inter_parmas").val(JSON.stringify(json, null, 8));
		var parmas = $.json2form(json,GlobalData["select_api_info"].aId);
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
			    last = $("#tb_parmas tr:last");
			    html = last[0].outerHTML
			    $("#tb_parmas tbody").html("");
			    $("#tb_parmas tbody").append(html);
			    for(var i=0;i<data.data.length;i++){
				    ApiHandle.add_parmas_row(data.data[i].pId,data.data[i].name,data.data[i].type,data.data[i].dec);
			    };
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		$.requestJson("/api/update/setParmas","POST",parmas,callback);
	};
	
	main.response_2_json=function(){
		var response = GlobalData["select_api_info"].response;
		var json = $.form2json(response);
		$("#textarea_inter_response").val(JSON.stringify(json, null, 8)); 
//		PIBase.setStyle('textarea_inter_response');
	};
	main.json_2_response=function(){
		var json={};
		try{
			json = JSON.parse($("#textarea_inter_response").val());
		}catch(err){
			$.fail_prompt("json格式不正确，请重新检查输入");
			return;
		}
		$("#textarea_inter_response").val(JSON.stringify(json, null, 8)); 
		var response = $.json2form(json,GlobalData["select_api_info"].aId);
		console.log(response);

		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				var response = data.data;
			    last = $("#tb_response tr:last");
			    html = last[0].outerHTML
			    $("#tb_response tbody").html("");
			    $("#tb_response tbody").append(html);
			    for(var i=0;i<response.length;i++){
				    ApiHandle.add_response_row(response[i].rId,response[i].name,response[i].type,response[i].dec);
			    };
			}else{
				$.fail_prompt("执行失败："+data["message"],5000);
			}
		};
		$.requestJson("/api/update/setResponse","POST",response,callback);
	};
	
	ApiNameSetting();
	ApiUrlSetting();
	ApiDecSetting()
	ApiMethodSetting();
	ApiParmasTypeSetting();
	ApiResponseTypeSetting();
	ApiParmasTransforSetting();
	return main;
}());

