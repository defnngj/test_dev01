# -*- coding: utf-8 -*-
'''
Created on 2017年9月15日

@author: anonymous
'''

# from __future__ import unicode_literals  如果导入这个，代表文本使用unicode的编码

import simplejson

from itest.models.testSuite import Users
from itest.models.testSuite import Project
from itest.models.testSuite import TestSuiteModel
from django.http import HttpResponse
from itest.util import globalVars
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle

def addTestSuite(request):  
    req = simplejson.loads(request.body)
    pId = None
    uId = None
    name = None
    dec = None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("dec"):
        dec = req["dec"]
    if req.has_key("uId"):
        uId = req["uId"]
    
    if not name or not pId or not dec or not uId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        pro = Project.objects.get(pk=int(pId))
        u = Users.objects.get(pk=int(uId))
    except Project.DoesNotExist or Users.DoesNotExist:
        globalVars.getLogger().error("pId,uId 不存在")
        return HttpResponse(globalVars.responseJson("false", "项目或者用户不存在"), content_type="application/json")   
    else:    
        try:
            suite = TestSuiteModel.objects.create(name=name,project=pro,dec=dec,user=u)
        except Exception as e:
            globalVars.getLogger().error("新建测试套件失败："+CommonValueHandle.text2str(e.message))
            return HttpResponse(globalVars.responseJson("false", "新建测试套件失败"), content_type="application/json")
        else:
            return HttpResponse(globalVars.responseJson("true","",suite.getDict()), content_type="application/json")
        
def getTestSuite(request):  
    req = simplejson.loads(request.body)
    suId = None
    if req.has_key("suId"):
        suId = req["suId"]
    
    if not suId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
    except TestSuiteModel.DoesNotExist:
        globalVars.getLogger().error("suId 不存在")
        return HttpResponse(globalVars.responseJson("false", "测试套件 不存在"), content_type="application/json")   
    else:    
        return HttpResponse(globalVars.responseJson("true","",suite.getDict()), content_type="application/json")
    
def updateTestSuiteCases(request):  
    req = simplejson.loads(request.body)
    suId = None
    casesId = None
    
    if req.has_key("suId"):
        suId = req["suId"]
    if req.has_key("casesId"):
        casesId = req["casesId"]

    if not suId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
        suite.casesId = casesId
        suite.save()
    except Exception as e:
        globalVars.getLogger().error("编辑测试套件失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "编辑测试套件失败"), content_type="application/json")   
    else:    
        return HttpResponse(globalVars.responseJson("true","",suite.getDict()), content_type="application/json")
    
    
def updateTestSuitePre(request):  
    req = simplejson.loads(request.body)
    suId = None
    preSql = None
    if req.has_key("suId"):
        suId = req["suId"]
    if req.has_key("preSql"):
        preSql = req["preSql"]
    if not suId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
        suite.preSql = preSql
        suite.save()
    except Exception as e:
        globalVars.getLogger().error("编辑测试套件失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "编辑测试套件失败"), content_type="application/json")   
    else:    
        return HttpResponse(globalVars.responseJson("true","",suite.getDict()), content_type="application/json")

def updateTestSuitePost(request):  
    req = simplejson.loads(request.body)
    suId = None
    postSql = None
    if req.has_key("suId"):
        suId = req["suId"]
    if req.has_key("postSql"):
        postSql = req["postSql"]
    if not suId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
        suite.postSql = postSql
        suite.save()
    except Exception as e:
        globalVars.getLogger().error("编辑测试套件失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "编辑测试套件失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true","",suite.getDict()), content_type="application/json")
    
def deleteTestSuite(request):  
    req = simplejson.loads(request.body)
    suId = None
    
    if req.has_key("suId"):
        suId = req["suId"]

    if not suId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
        suite.delete()
    except Exception as e:
        globalVars.getLogger().error("删除测试套件失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除测试套件失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def getTestSuiteList(request):  
    req = simplejson.loads(request.body)

    try:
        pId = req["pId"]
    except KeyError:
        pId = None

    if not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        suiteList = TestSuiteModel.objects.filter(project_id=int(pId)) 
    except Exception as e:
        globalVars.getLogger().error("删除测试套件失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除测试套件失败"), content_type="application/json")   
    else:
        dataList = []
        for suite in suiteList: 
            content={}
            content["name"]=suite.name
            content["suId"] = suite.id
            content["dec"] = suite.dec
            dataList.append(content)
        return HttpResponse(globalVars.responseJson("true","",dataList), content_type="application/json")
    
def updateTestSuiteBaseInfo(request):  
    req = simplejson.loads(request.body)
    suId = None
    name = None
    dec = None
    if req.has_key("suId"):
        suId = req["suId"]
    if req.has_key("name"):
        name = req["name"]
    if req.has_key("dec"):
        dec = req["dec"]
    if not suId or not name or not dec:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
        suite.name=name
        suite.dec=dec
        suite.save()
    except Exception as e:
        globalVars.getLogger().error("更新测试套件失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "更新测试套件失败"), content_type="application/json")   
    else:
        content={}
        content["name"]=suite.name
        content["suId"] = suite.id
        content["dec"] = suite.dec
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")


def updateSuiteRequirement(request):
    req = simplejson.loads(request.body)
    suId = None
    rIds = None
    if req.has_key("suId"):
        suId=req["suId"]
    if req.has_key("rIds"):
        rIds = req["rIds"]
    
    if not suId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        if not rIds:
            rIds = []
        suite = TestSuiteModel.objects.get(pk=int(suId))
        suite.updateRequirement(rIds)
    except Exception as e:
        globalVars.getLogger().error("修改测试套件的前置条件失败："+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改测试套件的前置条件失败"), content_type="application/json")   
    else:
        content={}
        content["preRequirement"] = suite.getPreRequirement()
        content["suId"] = suite.id
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")