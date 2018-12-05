# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.testSuite import TestSuiteModel
from itest.models.env import EnvModel
from itest.models.project import Project
from itest.models.testCaseResult import TestCaseResultModel
from itest.models.testCase import TestCaseModel
from itest.models.taskHistory import TaskHistoryModel
from itest.util import globalVars
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
import json

"""
任务表
"""
class TaskModel(models.Model):
    name = models.CharField(max_length=100,blank=False)
    suite = models.ForeignKey(TestSuiteModel,blank=False, on_delete=models.CASCADE)
    env = models.ForeignKey(EnvModel,blank=False, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    
    taskType = models.IntegerField(default=0)#0代表非定时任务，1代表是定时任务
    
    repeatDateTime = models.DateTimeField()
    repeatType = models.IntegerField(default=-1) #-1代表不重复，1代表每天，3代表每三天，7代表每周
    
    status = models.IntegerField(default=0) #0代表未运行，1代表运行中
    successRate = models.IntegerField(default=0) #成功率
    
    nextResultVersion = models.IntegerField(default=0) #代表下一次执行的结果的一个标识,就是一个版本号
    lastResultVersion = models.IntegerField(default=-1) #代表上一次执行的结果的一个标识,就是一个版本号
    
    lastRunningTime = models.CharField(max_length=100)#上次执行时间
    lastRunningUser = models.CharField(max_length=100)#上次执行人
    lastRunningSuccessCount = models.IntegerField(default=0)#上次成功的的数目
    lastRunningfailedCount = models.IntegerField(default=0)#上次失败的的数目
    
    lastRunningResultIdList = models.TextField(default="[]")#结果的id列表，用来跟case的id对应起来，本身的排序是跟测试套件里面的case 的排序一致
    lastRunningPreResultIdList = models.TextField(default="[]")#结果的id列表，用来跟precase的id对应起来，本身的排序是跟测试套件里面的case 的排序一致
    
    lastRunningResult = models.TextField(default="无结果")

    def __unicode__(self):
        return self.name
    
    def createHistory(self):
        try:
            history = TaskHistoryModel()
            
            history.taskId = self.id
            history.taskName = self.name
            history.suiteId = self.suite.id
            history.envId = self.env.id
            history.project = self.project
            
            history.taskType = self.taskType#0代表非定时任务，1代表是定时任务
            
            history.repeatDateTime = self.repeatDateTime
            history.repeatType = self.repeatType #-1代表不重复，1代表每天，3代表每三天，7代表每周
            
            history.status = self.status #0代表未运行，1代表运行中
            history.successRate = self.successRate #成功率
            
            history.nextResultVersion = self.nextResultVersion #代表下一次执行的结果的一个标识,就是一个版本号
            history.lastResultVersion = self.lastResultVersion #代表上一次执行的结果的一个标识,就是一个版本号
            
            history.lastRunningTime = self.lastRunningTime#上次执行时间
            history.lastRunningUser = self.lastRunningUser#上次执行人
            history.lastRunningSuccessCount = self.lastRunningSuccessCount#上次成功的的数目
            history.lastRunningfailedCount = self.lastRunningfailedCount#上次失败的的数目
            
            history.lastRunningResultIdList = self.lastRunningResultIdList#结果的id列表，用来跟case的id对应起来，本身的排序是跟测试套件里面的case 的排序一致
            history.lastRunningPreResultIdList = self.lastRunningPreResultIdList#结果的id列表，用来跟precase的id对应起来，本身的排序是跟测试套件里面的case 的排序一致
            
            history.lastRunningResult = self.lastRunningResult
            history.save()
        except Exception as e:
            globalVars.getLogger().error("历史数据保存失败:" + CommonValueHandle.text2str(e.message))
            pass
    
    def getDict(self):
        re = {}
        re["tId"] = self.id
        re["name"] = self.name
        re["suId"] = self.suite.id
        re["suName"] = self.suite.name
        re["eId"] = self.env.id
        re["eName"] = self.env.name
        re["pId"] = self.project.id
        re["repeatType"] = self.repeatType
        re["repeatDateTime"] = str(self.repeatDateTime)
        re["status"] = self.status
        re["taskType"] = self.taskType
        re["successRate"] = self.successRate
        re["nextResultVersion"] = self.nextResultVersion
        re["lastResultVersion"] = self.lastResultVersion
        re["lastRunningTime"] = self.lastRunningTime
        re["lastRunningUser"] = self.lastRunningUser
        re["lastRunningSuccessCount"] = self.lastRunningSuccessCount
        re["lastRunningfailedCount"] = self.lastRunningfailedCount
        re["lastRunningResultIdList"] = self.lastRunningResultIdList
        re["lastRunningPreResultIdList"] = self.lastRunningPreResultIdList
        re["lastRunningResult"] = self.lastRunningResult
        return re
    
    def getCases(self):
        casesId = []
        resultsId = []

        try:
            if not self.suite.casesId:
                casesId = []
            else:
                casesId = json.loads(self.suite.casesId) 
#             print casesId
            if not self.lastRunningResultIdList:
                resultsId = []
            else:
                resultsId = json.loads(self.lastRunningResultIdList)
        except Exception:
            casesId = []
            resultsId = []
        
        ret = []
        try:
            for index in range(len(casesId)):
                tmpcase = TestCaseModel.objects.get(pk=int(casesId[index]))
                tmpdict = tmpcase.getDict()
                tmpdict["rId"] = -1
                if index < len(resultsId):
                    try:
                        tmpresult = TestCaseResultModel.objects.get(pk=int(resultsId[index]),version=self.lastResultVersion)
                        if tmpresult.caseId == tmpcase.id:
                            tmpdict["rId"] = tmpresult.id
                            if (tmpresult.success > -1):
                                tmpdict["success"] = 1
                            else:
                                tmpdict["success"] = 0
                        else:
                            tmpdict["success"] = -1
                    except:
                        tmpdict["success"] = -1
                else:
                    tmpdict["success"] = -1
                ret.append(tmpdict)
        except Exception as e:
            globalVars.getLogger().error("获取案例数据失败:"+CommonValueHandle.text2str(e.message))
            return []
        else:
            return ret
    
    def getPreSql(self):
        return self.suite.preSql
    
    def getPostSql(self):
        return self.suite.postSql
    
    def getPreRequirement(self):
        requirements = []
        preResultIdList = []
        try:
#             print self.suite.preRequirement
            if not self.suite.preRequirement:
                requirements = []
            else:
                requirements = self.suite.getPreRequirement()
                
            if not self.lastRunningPreResultIdList:
                preResultIdList = []
            else:
                preResultIdList = json.loads(self.lastRunningPreResultIdList)
        except Exception:
            return []
        ret = []
        try:
            for index in range(len(requirements)):
                tmpcase = TestCaseModel.objects.get(pk=int(requirements[index]["cId"]))
                tmpdict = tmpcase.getDict()
                tmpdict["rId"] = -1
                if index < len(preResultIdList):
                    try:
                        tmpresult = TestCaseResultModel.objects.get(pk=int(preResultIdList[index]),version=self.lastResultVersion)
                        if tmpresult.caseId == tmpcase.id:
                            tmpdict["rId"] = tmpresult.id
                            if (tmpresult.success > -1):
                                tmpdict["success"] = 1
                            else:
                                tmpdict["success"] = 0
                        else:
                            tmpdict["success"] = -1
                    except:
                        tmpdict["success"] = -1
                else:
                    tmpdict["success"] = -1
                ret.append(tmpdict)
        except Exception as e:
            globalVars.getLogger().error("获取前置案例数据失败:"+CommonValueHandle.text2str(e.message))
            return []
        else:
            return ret
        