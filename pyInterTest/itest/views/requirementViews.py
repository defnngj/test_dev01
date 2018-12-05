# -*- coding: utf-8 -*-
'''
Created on 2017年9月28日

@author: anonymous
'''

from __future__ import unicode_literals

import simplejson

from itest.models.pickerValues import PickerValuesModel
from django.http import HttpResponse
from itest.util import globalVars
from itest.models.requirement import RequirementModel
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle

def addRequirement(request):
    req = simplejson.loads(request.body)
    cases = None
    if req.has_key("cases"):
        cases=req["cases"]
    if not cases:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        res = []
        for i in cases:
            require = RequirementModel.objects.create(case_id=i["cId"],type=i["type"])
            res.append(require.getDict())
    except Exception as e:
        globalVars.getLogger().error(u"新建前置条件失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "新建前置条件失败"), content_type="application/json")
    else:
        content={}
        content["requirements"]=res
        return HttpResponse(globalVars.responseJson("true","",content), content_type="application/json")
    
def deleteRequirement(request):
    req = simplejson.loads(request.body)
    rId = None
    if req.has_key("rId"):
        rId=req["rId"]
    if not rId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        require = RequirementModel.objects.get(pk=int(rId))
        #require.deleteAllPickerValue()
        require.delete()
    except Exception as e:
        globalVars.getLogger().error(u"删除前置条件失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除前置条件失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def requirementAddPicker(request):
    req = simplejson.loads(request.body)
    rId = None
    name = None
    value = None
    expression = None
    if req.has_key("rId"):
        rId=req["rId"]
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("value"):
        value=req["value"]
    if req.has_key("expression"):
        expression=req["expression"]
    if not rId or not value or not expression:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        picker = PickerValuesModel.objects.create(name=name,value=value,expression=expression)
        require = RequirementModel.objects.get(pk=int(rId))
        require.addPickerValue(picker.id);
    except Exception as e:
        globalVars.getLogger().error(u"新建变量提取失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "新建变量提取失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true","",picker.getDict()), content_type="application/json")
    
def requirementDeletePicker(request):
    req = simplejson.loads(request.body)
    rId = None
    vId = None
    if req.has_key("rId"):
        rId=req["rId"]
    if req.has_key("vId"):
        vId=req["vId"]

    if not rId or not vId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        picker = PickerValuesModel.objects.get(pk=int(vId))
        require = RequirementModel.objects.get(pk=int(rId))
        require.deletePickerValue(vId);
        picker.delete()
    except Exception as e:
        globalVars.getLogger().error(u"新建变量提取失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "新建变量提取失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true","",require.getDict()), content_type="application/json")
    
def requirementGetPicker(request):
    req = simplejson.loads(request.body)
    rId = None
    if req.has_key("rId"):
        rId=req["rId"]

    if not rId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        require = RequirementModel.objects.get(pk=int(rId))
    except Exception as e:
        globalVars.getLogger().error(u"新建变量提取失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "新建变量提取失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true","",require.getPickerValue()), content_type="application/json")