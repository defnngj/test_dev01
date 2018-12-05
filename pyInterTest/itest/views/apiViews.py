# -*- coding: utf-8 -*-
'''
Created on 2017年8月4日

@author: anonymous
'''
from __future__ import unicode_literals

from django.shortcuts import render
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
import simplejson
import json

# from models import Users
# from models import Token
from itest.models.user import Users
from itest.models.token import Token
from itest.models.project import Project
from itest.models.apiModules import ApiModules
from itest.models.apiDefine import ApiDefine
from itest.models.testCase import TestCaseModel
from itest.models.task import TaskModel
from itest.models.testSuite import TestSuiteModel
from itest.models.taskHistory import TaskHistoryModel

from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# import datetime
from itest.util import globalVars


from itest.excuteHandle.apiDebug import RequestDebug
# import itest.excuteHandle.apiDebug

def apitest(request):
    token = request.COOKIES[globalVars.IToken]
    try:
        tokenObj = Token.objects.get(Token=token)
    except Token.DoesNotExist:
        globalVars.getLogger().error("token不存在")
        return HttpResponseRedirect(reverse('login'))
    else:
        userName= tokenObj.user.user
        userId = tokenObj.user.id
        return render(request, "apiIndextest.html",globalVars.responeContent("true", "success", {"userName":userName,"userId":userId}))

def apiPageIndex(request,pId):
    token = request.COOKIES[globalVars.IToken]
    try:
        tokenObj = Token.objects.get(Token=token)
        taskCount = TaskModel.objects.filter(project_id=int(pId)).count()
        apiCount = ApiDefine.objects.filter(project_id=int(pId)).count()
        caseCount = TestCaseModel.objects.filter(project_id=int(pId)).count()
        suiteCount = TestSuiteModel.objects.filter(project_id=int(pId)).count()
        tasks = TaskHistoryModel.objects.filter(project_id=int(pId))
        charts = []
        for i in tasks:
            charts.append(i.getChartData())
    except Token.DoesNotExist:
        globalVars.getLogger().error("token不存在")
        return HttpResponseRedirect(reverse('login'))
    else:
        data = {}
        data["userName"] = tokenObj.user.user
        data["userId"] = tokenObj.user.id
        data["task"] = taskCount
        data["api"] = apiCount
        data["case"] = caseCount
        data["suite"] = suiteCount
        data["pId"] = pId
        data["charts"] = json.dumps(charts)
        return render(request, "apiIndex.html",globalVars.responeContent("true", "success", data))


