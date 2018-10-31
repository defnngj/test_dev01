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
                return HttpResponseRedirect('/manage/project_manage/')
            else:
                return render(request, "index.html",
                                        {"error": "用户名或者密码错误"})
    else:
        return render(request, "index.html")

# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 清楚用户登录状态
    response = HttpResponseRedirect('/')
    return response




"""
几个应用
user_app 用户登录、密码修改，基于用户的用例的展示
project_app 项目和模块
/manage/project_list
/manage/add_project
/manage/edit_project/1/
/manage/delete_project/1/

interface_app  接口用例，测试任务
/interface/add_testcase/
tools_app  测试工具
/tools/xxxx/


base.html
<html >
  <h1 > 新导航dddd < h1 >
   { % block content % }


   { % endblock % }
    <h1 > 底部公司信息 < h1 >
</html >


aaa.html
{ % extends "base.html" % }
{ % block content % }
  <p>中间的内容aaaa<p>
{ % endblock % }


bbb.html
{% extends "base.html" % }
{% block content % }
  <p > 中间的内容bbbbb< p >
{% endblock % }
"""
