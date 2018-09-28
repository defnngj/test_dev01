from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# 首页
def index(request):
    return render(request, "index.html")


# 处理登录请求
def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        
        if username == "" or password == "":
            return render(request, "index.html", 
                          {"error": "用户名或者密码为空"}
                         )
        else:
            user = auth.authenticate(username=username, password=password)  # 验证用户是不是存在
            
            if user is not None:
                auth.login(request, user) #记录用户登录状态
                request.session['user1'] = username
                return HttpResponseRedirect('/project_manage/')
            else:
                return render(request, "index.html",
                                        {"error": "用户名或者密码错误"})


@login_required #判断用户是否登录
def project_manage(request):
    username = request.session.get('user1', '')  # 读取浏览器 session
    return render(request, "project_manage.html", {"user": username})


# 退出登录
def logout(request):
    auth.logout(request)  # 清楚用户登录状态
    response = HttpResponseRedirect('/')
    return response
