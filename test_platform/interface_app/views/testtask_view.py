from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from interface_app.models import TestTask, TestCase
from interface_app.extend.task_run import run_cases
import os 
import json
from interface_app.apps import TASK_PATH, RUN_TASK_FILE
from interface_app.extend.task_thread import TaskThread

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
        TaskThread(tid).new_run()
        return HttpResponseRedirect("/interface/task_manage")
    else:
        return HttpResponse("404")


# 如何去运行这些用例？--单元测试框架 + 数据驱动

# unittest + ddt
