# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import json

from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponseRedirect

from itest.models.token import Token
from itest.models.project import Project
from itest.models.apiDefine import ApiDefine
from itest.models.task import TaskModel
from itest.util import globalVars
from itest.util import tools
from itest.models.daos.users_dao import UsersDao
from itest.models.daos.token_dao import TokenDao


# Create your views here.
def index(request):
    token = request.COOKIES[globalVars.IToken]

    token_obj = TokenDao.get_token_by_token(token)
    if token_obj is None:
        return HttpResponseRedirect(reverse('login'))

    user_name = token_obj.user.user
    user_id = token_obj.user.id
    content = globalVars.responeContent("true", "success", {"user_name": user_name, "user_id": user_id})
    return render(request, "index.html", content)
    # try:
    #     tokenObj = Token.objects.get(Token=token)
    #     projects = Project.objects.all()
    # except Token.DoesNotExist:
    #     return HttpResponseRedirect(reverse('login'))
    # else:
    #     userName = tokenObj.user.user
    #     userId = tokenObj.user.id
    #     datalist = []
    #     for p in projects:
    #         tmp = p.getDict()
    #         apicount = ApiDefine.objects.filter(project_id=int(p.id)).count()
    #         taskcount = TaskModel.objects.filter(project_id=int(p.id)).count()
    #         tmp["interCounts"] = apicount
    #         tmp["taskCounts"] = taskcount
    #         datalist.append(tmp)
    #     return render(request, "index.html", globalVars.responeContent("true", "success",
    #                                                                    {"userName": userName, "userId": userId,
    #                                                                     "projects": json.dumps(datalist)}))


# 登录请求
def login(request):
    """
    登录请求
    :param request:
    :return:
    """
    if request.method == "POST":
        req = tools.json_to_dict(request.body)
        user_name = tools.get_request_key(req, "user")
        pwd = tools.get_request_key(req, "pwd")

        if not user_name or not pwd:
            return tools.response_failed(u"账号或者密码不能为空")

        user = UsersDao.get_user(user_name, pwd)
        if user is None:
            return tools.response_failed(u"账号或者密码错误，请重新输入!")
        else:
            now_30 = datetime.datetime.now() + datetime.timedelta(days=30)  # token有效时间是30天
            new_token = globalVars.generateToken(user_name)  # 生成token

            token = TokenDao.get_token_by_user(user)
            re = False
            if token is None:
                re = TokenDao.create_token(user, new_token, now_30)
            else:
                cache.delete(token.Token)
                re = TokenDao.update_token(token, new_token, now_30)
            if not re:
                return tools.response_failed(u"数据库错误，登录失败")
            else:
                cache.set(token, now_30, settings.REDIS_TIMEOUT)
                return tools.response_by_json(
                    data={"token": new_token, "token_name": globalVars.IToken, "token_expird": 30})
    # get访问登录页面
    else:
        return render(request, "login.html")


def logout(request):
    """
     退出登录
    :param request:
    :return:
    """
    if not request.COOKIES.has_key(globalVars.IToken):
        return HttpResponseRedirect(reverse('login'))
    token = request.COOKIES[globalVars.IToken]
    TokenDao.del_token(token)
    cache.delete(token)
    return HttpResponseRedirect(reverse('login'))


def register(request):
    """
    注册请求
    :param request:
    :return:
    """
    if request.method == "POST":
        #req = tools.json_to_dict(request.body)
        #user_name = tools.get_request_key(req, "user")
        #pwd = tools.get_request_key(req, "pwd")
        user_name = request.POST.get("user", "")
        pwd = request.POST.get("pwd", "")
        if not user_name or not pwd:
            return tools.response_failed(u"账号或者密码不能为空")

        user = UsersDao.get_user_by_name(user_name)
        if user is None:
            token = globalVars.generateToken(user_name)
            date = datetime.datetime.now() + datetime.timedelta(days=30)
            new_user = UsersDao.create_user(user_name, pwd)
            if new_user is None:
                return tools.response_failed(u"创建账号失败")
            new_token = TokenDao.create_token(new_user, token, date)
            if new_token is None:
                return tools.response_failed(u"token创建失败")

            cache.set(token, new_token.expireDate, settings.REDIS_TIMEOUT)
            return tools.response_by_json(
                data={"token": token, "token_name": globalVars.IToken, "token_expird": 30})
        else:
            return tools.response_failed(u"账号已存在，请重新输入！")
    # 访问登录页面
    else:
        return render(request, "register.html", globalVars.responeContent("true", "访问注册页面成功", {}))


def user_setting_page(request):
    """
    个人设置页面
    :param request:
    :return:
    """
    token = request.COOKIES[globalVars.IToken]
    token_obj = TokenDao.get_token_by_token(token)
    if token_obj is None:
        return HttpResponseRedirect(reverse('login'))
    else:
        user_name = token_obj.user.user
        user_id = token_obj.user.id
        content = globalVars.responeContent("true", "success", {"user_name": user_name, "user_id": user_id})
        return render(request, "user_setting.html", content)


def reset_pwd(request):
    """
    修改密码
    :param request:
    :return:
    """
    req = tools.json_to_dict(request.body)
    name = tools.get_request_key(req, "name")
    old_pwd = tools.get_request_key(req, "old_pwd")
    new_pwd = tools.get_request_key(req, "new_pwd")
    user_id = tools.get_request_key(req, "user_id")

    if not name or not old_pwd or not new_pwd or not user_id:
        return tools.response_failed()

    user_obj = UsersDao.get_user_by_all(name, old_pwd, user_id)
    if user_obj is None:
        return tools.response_failed(u"账号或者密码错误，请重新输入!")

    re = UsersDao.update_user_pwd(user_obj, new_pwd)
    if re is None:
        return tools.response_failed(u"修改密码失败")
    return tools.response_by_json()
