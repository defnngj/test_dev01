
// 获取指定case_id的用例信息
var CaseInit = function (case_id) {
    
    //window.alert("abc")
    //document.write("<script language=javascript src='./jsProject.js'><\/script>");

    function getCaseInfo() {
        // 获取某个用例的信息
        $.post("/interface/get_case_info/", {
            "caseId": case_id,
        }, function (resp) {
            if (resp.success === "true") {
                let result = resp.data;
                console.log("结果", result);
                document.getElementById("req_name").value = result.name;
                document.getElementById("req_url").value = result.url;
                document.getElementById("req_header").value = result.reqHeader;
                document.getElementById("req_parameter").value = result.reqParameter;
                document.getElementById("assert_text").value = result.assertText;

                if (result.reqMethod === "post"){
                    document.getElementById("post").setAttribute("checked", "")
                }

                if (result.reqType === "json"){
                    document.getElementById("json").setAttribute("checked", "")
                }

                // window.alert(result.projectName);
                // window.alert(result.moduleName);

                // 初始化菜单
                ProjectInit('project_name', 'module_name', result.projectName, result.moduleName);

            }else{
                window.alert(resp.message);
            }
            //$("#result").html(resp);
        });
    }
    // 调用getCaseInfo函数
    getCaseInfo();

};


// 获取用例列表
var CaseListInit = function () {

    var options = "";
    function getCaseListInfo() {
        // 获取某个用例的信息
        $.get("/interface/get_case_list", {}, function (resp) {
            if (resp.success === "true") {
                console.log(resp.data);
                let cases = resp.data;
                for (let i = 0; i < cases.length; i++){
                    let option = '<input type="checkbox" name="' + cases[i].name 
                        + '" value="' + cases[i].id + '" /> ' + cases[i].name + '<br>'
                    
                    options = options + option;
                    
                }
                let devCaseList = document.querySelector(".caseList");
                devCaseList.innerHTML = options;

            } else {
                window.alert(resp.message);
            }
            //$("#result").html(resp);
        });
    }

    // 调用getCaseListInfo函数
    getCaseListInfo();

};


// 根据任务ID获取任务数据
var TaskInit = function (task_id) {

    var options = "";
    function getCaseListInfo() {
        // 获取某个任务的信息
        $.post("/interface/get_task_info/", {
            "taskId": task_id
        }, function (resp) {
            if (resp.success === "true") {
                console.log(resp.data);
                let result = resp.data;
                document.getElementById("taskName").value = result.name;
                document.getElementById("taskDescribe").value = result.describe;

                let cases = result.cases;
                for (let i = 0; i < cases.length; i++) {
                    var option = "";
                    if (cases[i].status === true){
                        option = '<input type="checkbox" checked="1"  name="' + cases[i].name
                            + '" value="' + cases[i].id + '" /> ' + cases[i].name + '<br>'
                    }else{
                        option = '<input type="checkbox"  name="' + cases[i].name
                            + '" value="' + cases[i].id + '" /> ' + cases[i].name + '<br>'
                    }
                    
                    options = options + option;

                }
                let devCaseList = document.querySelector(".caseList");
                devCaseList.innerHTML = options;

            } else {
                window.alert(resp.message);
            }
            //$("#result").html(resp);
        });
    }

    // 调用getCaseListInfo函数
    getCaseListInfo();

};