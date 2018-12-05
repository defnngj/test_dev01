# -*- coding: utf-8 -*-
'''
Created on 2017年9月15日

@author: anonymous
'''

# from __future__ import unicode_literals

import simplejson,datetime

from itest.models.apiDefine import ApiDefine
from itest.models.testCase import TestCaseModel
from itest.models.testSuite import TestSuiteModel
from itest.models.task import TaskModel
from itest.models.taskHistory import TaskHistoryModel
from itest.util import globalVars
from django.http import HttpResponse
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle



def getSummary(request):  
    req = simplejson.loads(request.body)
    pId = None
    print("~~~~~~~~")
    print(req)
    print("6666666")
    if req.has_key("pId"):
        pId=req["pId"]

    if not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")  
    try:
        taskCount = TaskModel.objects.filter(project_id=int(pId)).count()
        apiCount = ApiDefine.objects.filter(project_id=int(pId)).count()
        caseCount = TestCaseModel.objects.filter(project_id=int(pId)).count()
        suiteCount = TestSuiteModel.objects.filter(project_id=int(pId)).count()
    except Exception as e:
        globalVars.getLogger().error("获取结果失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "获取结果失败"), content_type="application/json")
    else:
        data = {}
        data["task"] = taskCount
        data["api"] = apiCount
        data["case"] = caseCount
        data["suite"] = suiteCount
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")

def getChart(request):  
    req = simplejson.loads(request.body)
    pId = None

    print("~~~~~~~~")
    print(req)
    print("6666666")
    if req.has_key("pId"):
        pId=req["pId"]

    if not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")  
    try:
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=-30)
        n_days = now + delta
        tasks = TaskHistoryModel.objects.filter(project_id=int(pId),lastRunningTime__gt = n_days)
        data = []
        for i in tasks:
            data.append(i.getChartData())
    except Exception as e:
        globalVars.getLogger().error("获取结果失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "获取结果失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")

