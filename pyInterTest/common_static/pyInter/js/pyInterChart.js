/**
 * author:anonymous
 */
//全局变量
var MorrisObj = null;

var HandleChartData = function(data){
	var dataList =  [];
	var tmpdata = {};
	for(var i=0;i<data.length;i++){
		var period = data[i].lastRunningTime;
		if(tmpdata.hasOwnProperty(period)){
			tmpdata[period]["lastRunningSuccessCount"] += data[i].lastRunningSuccessCount;
			tmpdata[period]["lastRunningfailedCount"] += data[i].lastRunningfailedCount;
			tmpdata[period]["count"] += 1;
		}else{
			tmpdata[period] = {"lastRunningSuccessCount":data[i].lastRunningSuccessCount,"lastRunningfailedCount":data[i].lastRunningfailedCount,"count":1}
		}
	}
	for(i in tmpdata){
		tmp = {};
		tmp["period"] = i;
		tmp["task"] = tmpdata[i].count;
		tmp["case"] = tmpdata[i].lastRunningSuccessCount+tmpdata[i].lastRunningfailedCount;
		if(0==tmp["case"]){
			tmp["rate"] = 0;
		}else{
			var n = (tmpdata[i].lastRunningSuccessCount / tmp["case"]) * 100
			n = n.toFixed(1);
			tmp["rate"] = n + "%";
		}
		dataList.push(tmp);
	}
	return dataList;
}

var InitChartData = function (data) {
//     morris chart
	var dataList = HandleChartData(data);
	MorrisObj = Morris.Area({
		element: 'hero-area',
		data: dataList,
		xkey: 'period',
		ykeys: ['task', 'case', 'rate'],
		labels: ['task', 'case', 'rate(%)'],
		hideHover: 'auto',
		lineWidth: 1,
		pointSize: 5,
		lineColors: ['#4a8bc2', '#ff6c60', '#a9d86e'],
		fillOpacity: 0.5,
		smooth: true
	});
//	Morris.Area({
//        element: 'hero-area',
//        data: [
//          {period: '2010 Q1', iphone: 2666, ipad: null, itouch: 2647},
//          {period: '2010 Q2', iphone: 2778, ipad: 2294, itouch: 2441},
//          {period: '2010 Q3', iphone: 4912, ipad: 1969, itouch: 2501},
//          {period: '2010 Q4', iphone: 3767, ipad: 3597, itouch: 5689},
//          {period: '2011 Q1', iphone: 6810, ipad: 1914, itouch: 2293},
//          {period: '2011 Q2', iphone: 5670, ipad: 4293, itouch: 1881},
//          {period: '2011 Q3', iphone: 4820, ipad: 3795, itouch: 1588},
//          {period: '2011 Q4', iphone: 15073, ipad: 5967, itouch: 5175},
//          {period: '2012 Q1', iphone: 10687, ipad: 4460, itouch: 2028},
//          {period: '2012 Q2', iphone: 8432, ipad: 5713, itouch: 1791}
//        ],
//
//          xkey: 'period',
//          ykeys: ['iphone', 'ipad', 'itouch'],
//          labels: ['iPhone', 'iPad', 'iPod Touch'],
//          hideHover: 'auto',
//          lineWidth: 1,
//          pointSize: 5,
//          lineColors: ['#4a8bc2', '#ff6c60', '#a9d86e'],
//          fillOpacity: 0.5,
//          smooth: true
//      });
//    $(function () {
//      // data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type
//      
//    });
    
}
var updateChartData = function(data){
	var dataList = HandleChartData(data);
	MorrisObj.setData(dataList);
}



var ChartHandle = (function () {
	main = {};
	main.get_statistics_data = function(){
		var callback=function(data){
			if(data["success"] == "true"|| data["success"] == true){
				$("#h1_chart_api_count").html(data.data["api"]);
				$("#h1_chart_case_count").html(data.data["case"]);
				$("#h1_chart_task_count").html(data.data["task"]);
				$("#h1_chart_suite_count").html(data.data["suite"]);
			}else{
				$.fail_prompt("执行任务失败："+data["message"],5000);
			}
		}
		$.requestJson("/statistics/summary","POST",{"pId":ProjectInfo.pId},callback);
	}
	
	main.get_chart_data = function(){
		var callback = function(data){
			if(data["success"] == "true"|| data["success"] == true){
				if(null==MorrisObj){
					InitChartData(data.data);
				}else{
					updateChartData(data.data);
				}
			}else{
			   $.fail_prompt("执行失败："+data["message"],5000);
		    }
		}
	 	$.requestJson("/statistics/chart","POST",{"pId":ProjectInfo.pId},callback);
	}
	$("#statistics_tab").on("click",function(){
		ChartHandle.get_statistics_data();
		ChartHandle.get_chart_data();
	});
	
	return main;
}());



