# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.project import Project
import json

"""
案例执行结果
"""
class TestCaseResultModel(models.Model): 
    project = models.ForeignKey(Project,blank=False, on_delete=models.CASCADE)
    
    url = models.TextField(default="")
    method = models.CharField(max_length=20,default="")
    parmasType = models.CharField(max_length=50,default="")
    
    taskId = models.IntegerField(default=-1,db_index=True)#任务的id
    caseId = models.IntegerField(default=-1)#案例的id
    
    version = models.IntegerField(default=-1,db_index=True)
    
    requestHead = models.TextField(default="")
    requestCookie = models.TextField(default="")
    requestBody = models.TextField(default="")
     
    responseHead = models.TextField(default="")
    responseCookie = models.TextField(default="")
    responseBody = models.TextField(default="")
     
    pickerValues = models.TextField(default="")
    asserts = models.TextField(default="")
     
    success = models.IntegerField(default=0) #-1代表失败，>-1代表成功
    
    responseStatus = models.CharField(max_length=10,default="200")
    
    preSql = models.TextField(default="")#前置sal
    postSql = models.TextField(default="")#后置sql
    
    message = models.TextField(default="执行完成")#后置sql
    
    def __unicode__(self):
        return str(self.taskId)
    
    def getDict(self):
        re = {}
        re["reId"] = self.id
        re["pId"] = self.project.id
        re["version"] = self.version
        try:
            re["requestHead"] = json.loads(self.requestHead)
        except:
            re["requestHead"] = []
        try:
            re["requestCookie"] = json.loads(self.requestCookie)
        except:
            re["requestCookie"] = []
        try:
            re["requestBody"] = json.loads(self.requestBody)
        except:
            re["requestBody"] = []  
        try:
            re["responseHead"] = json.loads(self.responseHead)
        except:
            re["responseHead"] = []
        try:
            re["responseCookie"] = json.loads(self.responseCookie)
        except:
            re["responseCookie"] = []
        re["responseBody"] = self.responseBody
        try:
            re["pickerValues"] = json.loads(self.pickerValues)
        except:
            re["pickerValues"] = []
        try:
            re["asserts"] = json.loads(self.asserts)
        except:
            re["asserts"] = []
        re["success"] = self.success
        re["preSql"]=self.preSql
        re["postSql"] = self.postSql
        re["tId"] = self.taskId
        re["url"] = self.url
        re["method"] = self.method
        re["parmasType"] = self.parmasType
        re["message"] = self.message
        return re
    
    def getDict2(self):
        re = {}
        re["reId"] = self.id
        re["pId"] = self.project.id
        re["version"] = self.version
        try:
            tmp = json.loads(self.requestHead)
        except:
            re["requestHead"] = []
        else:
            l = []
            for i in tmp:
                t = {}
                t["key"] = i
                t["value"] = tmp[i]
                l.append(t)
            re["requestHead"] = l
        
        try:
            tmp = json.loads(self.requestCookie)
        except:
            re["requestCookie"] = []
        else:
            l = []
            for i in tmp:
                t = {}
                t["key"] = i
                t["value"] = tmp[i]
                l.append(t)
            re["requestCookie"] = l
        
        if "json" ==self.parmasType:
            re["requestBody"] = str(self.requestBody)
        else:
            try:
                tmp = json.loads(self.requestBody)
            except:
                re["requestBody"] = []
            else:
                l = []
                for i in tmp:
                    t = {}
                    t["key"] = i
                    t["value"] = tmp[i]
                    l.append(t)
                re["requestBody"] = l
        
        try:
            tmp = json.loads(self.responseHead)
        except:
            re["responseHead"] = []
        else:
            l = []
            for i in tmp:
                t = {}
                t["key"] = i
                t["value"] = tmp[i]
                l.append(t)
            re["responseHead"] = l
        
        try:
            tmp = json.loads(self.responseCookie)
        except:
            re["responseCookie"] = []
        else:
            l = []
            for i in tmp:
                t = {}
                t["key"] = i
                t["value"] = tmp[i]
                l.append(t)
            re["responseCookie"] = l
            
        re["responseBody"] = self.responseBody
        try:
            tmp = json.loads(self.pickerValues)
        except:
            re["pickerValues"] = []
        else:
            l = []
            for i in tmp:
                t = {}
                t["key"] = i
                t["value"] = tmp[i]
                l.append(t)
            re["pickerValues"] = l
            
#         print re["pickerValues"]
        try:
            re["asserts"] = json.loads(self.asserts)
        except:
            re["asserts"] = []

        re["success"] = self.success
        re["preSql"]=self.preSql
        re["postSql"] = self.postSql
        re["tId"] = self.taskId
        re["url"] = self.url
        re["method"] = self.method
        re["parmasType"] = self.parmasType
        re["message"] = self.message
        return re