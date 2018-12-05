# coding=utf-8
"""
Created on 2018年3月6日
@author: anonymous
"""
import logging
import simplejson
import traceback
import json
from django.http import HttpResponse
import requests


def json_to_dict(body):
    """
    把json数据转换为dict
    :param body: json格式数据
    :return: dict
    """
    print(body)
    re = None
    try:
        re = simplejson.loads(body)
    except Exception as e:
        traceback.print_exc()
        logging.error(e)
        re = {}
    return re


def get_request_key(req, key):
    """
    获取
    :param req: dict格式
    :param key: 关键字
    :return: data
    """
    re = None
    if key in req:
        re = req[key]
    return re


def response_by_json(success="true", message="", data={}):
    """
    ajax的请求的返回数据
    :param success: 结果
    :param message: 说明
    :param data: 详细数据
    :return:
    """
    content = dict()
    content["success"] = success
    content["message"] = message
    content["data"] = data
    return HttpResponse(json.dumps(content), content_type="application/json")


def response_failed(message=u"参数错误"):
    """
    响应失败
    :param message:
    :return:
    """
    return response_by_json("false", message, {})

logger = logging.getLogger(__name__)