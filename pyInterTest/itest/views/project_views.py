# -*- coding: utf-8 -*-
'''
Created on 2017年8月1日

@author: anonymous
'''

from __future__ import unicode_literals

import datetime
from itest.util import tools
from itest.models.daos.project_dao import ProjectDao
from itest.models.daos.users_dao import UsersDao


def get_project_list(request):
    """
    筛选项目
    :param request:
    :return:
    """
    req = tools.json_to_dict(request.body)
    status = tools.get_request_key(req, "status")
    user_id = tools.get_request_key(req, "user_id")
    exclude = tools.get_request_key(req, "exclude")
    if "true" == exclude:
        exclude = True
    else:
        exclude = False

    projects = ProjectDao.get_projects_list_exclude_status_user(status, user_id, exclude)
    content = dict()
    content["len"] = projects.count()
    content["data"] = ProjectDao.transform_projects_content(projects)
    return tools.response_by_json(data=content)
        

def add_project(request):
    """
    创建项目
    :param request:
    :return:
    """
    req = tools.json_to_dict(request.body)
    name = tools.get_request_key(req, "name")
    dec = tools.get_request_key(req, "dec")
    user_id = tools.get_request_key(req, "user_id")

    if (not name) or (not dec) or user_id is None:
        return tools.response_failed()

    user_obj = UsersDao.get_user_by_id(user_id)
    if user_obj is None:
        return tools.response_failed(u"查询用户失败")

    create_time = datetime.datetime.now()
    re = ProjectDao.create_project(name, dec, user_obj, create_time, 0)
    if not re:
        return tools.response_failed(u"创建项目失败")
    content = dict()
    content["name"] = name
    content["dec"] = dec
    content["user_id"] = user_id
    content["create_time"] = str(create_time)
    content["status"] = 0
    return tools.response_by_json(data=content)
        

def update_project(request):
    """
    创建项目
    :param request:
    :return:
    """
    req = tools.json_to_dict(request.body)
    name = tools.get_request_key(req, "name")
    dec = tools.get_request_key(req, "dec")
    project_id = tools.get_request_key(req, "project_id")
    if not name or not dec or project_id is None:
        return tools.response_failed()
    re = ProjectDao.update_project_base(project_id, name, dec)
    if not re:
        return tools.response_failed(u"修改项目失败")
    else:
        content = dict()
        content["name"] = name
        content["dec"] = dec
        content["pId"] = project_id
        return tools.response_by_json(data=content)


def close_project(request):
    """
    关闭项目
    :param request:
    :return:
    """
    req = tools.json_to_dict(request.body)
    status = tools.get_request_key(req, "status")
    project_id = tools.get_request_key(req, "project_id")

    if status is None or project_id is None:
        return tools.response_failed()
    re = ProjectDao.update_project_status(project_id, int(status))
    if not re:
        return tools.response_failed(u"关闭项目失败")
    else:
        content = dict()
        content["status"] = status
        content["project_id"] = project_id
        return tools.response_by_json(data=content)
