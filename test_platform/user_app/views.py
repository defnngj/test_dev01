from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# 主要代码逻辑
def index(request):
    return render(request, "index.html")


# 处理登录请求
def login_action(request):
    if request.method == "GET":
        username = request.GET.get("username")
        password = request.GET.get("password")

        if username == "" or password == "":
            return render(request, "index.html", 
                          {"error": "用户名或者密码为空"}
                         )


"""
django 的开发模式：
M    models.py
T    template HTML
V    views.py
"""
