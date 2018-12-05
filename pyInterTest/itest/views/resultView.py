# -*- coding: utf-8 -*-
'''
Created on 2017年9月15日

@author: anonymous
'''

from __future__ import unicode_literals

import simplejson

from itest.models.testCaseResult import TestCaseResultModel
from django.http import HttpResponse
from itest.util import globalVars
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle

def getTestCaseResult(request):  
    req = simplejson.loads(request.body)
    reId = None

    if req.has_key("rId"):
        reId=req["rId"]

    if not reId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")  
    try:
        result = TestCaseResultModel.objects.get(pk=int(reId))
    except Exception as e:
        globalVars.getLogger().error(u"获取结果失败："+CommonValueHandle.text2unicode(e.message))
        return HttpResponse(globalVars.responseJson("false", "获取结果失败"), content_type="application/json")
    else:
        return HttpResponse(globalVars.responseJson("true","",result.getDict()), content_type="application/json")


