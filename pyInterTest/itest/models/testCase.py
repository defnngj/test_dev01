# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.project import Project
from itest.models.user import Users
from itest.models.apiDefine import ApiDefine
from itest.models.publicAssert import PublicAssertModel
from itest.models.customizeAssert import CustomizeAssertModel
from itest.models.pickerValues import PickerValuesModel
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
# from itest.models.requirementModel import RequirementModel

import itest.models.requirement
#import requirement #这样的import方式是为了解决循环引用导致的无法执行的问题
# import project
import json
from itest.util import globalVars

"""
参数定义
"""
class TestCaseModel(models.Model):
#     module = models.ForeignKey(ApiModules,blank=False)
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Users,blank=False, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=60,blank=False)
    dec = models.TextField(default="")
    caseLabels = models.TextField(default="")#案例的标签
    
    api = models.ForeignKey(ApiDefine,blank=False,db_index=True, on_delete=models.CASCADE)
    
    preTestCase = models.TextField(default="") #前置用例,数组列表
    preValuePicker = models.TextField(default="") #前置用例的变量提取,数组列表
    preRequirement = models.TextField(default="[]") #前置条件
    
    postTestCase = models.TextField(default="") #后置用例,数组列表
    postRequirement = models.TextField(default="[]") #后置条件
    
    preSql = models.TextField(default="")#前置sql语句
    postSql = models.TextField(default="") #后置sql语句
    
    preAssert = models.TextField(default="")# 公共断言，一个id列表
    otherAssert = models.TextField(default="") #断言判断，可以有多个，一个id列表
    sqlAssert = models.TextField(default="") #sql断言判断，可以有多个，一个id列表
    
    #globalTestData = models.IntegerField() #存储的是这个测试用例全局的数据判断，也是默认的数据判断
    
    headerData = models.TextField(default="")#头部数据，json格式
    parmasData = models.TextField(default="")#参数数据，json格式
    dataType = models.IntegerField(default=1) #参数的数据格式,0代表json，1代表form
    valuePicker = models.TextField(default="")  #变量提取
    
    def __unicode__(self):
        return self.name
    
    def cloneCase(self):
        newCase = TestCaseModel()
        newCase.project=self.project
        newCase.user=self.user
        newCase.name=self.name
        newCase.dec=self.dec
        newCase.caseLabels=self.caseLabels
        newCase.api=self.api
        newCase.preTestCase=self.preTestCase
        newCase.preSql=self.preSql
        newCase.postTestCase=self.postTestCase
        newCase.postSql=self.postSql
        newCase.preAssert=self.preAssert
        newCase.otherAssert=self.otherAssert
        newCase.headerData=self.headerData
        newCase.parmasData=self.parmasData
        newCase.valuePicker=self.valuePicker
        newCase.dataType=self.dataType
        newCase.preValuePicker = self.preValuePicker
        newCase.sqlAssert = self.sqlAssert
        newCase.preRequirement = self.preRequirement
        newCase.postRequirement = self.postRequirement
        return newCase
    
    def getDict(self):
        content={}
        content["cId"] = self.id
        content["name"]= self.name
        content["dec"] = self.dec
        
        content["aId"] = self.api.id
        content["apiName"] = self.api.name
        content["apiMethod"] = self.api.method
        content["apiUrl"] = self.api.url
        content["apiHeader"] = self.api.getHeader()
        content["apiParmasType"] = self.api.parmasType
        content["apiParmas"] = self.api.getParmas()
                
        content["label"] = self.caseLabels
        content["preTestCase"] = self.preTestCase
        content["preSql"] = self.preSql
        content["postTestCase"] = self.postTestCase
        content["postSql"] = self.postSql
        
        content["preAssert"] = self.getPreAssert()
        content["sqlAssert"] = self.getSqlAssert()
        content["otherAssert"] = self.getOtherAssert()
        
#         publicAsserts = PublicAssertModel.objects.filter(project=self.project)
#         assertlist = []
#         for i in publicAsserts:
#             tmp={}
#             tmp["sId"] = i.id
#             tmp["name"] = i.name
#             assertlist.append(tmp)
        content["allPreAssert"] = self.getPublicAssert()
        
        content["headerData"] = self.headerData
        content["parmasData"] = self.parmasData
        content["dataType"] = self.dataType
        content["valuePicker"] = self.getValuePicker()
        
