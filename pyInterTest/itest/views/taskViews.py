# -*- coding: utf-8 -*-
'''
Created on 2017年9月15日

@author: anonymous
'''

# from __future__ import unicode_literals

import simplejson

from itest.models.project import Project
from itest.models.task import TaskModel

from itest.models.env import EnvModel
from django.http import HttpResponse
from itest.util import globalVars
from itest.models.testSuite import TestSuiteModel
from itest.excuteHandle.taskHandle.testTaskExcute import TestTaskExcute
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
from itest.models.taskHistory import TaskHistoryModel

import traceback
from django.core.mail import send_mail
from django.conf import settings


def addTask(request):  
    req = simplejson.loads(request.body)
    pId = None
    name = None
    suId = None
    eId = None
    taskType = None
    repeatDateTime = None
    repeatType = None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("suId"):
        suId=req["suId"]
    if req.has_key("eId"):
        eId=req["eId"]
    if req.has_key("taskType"):
        taskType=req["taskType"]
    if req.has_key("repeatDateTime"):
        repeatDateTime=req["repeatDateTime"]
    if req.has_key("repeatType"):
        repeatType=req["repeatType"]
    
    if not name or not pId or not suId or not eId or not taskType or not repeatDateTime or not repeatType:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")  
    try:
        task = TaskModel.objects.create(name=name,project_id=pId,suite_id=suId,env_id=eId,taskType=taskType,repeatDateTime=repeatDateTime,repeatType=repeatType)
    except Exception as e:
        globalVars.getLogger().error(u"新建任务失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "新建任务失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true","",task.getDict()), content_type="application/json")

def getTaskList(request):  
    req = simplejson.loads(request.body)
    pId = None
    if req.has_key("pId"):
        pId=req["pId"]
    
    if not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        tasklist = TaskModel.objects.filter(project_id=int(pId)).order_by("-repeatDateTime")
    except Project.DoesNotExist:
        globalVars.getLogger().error("pId不存在")
        return HttpResponse(globalVars.responseJson("false", "项目不存在"), content_type="application/json")   
    else:    
        re = []
        for i in tasklist:
            re.append(i.getDict())
        return HttpResponse(globalVars.responseJson("true","",re), content_type="application/json")
    
def getTask(request):  
    req = simplejson.loads(request.body)
    tId = None
    if req.has_key("tId"):
        tId=req["tId"]
     
    if not tId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        task = TaskModel.objects.get(pk=int(tId))
    except Project.DoesNotExist:
        globalVars.getLogger().error("pId不存在")
        return HttpResponse(globalVars.responseJson("false", "项目不存在"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true","",task.getDict()), content_type="application/json")
    
def deleteTask(request):  
    req = simplejson.loads(request.body)
    tId = None
    if req.has_key("tId"):
        tId=req["tId"]
    if not tId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        task = TaskModel.objects.get(pk=int(tId))
        task.delete()
    except Exception as e:
        globalVars.getLogger().error(u"删除任务失败:"+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除任务失败"), content_type="application/json")   
    else:    
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def updateTask(request):  
    req = simplejson.loads(request.body)
    tId = None
    name = None
    suId = None
    eId = None
    taskType = None
    repeatDateTime = None
    repeatType = None
    if req.has_key("tId"):
        tId=req["tId"]
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("suId"):
        suId=req["suId"]
    if req.has_key("eId"):
        eId=req["eId"]
    if req.has_key("taskType"):
        taskType=req["taskType"]
    if req.has_key("repeatDateTime"):
        repeatDateTime=req["repeatDateTime"]
    if req.has_key("repeatType"):
        repeatType=req["repeatType"]
    
    if not tId or not name or not suId or not eId or not taskType or not repeatDateTime or not repeatType:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        task = TaskModel.objects.get(pk=int(tId))
        task.name = name
        task.env = EnvModel.objects.get(pk=int(eId))
        task.suite = TestSuiteModel.objects.get(pk=int(suId))
        task.taskType = taskType
        task.repeatDateTime = repeatDateTime
        task.repeatType = int(repeatType)
        task.successRate = 0
        task.lastRunningTime = u""
        task.lastRunningUser = u""
        task.lastRunningSuccessCount = 0
        task.lastRunningfailedCount = 0
        task.lastResultVersion = -1
        task.lastRunningResult = u"未执行,无结果"
        task.save()
    except Exception as e:
        globalVars.getLogger().error(u"修改任务失败:"+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改任务失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true","",task.getDict()), content_type="application/json")    
    
def getCasesList(request):  
    req = simplejson.loads(request.body)
    tId = None
    if req.has_key("tId"):
        tId=req["tId"]
    
    if not tId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        task = TaskModel.objects.get(pk=int(tId))
        cases = task.getCases()
        
    except Exception as e:
        globalVars.getLogger().error(u"修改任务失败:"+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改任务失败"), content_type="application/json")
    else:
        re = {}
        re["cases"] = cases
        re["lastRunningSuccessCount"] = task.lastRunningSuccessCount
        re["lastRunningfailedCount"] = task.lastRunningfailedCount
        re["lastRunningTime"] = task.lastRunningTime
        re["lastRunningUser"] = task.lastRunningUser
        re["lastRunningResult"] = task.lastRunningResult
        re["preSql"] = task.getPreSql()
        re["postSql"] = task.getPostSql()
        re["preRequirement"] = task.getPreRequirement()
        return HttpResponse(globalVars.responseJson("true","",re), content_type="application/json")  

def runTask(request):
    req = simplejson.loads(request.body)
    tId = None
    uId = None
    if req.has_key("tId"):
        tId=req["tId"]
    if req.has_key("uId"):
        uId=req["uId"]
    if not tId or not uId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        task = TaskModel.objects.get(pk=int(tId))
        excute = TestTaskExcute(task.id, uId)
        ret = excute.excute()
        if True!=ret:
            globalVars.getLogger().error(u"执行任务失败:"+CommonValueHandle.text2unicode(ret))
            return HttpResponse(globalVars.responseJson("false", u"执行任务失败:"+CommonValueHandle.text2unicode(ret)), content_type="application/json") 
    except Exception as e:
        print(e)
        print(1)
        traceback
        globalVars.getLogger().error(u"执行任务失败:" + CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", u"执行任务失败:" + CommonValueHandle.text2unicode(e.message)), content_type="application/json")   
    else:


        new_task = TaskModel.objects.get(pk=int(tId))
        return HttpResponse(globalVars.responseJson("true","",new_task.getDict()), content_type="application/json")
    
def getTaskHistory(request):
    req = simplejson.loads(request.body)
    tId = None
    if req.has_key("tId"):
        tId=req["tId"]
    if not tId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        historys = TaskHistoryModel.objects.filter(taskId=int(tId)).order_by("-lastResultVersion")
    except Exception as e:
        globalVars.getLogger().error(u"查询历史数据失败:" + CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", u"查询历史数据失败:" + CommonValueHandle.text2unicode(e.message)), content_type="application/json")   
    else:
        data = []
        for t in historys:
            tmp = {}
            tmp["time"] = t.lastRunningTime
            tmp["hId"] = t.id
            tmp["version"] = t.lastResultVersion
            tmp["name"] = t.taskName
            data.append(tmp)
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")  
    
def getTaskHistoryReport(request):
    req = simplejson.loads(request.body)
    hId = None
    if req.has_key("hId"):
        hId=req["hId"]
    if not hId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        history = TaskHistoryModel.objects.get(pk=int(hId))
        suite = TestSuiteModel.objects.get(pk=int(history.suiteId))
        preSql = suite.preSql
        postSql = suite.postSql
    except Exception as e:
        globalVars.getLogger().error(u"查询历史数据失败:" + CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", u"查询历史数据失败:" + CommonValueHandle.text2unicode(e.message)), content_type="application/json")   
    else:
        data = {}
        data["preSql"] = preSql
        data["postSql"] = postSql
        data["preCases"] = history.getPreCaseResult()
        data["Cases"] = history.getCaseResult()
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")  