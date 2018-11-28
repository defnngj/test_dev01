from django.shortcuts import render
from django.http import HttpResponse
from interface_app.models import TestTask

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

