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


# 退出登录
def logout(request):
    auth.logout(request)  # 清楚用户登录状态
    response = HttpResponseRedirect('/')
    return response




# 添加项目
@login_required
def add_project(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'project_manage.html', {'form': form})

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
