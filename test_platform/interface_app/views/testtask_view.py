from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from interface_app.models import TestTask
from interface_app.extend.task_run import run_cases
import os 

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
        print(cases_list)
        # run_cases()  #运行函数
        os.system(
            "python3 D:/class_dev/test_dev_sample/test_platform/interface_app/extend/task_run.py")
        
        return HttpResponseRedirect("/interface/task_manage")
    else:
        return HttpResponse("404")

# 如何去运行这些用例？--单元测试框架 + 数据驱动

# unittest + ddt
