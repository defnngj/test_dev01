# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models

from itest.models.project import Project
import time

"""
用户表
"""
class TaskHistoryModel(models.Model):
    taskId = models.IntegerField(default=-1,blank=False,db_index=True)
    taskName = models.CharField(max_length=100,blank=False)
    suiteId = models.IntegerField(default=-1,blank=False)
    envId = models.IntegerField(default=-1,blank=False)
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
    lastRunningResult = models.TextField(default="")

    def __unicode__(self):
        return self.taskName
    
    def getDict(self):
        re = {}
        re["hId"] = self.id
        re["tId"] = self.taskId
        re["name"] = self.taskName
        re["suId"] = self.suiteId
        re["eId"] = self.envId
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
    
    def getChartData(self):
        re = {}
        re["lastRunningSuccessCount"] = self.lastRunningSuccessCount
        re["lastRunningfailedCount"] = self.lastRunningfailedCount
        tmptime = time.strptime(self.lastRunningTime, '%Y-%m-%d %H:%M:%S')
        re["lastRunningTime"] = time.strftime("%Y-%m-%d",tmptime);
        return re
    
    def getPreCaseResult(self):
        return []
    
    def getCaseResult(self):
        return []