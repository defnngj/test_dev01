# -*- coding: utf-8 -*-
'''
Created on 2017年9月12日

@author: anonymous
'''

from __future__ import unicode_literals


import simplejson

from itest.models.user import Users
from itest.models.apiDefine import ApiDefine
from itest.models.project import Project
from itest.models.testCase import TestCaseModel
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle



from django.http import HttpResponse
# import datetime
from itest.util import globalVars


def addCase(request):  
    req = simplejson.loads(request.body)
    name = None
    dec = None
    pId = None
    aId = None
    uId = None
    label = None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("dec"):
        dec = req["dec"]
    if req.has_key("aId"):
        aId = req["aId"]
    if req.has_key("uId"):
        uId = req["uId"]
    if req.has_key("label"):
        label = req["label"]
    
    if not name or not pId or not dec or not aId or not uId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        pro = Project.objects.get(pk=int(pId))
        u = Users.objects.get(pk=int(uId))
        a = ApiDefine.objects.get(pk=int(aId))
    except Project.DoesNotExist or Users.DoesNotExist or ApiDefine.DoesNotExist:
        globalVars.getLogger().error("pId,aId,uId 不存在")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")   
    else:    
        try:
            case = TestCaseModel.objects.create(name=name,project=pro,dec=dec,user=u,api=a,caseLabels=label)
        except Exception as e:
            globalVars.getLogger().error(u"新建模块失败："+CommonValueHandle.text2unicode(e.message))
            return HttpResponse(globalVars.responseJson("false", "新建模块失败"), content_type="application/json")
        else:
            content={}
            content["name"]=name
            content["dec"] = dec
            content["pId"] = pId
            content["aId"] = aId
            content["uId"] = uId           
            content["mId"] = -1
            content["parentId"] = aId
            content["type"] = "case"
            content["cId"] = case.id
            content["method"]="none"
            return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")
        
