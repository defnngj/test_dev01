#coding=utf-8
'''
Created on 2017年7月31日

@author: anonymous
'''
import hashlib
import time
# import the logging library
import logging
import json
import types


# from models import Token
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from django.urls import reverse

IToken = "IToken"
Interval = 5 #定时任务的循环时间，单位是分钟

def isEmpty(data):
    if data==0:
        return False
    if not data:
        return False
    else:
        return True

# 生成token
def generateToken(name):
    now=time.time()
    data = name + str(now)
    data_bytes_utf8 = data.encode(encoding="utf-8")
    hash_md5 = hashlib.md5(data_bytes_utf8)
    return hash_md5.hexdigest()

#结果响应的结果样式
def responeContent(success="true",message="",data={}):
    content = {}
    content["success"] = success
    content["message"] = message
    content["data"] = data
#     content["userId"] = data.userId
#     content["userName"] = data.userName
    return content

def responseJson(success="true",message="",data={}):
    response_data = responeContent(success,message,data)
    return json.dumps(response_data)

def getLogger():  
    logger = logging.getLogger(__name__)
    return logger

def objTodict(obj):
    Dict = {}
    objdick = obj.__dict__.items()
    for i in objdick:
        d = getattr(obj, i)
        if not isinstance(d, types.FunctionType):
            Dict[i] = d
    return Dict

def str2Dict(s):
    Dict = {}
    try:
        Dict = json.loads(s)
    except Exception:
        Dict = {}
    return Dict

def str2List(s):
    Dict = []
    try:
        Dict = json.loads(s)
    except Exception:
        Dict = []
    return Dict

def dict2Str(obj):
    s = "{}"
    try:
        s = json.dumps(obj)
    except Exception:
        s = "{}"
    return s

def list2Str(obj):
    s = "[]"
    try:
        s = json.dumps(obj)
    except Exception:
        s = "[]"
    return s

logger = logging.getLogger(__name__)