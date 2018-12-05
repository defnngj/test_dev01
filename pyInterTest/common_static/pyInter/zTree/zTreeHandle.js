/**
 * 用于处理接口系统的树形结构
 * author:anonymous
 */

//闭包限定命名空间
(function ($) {
	$.fn.extend({
        "initZTree":function(options){
        	var id = this.attr("id");
        	//检测用户传进来的参数是否合法
            if (!isValid(options))
                return this;
            var opts = $.extend({}, defaluts, options); //使用jQuery.extend 覆盖插件默认参数
            
        	var tree=[];
        	data = options.dataList;
        	for(var i=0;i<data.length;i++){
        		var tmpNode=setNodeData(data[i]);
        		if(data[i].parentId==undefined || data[i].parentId==0){
        			tree.push(tmpNode);
        		}else{
        			setJsonChild.mark=false;
        			setJsonChild(tree,tmpNode);// 递归设置数据
        		}
        	};
        	$.fn.zTree.init($("#"+id), options.setting, tree);
        },
        "addZTreeChildNode": function(data){
        	var id = this.attr("id");
 		    var tmpNode = setNodeData(data);;
		    var treeObj = $.fn.zTree.getZTreeObj(id);
		    var nodes = treeObj.getSelectedNodes();
		    if(nodes.length==0){
		    	treeObj.addNodes(null,-1,tmpNode,false);
		    }else{
		    	treeObj.addNodes(nodes[0],-1,tmpNode,false);
		    }

		    var node = {}
		    switch(tmpNode.type){
		    case "module":
		    	node = treeObj.getNodeByParam("mId", tmpNode.mId, nodes[0]);
		    	break;
		    case "api":
		    	node = treeObj.getNodeByParam("aId", tmpNode.aId, nodes[0]);
		    	break;
		    case "case":
		    	node = treeObj.getNodeByParam("cId", tmpNode.cId, nodes[0]);
		    	break;
		    }
		    treeObj.selectNode(node,false,true);
		    treeObj.setting.callback.onClick(null, id, node);//触发函数
        },
        "addZTreeBrotherNode": function(data){
        	var id = this.attr("id");
 		    var tmpNode = setNodeData(data);;
 		    var parentNode = {};
		    var treeObj = $.fn.zTree.getZTreeObj(id);
		    var sNodes = treeObj.getSelectedNodes();
		    if (sNodes.length > 0) {
		    	parentNode = sNodes[0].getParentNode();
		    }
		    treeObj.addNodes(parentNode,-1,tmpNode,false);
		    
		    var node = {}
		    switch(tmpNode.type){
		    case "module":
		    	node = treeObj.getNodeByParam("mId", tmpNode.mId, parentNode);
		    	break;
		    case "api":
		    	node = treeObj.getNodeByParam("aId", tmpNode.aId, parentNode);
		    	break;
		    case "case":
		    	node = treeObj.getNodeByParam("cId", tmpNode.cId, parentNode);
		    	break;
		    }
		    treeObj.selectNode(node,false,true);
		    treeObj.setting.callback.onClick(null, id, node);//触发函数
        },
        "updateCurrentZTreeNode": function(text){
        	var id = this.attr("id");
        	var treeObj = $.fn.zTree.getZTreeObj(id);
        	var nodes = treeObj.getSelectedNodes();
        	if (nodes.length>0) {
        		nodes[0].name =  textlength_settting(text);
        		nodes[0].title= text;
        		nodes[0].alltext= text;
        		treeObj.updateNode(nodes[0]);
        	}
        },
        "getSelectedNodes": function(){
        	var id = this.attr("id");
        	var treeObj = $.fn.zTree.getZTreeObj(id);
        	var nodes = treeObj.getSelectedNodes();
        	return nodes;
        },
        "selectedNodes": function(node){
        	var id = this.attr("id");
        	var treeObj = $.fn.zTree.getZTreeObj(id);
    		treeObj.selectNode(node,false,true);
        },
        "removeNode": function(node){
        	var id = this.attr("id");
        	var treeObj = $.fn.zTree.getZTreeObj(id);
        	treeObj.removeNode(node);
        },
        "getCheckNodes": function(node){
        	var id = this.attr("id");
        	var treeObj = $.fn.zTree.getZTreeObj(id);
        	var nodes = treeObj.getCheckedNodes(true);
        	return nodes
        }
    });
	
	function setNodeData(data){
		tmpNode={};
		tmpNode["name"] = textlength_settting(data.name);
		tmpNode["alltext"] = data.name;
		tmpNode["title"] = data.name;
		tmpNode["mId"] = data.mId;
		tmpNode["aId"] = data.aId;
		tmpNode["parentId"] = data.parentId;
		tmpNode["cId"] = data.cId;
		tmpNode["pId"] = data.pId;
		tmpNode["type"] = data.type;
		tmpNode["method"] = data.method;
		if(tmpNode["type"] == "module"){
			tmpNode["isParent"] = true;
		}else{
			if("api" == tmpNode["type"]){
				tmpNode["isParent"] = true;
				tmpNode["icon"] = "/static/zTree/css/zTreeStyle/img/diy/3.png";
			}else{
				tmpNode["isParent"] = false;
				tmpNode["icon"] = "/static/zTree/css/zTreeStyle/img/diy/2.png";
			}
		}
		tmpNode["children"] = [];
		return tmpNode;
	}
	
	//默认参数
    var defaluts = {
        dataList: {},
        setting:{checkable: true}
    };
    //私有方法，检测参数是否合法
    function isValid(options) {
        return !options || (options && typeof options === "object") ? true : false;
    }
    
    function isEmpty(obj){
    	if(obj==undefined){
    		return true;
    	}
        for (var name in obj) 
        {
            return false;
        }
        return true;
    };
    
	function setJsonChild(data,node){
		if(isEmpty(data)||isEmpty(node)){
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
	
	function setNode(data,node){
		if(isEmpty(data)||isEmpty(node)){
			return false;
		}
		if(setJsonChild.mark){// 已经找到了父节点，直接返回
			return true;
		}
		var mark1 = (data.mId == node.parentId && "module"==data.type && ("module"==node.type||"api"==node.type))
		var mark2 = (data.aId == node.parentId && "case"==node.type)
		if(mark1 || mark2){
			data.children.push(node);
			setJsonChild.mark=true;
			return true;
		}else{
			setJsonChild(data.children,node);
		}
	}
	
    function textlength_settting(text,length = 200){
	    if(text.length > length){
		   return (text.substr(0,length) + ".."); 
	    }else{
		   return text;
	    }
    }
})(window.jQuery);