def addApiModule(request):  
    req = simplejson.loads(request.body)
    name = None
    pId = None
    parentId = None
    parentId_status = None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("parentId"):
        parentId=req["parentId"]
        if parentId!=None and parentId!="":
            parentId_status=True
    
    if not name or not pId or not parentId_status:
        globalVars.getLogger().error("名称和pId,parentId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        pro = Project.objects.get(pk=int(pId))
    except Project.DoesNotExist:
        globalVars.getLogger().error("pId不存在")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")   
    else:    
        try:
            mo = ApiModules.objects.create(name=name,project=pro,parentId=parentId)
        except Exception as e:
            globalVars.getLogger().error(u"新建模块失败："+CommonValueHandle.text2unicode(e.message))
            return HttpResponse(globalVars.responseJson("false", "新建模块失败"), content_type="application/json")
        else:
            content={}
            content["name"]=name
            content["pId"] = pId
            content["parentId"] = parentId
            content["mId"] = mo.id
            content["type"] = "module"
            return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")
            
def updateApiModule(request):
    req = simplejson.loads(request.body)
    name = None
    parentId = None
    mId=None
    parentId_status=None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("parentId"):
        parentId=req["parentId"]
        if parentId!=None and parentId!="":
            parentId_status=True
    if req.has_key("mId"):
        mId=req["mId"]
        
    if not mId:
        globalVars.getLogger().error("mId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        module = ApiModules.objects.get(pk=mId)
    except ApiModules.DoesNotExist:
        globalVars.getLogger().error("mId错误")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")   
    else:    
        try:
            if name:
                module.name=name
            if parentId_status:
                module.parentId=parentId
            module.save()
        except Exception as e:
            globalVars.getLogger().error(u"修改模块失败："+CommonValueHandle.text2unicode(e.message))
            return HttpResponse(globalVars.responseJson("false", "修改模块失败"), content_type="application/json")
        else:
            content={}
            content["name"]=name
            content["mId"] = mId
            content["parentId"] = parentId
            content["type"] = "module"
            return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")

def deleteApiModule(request):
    req = simplejson.loads(request.body)
    mId=None
    if req.has_key("mId"):
        mId=req["mId"]
        
    if not mId:
        globalVars.getLogger().error("mId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        module = ApiModules.objects.get(pk=mId)
    except Project.DoesNotExist:
        globalVars.getLogger().error("mId错误")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")   
    else:    
        try:
            module.delete()
        except Exception as e:
            globalVars.getLogger().error(u"删除模块失败："+CommonValueHandle.text2unicode(e.message))
            return HttpResponse(globalVars.responseJson("false", "删除模块失败"), content_type="application/json")
        else:
            return HttpResponse(globalVars.responseJson("true","",{}), content_type="application/json")


def getApiModules(request):

    req = simplejson.loads(request.body)
    pId = None

    if req["pId"]:
        pId=req["pId"]

    if not pId:
        globalVars.getLogger().error("pId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        pro = Project.objects.get(pk=int(pId))
    except Project.DoesNotExist:
        globalVars.getLogger().error("pId不存在")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")   
    else:
        try:
            moduleList = ApiModules.objects.filter(project=pro)
            apilist = ApiDefine.objects.filter(project=pro)
            caselist = TestCaseModel.objects.filter(project=pro)
        except Exception as e:
            globalVars.getLogger().error(u"查询模块数据失败："+CommonValueHandle.text2unicode(e.message))
            return HttpResponse(globalVars.responseJson("false", "查询失败"), content_type="application/json")   
        else:    
            content={}
            content["len"]=moduleList.count()+ apilist.count()
            datalist = []
            for p in moduleList:
                tmp={}
                tmp["name"] = p.name
                tmp["mId"] = p.id
                tmp["parentId"] = p.parentId
                tmp["pId"] = p.project.id
                tmp["type"] = "module"
                tmp["aId"] = -1
                tmp["cId"] = -1
                tmp["method"]="none"
                datalist.append(tmp)
            
            for i in apilist:
                tmp={}
                tmp["name"]=i.name
                tmp["aId"] = i.id
                tmp["mId"] = i.module.id
                tmp["method"]=i.method
                tmp["pId"] = i.project.id
                tmp["parentId"] = i.module.id
                tmp["type"] = "api"
                tmp["cId"] = -1
                datalist.append(tmp)
            
            for i in caselist:
                tmp={}
                tmp["name"]=i.name
                tmp["aId"] = i.api.id
                tmp["mId"] = -1
                tmp["method"]= "none"
                tmp["pId"] = i.project.id
                tmp["parentId"] = i.api.id
                tmp["type"] = "case"
                tmp["cId"] = i.id
                datalist.append(tmp)
                
            content["data"] = datalist
            return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")

def addApi(request):
    req = simplejson.loads(request.body)
    pId = None
    mId = None
    uId = None
    name=None
    dec=None
    method=None
    url=None
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("mId"):
        mId=req["mId"]
    if req.has_key("uId"):
        uId=req["uId"]
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("dec"):
        dec=req["dec"]
    if req.has_key("method"):
        method=req["method"]
    if req.has_key("url"):
        url=req["url"]
    if not pId or not mId or not uId or not name or not dec or not method or not url:
        globalVars.getLogger().error("pId,mId,uId,name,dec,method,url不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        pro = Project.objects.get(pk=int(pId))
        user = Users.objects.get(pk=int(uId))
        module = ApiModules.objects.get(pk=int(mId))
    except (Project.DoesNotExist,Users.DoesNotExist,ApiModules.DoesNotExist) as e:
        globalVars.getLogger().error(u"参数有误："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json") 
    else:
        try:
            api = ApiDefine.objects.create(name=name,project=pro,user=user,module=module,dec=dec,method=method,url=url,parmasType="json",responseType="json")
        except Exception as e:
            globalVars.getLogger().error(u"创建api失败:"+CommonValueHandle.text2unicode(e.message))
            return HttpResponse(globalVars.responseJson("false", "创建接口失败"), content_type="application/json")   
        else:    
            data = {}
            data["aId"] = api.id
            data["pId"] = pId
            data["uId"] = uId
            data["mId"] = mId
            data["name"] = name
            data["dec"] = dec
            data["url"] = url
            data["type"] = "api"
            data["method"] = method
            return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")

def deleteApi(request):
    req = simplejson.loads(request.body)
    aId = None
    print("~~~~~~~~")
    print(req)
    print("6666666")

    if req.has_key("aId"):
        aId=req["aId"]
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        TestCaseModel.objects.filter(api=api).delete()
        api.delete()
    except Exception as e:
        globalVars.getLogger().error(u"删除api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除接口失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def getApiList(request):
    req = simplejson.loads(request.body)
    mId = None
    if req.has_key("mId"):
        mId=req["mId"]
    if not mId:
        globalVars.getLogger().error("mId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        module = ApiModules.objects.get(pk=int(mId))
    except ApiModules.DoesNotExist:
        globalVars.getLogger().error("模块mId不存在")
        return HttpResponse(globalVars.responseJson("false", "模块不存在"), content_type="application/json")
    else:
        try:
            apilist = ApiDefine.objects.filter(module=module)
        except Exception as e:
            globalVars.getLogger().error(u"数据库查询失败："+CommonValueHandle.text2unicode(e.message))
            return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
        else:
            context={}
            data=[]
            for i in apilist:
                tmp={}
                tmp["aId"] = i.id
                tmp["name"]=i.name
                tmp["method"]=i.method
                tmp["type"] = "api"
                data.append(tmp)
            context["length"] = apilist.count()
            context["data"] = data
            return HttpResponse(globalVars.responseJson("true","",context), content_type="application/json")
        
def getApiDetail(request):
    req = simplejson.loads(request.body)
    aId = None
    if req.has_key("aId"):
        aId=req["aId"]
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
    except ApiModules.DoesNotExist:
        globalVars.getLogger().error("模块mId不存在")
        return HttpResponse(globalVars.responseJson("false", "模块不存在"), content_type="application/json")
    else:
        context={}
        context["aId"] = api.id
        context["mId"] = api.module.id
        context["pId"] = api.project.id
        context["uId"] = api.user.id
        context["name"] = api.name
        context["url"] = api.url
        context["method"] = api.method
        context["dec"] = api.dec
        context["header"] = api.getHeader()
        context["parmasType"] = api.parmasType
        context["parmas"] = api.getParmas()
        context["parmasExample"] = api.parmasExample
        context["responseStatus"] = api.responseStatus
        context["responseType"] = api.responseType
        context["response"] = api.getResponse()
        context["responseExample"] = api.responseExample
        return HttpResponse(globalVars.responseJson("true","",context), content_type="application/json")

def updateApiName(request):
    req = simplejson.loads(request.body)
    aId = None
    name = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("name"):
        name=req["name"]
        
    if not aId or not name:
        globalVars.getLogger().error("aId或者name不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        api.name = name
        api.save()
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateApiUrl(request):
    req = simplejson.loads(request.body)
    aId = None
    url = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("url"):
        url=req["url"]
        
    if not aId or not url:
        globalVars.getLogger().error("aId或者url不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        api.url = url
        api.save()
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateApiDec(request):
    req = simplejson.loads(request.body)
    aId = None
    dec = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("dec"):
        dec=req["dec"]
        
    if not aId or not dec:
        globalVars.getLogger().error("aId或者dec不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        api.dec = dec
        api.save()
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateApiMethod(request):
    req = simplejson.loads(request.body)
    aId = None
    method = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("method"):
        method=req["method"]
        
    if not aId or not method:
        globalVars.getLogger().error("aId或者url不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        api.method = method
        api.save()
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改api失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateApiAddHeader(request):
    req = simplejson.loads(request.body)
    aId = None
#     print(req)
    if req.has_key("aId"):
        aId=req["aId"]
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.addHeader(req)
#         print(type(res))
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"添加api header失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "添加 header失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        data = {}
        data["aId"] = aId
        data["name"] = req["name"]
        data["value"] = req["value"]
        data["dec"] = req["dec"]
        data["hId"] = res.id
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")

def updateApiDelHeader(request):
    req = simplejson.loads(request.body)
    aId = None
    hId = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("hId"):
        hId=req["hId"]
        
    if not aId or not hId:
        globalVars.getLogger().error("aId或者hId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.delHeader(hId)
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"删除api Header失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "删除head失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateApiChangeHeader(request):
    req = simplejson.loads(request.body)
    aId = None
    hId = None
    direction = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("hId"):
        hId=req["hId"]
    if req.has_key("direction"):
        direction=req["direction"]
        
    if not aId or not hId or not direction:
        globalVars.getLogger().error("aId,hId,direction不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.changeHeader(direction,hId)
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"修改api Header顺序失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "修改heade失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api Header顺序失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改head失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateApiParmasType(request):
    req = simplejson.loads(request.body)
    aId = None
    parmasType = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("parmasType"):
        parmasType=req["parmasType"]
    if not aId or not parmasType:
        globalVars.getLogger().error("aId或者parmasType不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        api.parmasType = parmasType
        api.save()
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def updateApiAddParmas(request):
    req = simplejson.loads(request.body)
    aId = None
    if req.has_key("aId"):
        aId=req["aId"]
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.addParmas(req)
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"添加api parmas失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "修改参数失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        data = {}
        data["aId"] = aId
        data["name"] = req["name"]
        data["type"] = req["type"]
        data["dec"] = req["dec"]
        data["pId"] = res.id
        data["default"] = res.default
        data["value"] = res.value
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")

def updateApiDelParmas(request):
    req = simplejson.loads(request.body)
    aId = None
    pId = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("pId"):
        pId=req["pId"]
        
    if not aId or not pId:
        globalVars.getLogger().error("aId或者pId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.delParmas(pId)
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"删除api parmas失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "删除参数失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        data = {};
        data["delId"] = res;
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")

def updateApiChangeParmas(request):
    req = simplejson.loads(request.body)
    aId = None
    pId = None
    direction = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("direction"):
        direction=req["direction"]
        
    if not aId or not pId or not direction:
        globalVars.getLogger().error("aId,pId,direction不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.changeParmas(direction,pId)
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"修改api parmas："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "修改参数失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api parmas："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改参数失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateAPiSetParmas(request):
    req = simplejson.loads(request.body)
    aId = None
    if len(req) == 0:
        return HttpResponse(globalVars.responseJson("false", "数据为空"), content_type="application/json")
    if req[0].has_key("aId"):
        aId=req[0]["aId"] 
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.setParmas(req)
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"添加api parmas失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "更新参数失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "更新参数失败"), content_type="application/json")
    else:
        resList=[]
        for i in res:
            data = {}
            data["aId"] = api.id
            data["name"] = i.name
            data["type"] = i.type
            data["dec"] = i.dec
            data["pId"] = api.project.id
            data["default"] = i.default
            data["value"] = i.value
            resList.append(data)
        return HttpResponse(globalVars.responseJson("true","",resList), content_type="application/json")

def updateApiResponseType(request):
    req = simplejson.loads(request.body)
    aId = None
    responseType = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("responseType"):
        responseType=req["responseType"]
    if not aId or not responseType:
        globalVars.getLogger().error("aId或者responseType不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        api.responseType = responseType
        api.save()
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def updateApiAddResponse(request):
    req = simplejson.loads(request.body)
    aId = None
    if req.has_key("aId"):
        aId=req["aId"]
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.addResponse(req)
#         print(type(res))
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"添加api response失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "添加响应失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        data = {}
        data["aId"] = aId
        data["name"] = req["name"]
        data["type"] = req["type"]
        data["dec"] = req["dec"]
        data["rId"] = res.id
        data["default"] = res.default
        data["value"] = res.value
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")

def updateApiDelResponse(request):
    req = simplejson.loads(request.body)
    aId = None
    rId = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("rId"):
        rId=req["rId"]
        
    if not aId or not rId:
        globalVars.getLogger().error("aId或者rId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.delResponse(rId)
        if isinstance(res, unicode) or isinstance(res, str):
            return HttpResponse(globalVars.responseJson("false", u"删除api response失败："+CommonValueHandle.text2unicode(res)), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改参数失败"), content_type="application/json")
    else:
        data = {};
        data["delId"] = res
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")
    
def updateApiChangeResponse(request):
    req = simplejson.loads(request.body)
    aId = None
    rId = None
    direction = None
    if req.has_key("aId"):
        aId=req["aId"]
    if req.has_key("rId"):
        rId=req["rId"]
    if req.has_key("direction"):
        direction=req["direction"]
        
    if not aId or not rId or not direction:
        globalVars.getLogger().error("aId,pId,direction不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.changeResponse(direction,rId)
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"修改api parmas："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    except Exception as e:
        globalVars.getLogger().error(u"修改api parmas："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改接口失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def updateAPiSetResponse(request):
    req = simplejson.loads(request.body)
    aId = None
    if len(req) == 0:
        return HttpResponse(globalVars.responseJson("false", "数据为空"), content_type="application/json")
    if req[0].has_key("aId"):
        aId=req[0]["aId"] 
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        res = api.setResponse(req)
#         print(type(res))
        if isinstance(res, unicode) or isinstance(res, str):
            globalVars.getLogger().error(u"添加api parmas失败："+CommonValueHandle.text2unicode(res))
            return HttpResponse(globalVars.responseJson("false", "添加参数失败"), content_type="application/json")
    except Exception as e:
        return HttpResponse(globalVars.responseJson("false", u"修改api失败："+CommonValueHandle.text2unicode(e.message)), content_type="application/json")
    else:
        resList=[]
        for i in res:
            data = {}
            data["aId"] = api.id
            data["name"] = i.name
            data["type"] = i.type
            data["dec"] = i.dec
            data["rId"] = i.id
            data["default"] = i.default
            data["value"] = i.value
            resList.append(data)
        return HttpResponse(globalVars.responseJson("true","",resList), content_type="application/json")

def apiDebug(request):
    req = simplejson.loads(request.body)
    r = ""
    method = ""
    header = {}
    parmasType = ""
    form = []
    json = {}

    try:
        r=req["url"]
    except KeyError:
        r = ""

    try:
        method=req["method"]
    except KeyError:
        method = ""

    try:
        header=req["header"]
    except KeyError:
        header = {}

    try:
        parmasType=req["parmasType"]
    except KeyError:
        parmasType = ""

    try:
        form=req["form"]
    except KeyError:
        form = {}

    try:
        json=req["json"]
    except KeyError:
        json = {}

    if not r or not method:
        globalVars.getLogger().error("url或者method不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        #api = ApiDefine.objects.get(pk=int(aId))
        debug = RequestDebug(r, method,header,parmasType,form,json)
        debug.send()
#         res = apiDebug.sendRequest(req)
    except Exception as e:
        globalVars.getLogger().error(u"debug请求失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "请求失败"), content_type="application/json")
    else:
        data = {}
        print(debug.getResponseBody())
        print(debug.getResponseHeader())
        print(debug.getRequest())
        data["body"] = debug.getResponseBody()
        data["head"] = debug.getResponseHeader()
        data["request"] = debug.getRequest()
        data["status"] = debug.getResponseStatus()
        return HttpResponse(globalVars.responseJson("true","",data), content_type="application/json")


def copyApi(request):
    req = simplejson.loads(request.body)
    aId = None
    if req.has_key("aId"):
        aId=req["aId"] 
    if not aId:
        globalVars.getLogger().error("aId不能为空")
        return HttpResponse(globalVars.responseJson("false", "参数错误"), content_type="application/json")
    try:
        api = ApiDefine.objects.get(pk=int(aId))
        newApi = api.cloneApi()
        newApi.save()
    except Exception as e:
        globalVars.getLogger().error(u"复制api失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "复制失败"), content_type="application/json")
    else:
        tmp={}
        tmp["name"]=newApi.name
        tmp["aId"] = newApi.id
        tmp["mId"] = newApi.module.id
        tmp["method"]=newApi.method
        tmp["pId"] = newApi.project.id
        tmp["parentId"] = newApi.module.id
        tmp["type"] = "api"
        tmp["cId"] = -1
        return HttpResponse(globalVars.responseJson("true","",tmp), content_type="application/json")   
