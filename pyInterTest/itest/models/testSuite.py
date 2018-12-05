# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json

from itest.models.requirement import RequirementModel
from itest.models.project import Project
from itest.models.user import Users
from itest.models.testCase import TestCaseModel
from itest.util import globalVars


"""
testSuite
"""
class TestSuiteModel(models.Model): 
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Users,blank=False, on_delete=models.CASCADE)
    
    name = models.CharField(u'名称',max_length=60,blank=False)
    dec = models.TextField(u'描述',default="")
    
    preSql = models.TextField(u'前置sql',default="")#前置sql语句
    postSql = models.TextField(u'后置sql',default="") #后置sql语句
    
#     preCases = models.TextField(default="")#前置前置case
#     valuePicker = models.TextField(default="")#前置case中的变量提取
    
    
    casesId = models.TextField(u'关联的案例id',default="") #关联的案例
    
    preRequirement = models.TextField(u'前置条件',default="[]") #前置条件
    postRequirement = models.TextField(u'后置条件',default="[]") #后置条件
    
    def getDict(self):
        re = {}
        re["name"]=self.name
        re["dec"] = self.dec
        re["pId"] = self.project.id
        re["uId"] = self.user.id
        re["suId"] = self.id
        re["preSql"] = self.preSql
        re["postSql"] = self.postSql
        
        re["cases"] = self.getCases()
        
        re["preRequirement"] = self.getPreRequirement()
        re["postRequirement"] = self.getPostRequirement()
        
#         try:
#             pre = json.loads(self.preRequirement)
#             if isinstance(pre,list):
#                 for i in pre:
#                     p = RequirementModel.objects.get(pk=int(i))
#                     re["preRequirement"].append(p.getDict())
#             else:
#                 re["preRequirement"] = []
#         except Exception:
#             re["preRequirement"] = []
#                 
#         try:  
#             post = json.dumps(self.postRequirement)
#             if isinstance(post,list):
#                 for i in post:
#                     p = RequirementModel.objects.get(pk=int(i))
#                     re["postRequirement"].append(p.getDict())
#             else:
#                 re["postRequirement"] = []
#         except Exception:
#             re["postRequirement"] = []
            
        return re
    
    def getCases(self):
        jsonData = []
        if self.casesId=="":
            jsonData = []
        else:
            jsonData = json.loads(self.casesId) 
        try:
            caseList = []
            for cId in jsonData:
                tcase = TestCaseModel.objects.get(pk=cId)
                caseList.append(tcase)  
        except Exception as e:
            globalVars.getLogger().error(e.message)
            return []
        else:
            dataList = []
            for case in caseList:
                dataList.append(case.getDict())
            return dataList
    
    def getRequirement(self,Commonfield):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return []
        com = getattr(self, Commonfield)
        re = []
        try:
            pre = json.loads(com)
            if isinstance(pre,list):
                for i in pre:
                    p = RequirementModel.objects.get(pk=int(i))
                    re.append(p.getDict())
            else:
                re = []
        except Exception:
            re = []
        return re
    def getPreRequirement(self):
        return self.getRequirement("preRequirement")
    def getPostRequirement(self):
        return self.getRequirement("postRequirement")
    
    def updateRequirement(self,rIds):
        try:  
            re = json.dumps(rIds)
            self.preRequirement = re
            self.save()
        except Exception as e:
            globalVars.getLogger().error(e.message)
            pass
        