def caseDetail(request):
    req = simplejson.loads(request.body)
    cId = None

    if req.has_key("cId"):
        cId=req["cId"]

    if not cId:
        globalVars.getLogger().error("cId参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
    except TestCaseModel.DoesNotExist:
        globalVars.getLogger().error("cId查询不存在")
        return HttpResponse(globalVars.responseJson("false", "案例不存在"), content_type="application/json")   
    else:    
        return HttpResponse(globalVars.responseJson("true","",case.getDict()), content_type="application/json")

def updateCaseBaseInfo(request):
    req = simplejson.loads(request.body)
    cId = None
    name = None
    dec = None
    label = None

    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("dec"):
        dec=req["dec"]
    if req.has_key("label"):
        label=req["label"]
    if not cId:
        globalVars.getLogger().error("cId参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        if None!=name:
            case.name=name
        if None!=dec:
            case.dec = dec
        if None!=label:
            case.caseLabels = label
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改案例失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["name"]= name
        content["dec"] = dec
        content["label"] = label
        content["type"] = "case"
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")
    
def updateCaseHeader(request):
    req = simplejson.loads(request.body)
    cId = None
    headerData=None

    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("headerData"):
        headerData=req["headerData"]
    if not cId:
        globalVars.getLogger().error("cId参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.headerData = headerData
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改案例失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["headerData"]= headerData
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")

def updateCaseParmas(request):
    req = simplejson.loads(request.body)
    cId = None
    parmasData=None
    dataType=None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("parmasData"):
        parmasData=req["parmasData"]
    if req.has_key("dataType"):
        dataType=req["dataType"]
    if not cId:
        globalVars.getLogger().error("cId参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.parmasData = parmasData
        case.dataType = dataType
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改案例失败"), content_type="application/json")   
    else:
        content={}
        content["cId"] = case.id
        content["parmasData"]= parmasData
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")

def updateCasePicker(request):
    req = simplejson.loads(request.body)
    cId = None
    valuePicker=None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("valuePicker"):
        valuePicker=req["valuePicker"]
    if not cId:
        globalVars.getLogger().error("cId参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.updateValuePicker(valuePicker)
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改案例失败"), content_type="application/json")   
    else:    
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def updateCaseAssert(request):
    req = simplejson.loads(request.body)
    cId = None
    preAssert=None
    otherAssert=None
    sqlAssert = None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("preAssert"):
        preAssert=req["preAssert"]
    if req.has_key("otherAssert"):
        otherAssert=req["otherAssert"]
    if req.has_key("sqlAssert"):
        sqlAssert=req["sqlAssert"]
    if not cId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.updatePreAssertList(preAssert)
        case.updateSqlAssertList(sqlAssert)
        case.updateOtherAssertList(otherAssert)
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改case失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["otherAssert"]= case.getOtherAssert()
        content["preAssert"]= case.getPreAssert()
        content["sqlAssert"]=case.getSqlAssert()
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")
    
def updateCasePre(request):
    req = simplejson.loads(request.body)
    cId = None
    preCase=None
    preSql=None
    preValuePicker = None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("preCase"):
        preCase=req["preCase"]
    if req.has_key("preSql"):
        preSql=req["preSql"]
    if req.has_key("preValuePicker"):
        preValuePicker=req["preValuePicker"]
    if not cId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.preTestCase = preCase
        case.preSql = preSql
        case.preValuePicker = preValuePicker
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改case失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["preSql"]= preSql
        content["preCase"]= preCase
        content["preValuePicker"] = preValuePicker
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")
    
def updateCasePost(request):
    req = simplejson.loads(request.body)
    cId = None
    postCase=None
    postSql=None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("postCase"):
        postCase=req["postCase"]
    if req.has_key("postSql"):
        postSql=req["postSql"]
    if not cId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.postTestCase = postCase
        case.postSql = postSql
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改case失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["postSql"]= postSql
        content["postCase"]= postCase
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")

def deleteCase(request):
    req = simplejson.loads(request.body)
    cId = None
    if req.has_key("cId"):
        cId=req["cId"]
    if not cId:
        globalVars.getLogger().error("cId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.delete()
    except Exception as e:
        globalVars.getLogger().error(u"删除case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除case失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def copyCase(request):
    req = simplejson.loads(request.body)
    cId = None
    if req.has_key("cId"):
        cId=req["cId"]
    if not cId:
        globalVars.getLogger().error("cId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        newCase = case.cloneCase()
        newCase.save()
    except Exception as e:
        globalVars.getLogger().error(u"copy case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "copy案例失败"), content_type="application/json")
    else:
        tmp={}
        tmp["name"]=newCase.name
        tmp["aId"] = newCase.api.id
        tmp["mId"] = -1
        tmp["method"]= "none"
        tmp["pId"] = newCase.project.id
        tmp["parentId"] = newCase.api.id
        tmp["type"] = "case"
        tmp["cId"] = newCase.id
        return HttpResponse(globalVars.responseJson("true","",tmp), content_type="application/json")

def updateCasePreSql(request):
    req = simplejson.loads(request.body)
    cId = None
    preSql=None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("preSql"):
        preSql=req["preSql"]
    if not cId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.preSql = preSql
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改case失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["preSql"]= preSql
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")
    
def updateCasePreRequirement(request):
    req = simplejson.loads(request.body)
    cId = None
    rIds=None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("rIds"):
        rIds=req["rIds"]
    if not cId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.updatePreRequirement(rIds)
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改case失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["preRequirement"]= case.getPreRequirement()
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")

def updateCasePostSql(request):
    req = simplejson.loads(request.body)
    cId = None
    postSql=None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("postSql"):
        postSql=req["postSql"]
    if not cId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.postSql = postSql
        case.save();
    except Exception as e:
        globalVars.getLogger().error(u"修改case失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改case失败"), content_type="application/json")   
    else:    
        content={}
        content["cId"] = case.id
        content["postSql"]= postSql
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")

def updateCasePostRequirement(request):
    req = simplejson.loads(request.body)
    cId = None
    rIds = None
    if req.has_key("cId"):
        cId=req["cId"]
    if req.has_key("rIds"):
        rIds = req["rIds"]
    
    if not cId or not rIds:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        case = TestCaseModel.objects.get(pk=int(cId))
        case.updatePostRequirement(rIds)
    except Exception as e:
        globalVars.getLogger().error(u"修改案例套件的前置条件失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改案例套件的前置条件失败"), content_type="application/json")   
    else:
        content={}
        content["postRequirement"] = case.getPostRequirement()
        content["cId"] = case.id
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")