#         pre = json.loads(self.preRequirement)
#         if isinstance(pre,list):
#             for i in pre:
#                 p = requirement.RequirementModel.objects.get(pk=int(i))
#                 content["preRequirement"].append(p.getDict())
#                  
#                  
#         post = json.dumps(self.postRequirement)
#         if isinstance(post,list):
#             for i in post:
#                 p = requirement.RequirementModel.objects.get(pk=int(i))
#                 content["postRequirement"].append(p.getDict())
        
        content["preRequirement"] = self.getPreRequirement()
        content["postRequirement"] = self.getPostRequirement()
        return content
    
    def getPublicAssert(self):
        publicAsserts = PublicAssertModel.objects.filter(project=self.project)
        assertlist = []
        for i in publicAsserts:
            assertlist.append(i.getDict())
        return assertlist
    
    def getAssert(self,Commonfield):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return []
        com = getattr(self, Commonfield)
        
        re = []
        List = []
        if self.sqlAssert:
            try:
                re = json.loads(com)
            except Exception:
                re = []
            if not isinstance(re, list):
                re = []
        for i in re:
            try:
                a = CustomizeAssertModel.objects.get(pk=int(i))
            except Exception as e:
                globalVars.getLogger().error(i)
                globalVars.getLogger().error(e.message)
                continue
            else:
                List.append(a.getDict())
        return List
    
    def getSqlAssert(self):
        return self.getAssert("sqlAssert")

    def getOtherAssert(self):
        return self.getAssert("otherAssert")
    
    def getPreAssert(self):
        re = []
        try:
            re = json.loads(self.preAssert)
        except Exception:
            re = []
        return re

    def updateCommonAssertList(self,List,Commonfield):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return -1
        com = getattr(self, Commonfield)
        oldlist = []
        try:
            oldlist = json.loads(com)
        except Exception as e:
            globalVars.getLogger().error("json转换失败"+CommonValueHandle.text2str(e.message))
            oldlist = []
        
        try:
            for i in oldlist:
                a = CustomizeAssertModel.objects.get(pk=int(i))
                a.delete()
        except Exception as e:
            globalVars.getLogger().error(e.message)
        
        re = []
        for i in List:
            assertobj = CustomizeAssertModel()
            assertobj.updateFromDict(i)
            re.append(assertobj.id)
        try:
            setattr(self,Commonfield,json.dumps(re))
            self.save()
            return 0
        except Exception:
            return -1
            
    def updateSqlAssertList(self,List):
        return self.updateCommonAssertList(List,"sqlAssert")
        
    def updateOtherAssertList(self,List):
        return self.updateCommonAssertList(List,"otherAssert")
    
    def updatePreAssertList(self,List):
        re = "[]"
        try:
            re = json.dumps(List)
        except Exception:
            re = "[]"
        self.preAssert = re
        self.save()
    
    
    def getPreRequirement(self):
        re = []
        List = []
        try:
            List = json.loads(self.preRequirement)
        except Exception:
            List = []
        if isinstance(List,list):
            for i in List:
                try:
                    tmp = requirement.RequirementModel.objects.get(pk=int(i))
                    re.append(tmp.getDict());
                except Exception:
                    continue
        return re
    
    def updatePreRequirement(self,rIds):
        try:  
            re = json.dumps(rIds);
            self.preRequirement = re
            self.save()
        except Exception as e:
            globalVars.getLogger().error("json转换失败"+CommonValueHandle.text2str(e.message))
            pass
        
    def getPostRequirement(self):
        re = []
        List = []
        try:
            List = json.loads(self.postRequirement)
        except Exception:
            List = []
        if isinstance(List,list):
            for i in List:
                try:
                    tmp = requirement.RequirementModel.objects.get(pk=int(i))
                    re.append(tmp.getDict());
                except Exception:
                    continue
        return re
    
    def updatePostRequirement(self,rIds):
        try:  
            re = json.dumps(rIds);
            self.postRequirement = re
            self.save()
        except Exception as e:
            globalVars.getLogger().error("json转换失败"+CommonValueHandle.text2str(e.message))
            pass
        
    
#     def updatePreRequirement(self,List):
#         re = []
#         try:
#             re = json.loads(self.preRequirement)
#         except Exception:
#             re = []
#         for i in re:
#             try:
#                 tmp = requirement.RequirementModel.objects.get(pk=int(i))
#                 tmp.delete()
#             except Exception:
#                 continue
#         rIds = []
#         for j in List:
#             require = requirement.RequirementModel()
#             require.createFromDict(j)
#             rIds.append(require.id)
#         try:
#             re = json.dumps(self.rIds)
#             self.preRequirement = re
#             self.save()
#         except Exception:
#             pass
    
    def updateValuePicker(self,List):
        oldList = globalVars.str2List(self.valuePicker)
        for i in oldList:
            try:
                p = PickerValuesModel.objects.get(pk=int(i))
                p.delete()
            except Exception:
                pass
            
        if List and isinstance(List,list):
            re = []
            for o in List:
                try:
                    p = PickerValuesModel()
                    if o.has_key("name"):
                        p.name = o["name"]
                    if o.has_key("value"):
                        p.value = o["value"]
                    if o.has_key("expression"):
                        p.expression = o["expression"]
                    p.save()
                    re.append(p.id)
                except Exception as e:
                    globalVars.getLogger().error(e.message)
                    return
            self.valuePicker = globalVars.list2Str(re)
            self.save()
        else:
            return
    
    def getValuePicker(self):
        re = []
        List = globalVars.str2List(self.valuePicker)
        if isinstance(List,list):
            for i in List:
                try:
                    p = PickerValuesModel.objects.get(pk=int(i))
                    re.append(p.getDict())
                except Exception as e:
                    globalVars.getLogger().error("获取数据失败："+CommonValueHandle.text2str(e.message))
                    return []
        return re