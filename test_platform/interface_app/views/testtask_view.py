from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from interface_app.models import TestTask, TestCase
from interface_app.extend.task_run import run_cases
import os 
import json
from interface_app.apps import TASK_PATH, RUN_TASK_FILE


"""
说明：接口任务文件，返回HTML页面
"""

# 获取任务列表
def task_manage(request):
    testtasks = TestTask.objects.all()
    
    if request.method == "GET":
        return render(request, "task_manage.html", {
            "type": "list",
            "testtasks": testtasks,
        })
    else:
        return HttpResponse("404")


# 创建任务
def add_task(request):
    if request.method == "GET":
        return render(request, "add_task.html", {
            "type": "add",
        })
    else:
        return HttpResponse("404")


# 运行任务
def run_task(request, tid):
    if request.method == "GET":
        task_obj = TestTask.objects.get(id=tid)
        cases_list = task_obj.cases.split(",")
        cases_list.pop(-1)

        task_obj.status = 1   # 修改状态
        task_obj.save()

        
        print(cases_list)
        # run_cases()  #运行函数
        all_cases_dict = {}
        for case_id in cases_list:
            case_obj = TestCase.objects.get(id=case_id)
            case_dict = {
                "url": case_obj.url,
                "method": case_obj.req_method,
                "type_": case_obj.req_type,
                "header": case_obj.req_header,
                "parameter": case_obj.req_parameter,
                "assert_": case_obj.resp_assert
            } 
            all_cases_dict[case_obj.id] = case_dict

        print(all_cases_dict)

        cases_str = json.dumps(all_cases_dict)

        cases_data_file = TASK_PATH + "cases_data.json"
        print(cases_data_file)

        with open(cases_data_file, "w+") as f:
            f.write(cases_str)

        # 运行测试
        os.system("python3 " + RUN_TASK_FILE)
        
        return HttpResponseRedirect("/interface/task_manage")
    else:
        return HttpResponse("404")


# 如何去运行这些用例？--单元测试框架 + 数据驱动

# unittest + ddt
