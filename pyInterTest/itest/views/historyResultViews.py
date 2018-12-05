# -*- coding: utf-8 -*-
'''
Created on 2017年9月15日

@author: anonymous
'''

# from __future__ import unicode_literals

# import simplejson,datetime
import json
from django.shortcuts import render
# from itest.models.apiDefine import ApiDefine
from itest.models.testCase import TestCaseModel
from itest.models.testSuite import TestSuiteModel
from itest.models.testCaseResult import TestCaseResultModel
from itest.models.taskHistory import TaskHistoryModel
from itest.util import globalVars

from django.http import HttpResponseRedirect
from django.urls import reverse
# from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle


def getHistoryResultPage(request,hId):
    try:
        task = TaskHistoryModel.objects.get(pk=int(hId))
    except Exception as e:
        globalVars.getLogger().error(e.message)
        return HttpResponseRedirect(reverse('index'))
    else:
        preResultIds = task.lastRunningPreResultIdList
        resultIds = task.lastRunningResultIdList
        data={}
        data["name"] = task.taskName
        data["version"] = task.lastResultVersion
        data["time"] = task.lastRunningTime
        data["preSql"] = __getSuitePresql(task.suiteId)
        data["postSql"] = __getSuitePostsql(task.suiteId)
        data["results"] = __getResultLists(resultIds)
        data["preResults"] = __getResultLists(preResultIds)
        data["message"] = task.lastRunningResult
        
        return render(request, "historyResult.html",globalVars.responeContent("true", "success",data))

def __getSuitePresql(suId):
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
    except Exception as e:
        globalVars.getLogger().error(e.message)
        return ""
    else:
        return suite.preSql
    
def __getSuitePostsql(suId):
    try:
        suite = TestSuiteModel.objects.get(pk=int(suId))
    except Exception as e:
        globalVars.getLogger().error(e.message)
        return ""
    else:
        return suite.postSql
    
def __getResultLists(rIdsStr):
    try:
        rIds = json.loads(rIdsStr)
        ret = []
#         print results
        results = TestCaseResultModel.objects.filter(id__in=rIds)
        for i in results:
            tmp = i.getDict2()
            cId = i.caseId
            cases = TestCaseModel.objects.filter(pk=int(cId))
            if(0==len(cases)):
                tmp["caseName"] = "已删除"
            else:
                tmp["caseName"] = cases[0].name
            ret.append(tmp)
    except Exception as e:
        globalVars.getLogger().error(e.message)
        return []
    else:
        return ret