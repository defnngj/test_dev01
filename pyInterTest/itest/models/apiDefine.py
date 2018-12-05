# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.project import Project
from itest.models.apiModules import ApiModules
from itest.models.user import Users
from itest.util import globalVars
from itest.models.commonParmas import CommonParmasModel
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle

import json


"""
api定义表
"""
class ApiDefine(models.Model):
    module = models.ForeignKey(ApiModules,blank=False, on_delete=models.CASCADE)
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Users,blank=False, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=60,blank=False)
    url = models.CharField(max_length=600,blank=False)
    method = models.CharField(max_length=20,blank=False)
    dec = models.TextField()
    
    header = models.TextField()#一个数组，存储的是一个id列表
    parmasType= models.CharField(max_length=30)  #分为json类型和x-www-form-urlencoded类型
    parmas= models.TextField() #一个数组，存储的是一个id列表
    parmasExample= models.TextField() #根据 parmas 列表生成的数据结构，也可以自己构造
    
    responseStatus = models.CharField(max_length=20)
    responseType = models.CharField(max_length=30)  #分为json类型和text类型
    response = models.TextField()  #一个数组，存储的是一个id列表
    responseExample= models.TextField()  #根据 response 列表生成的数据结构，也可以自己构造
    
    def cloneApi(self):
        newApi=ApiDefine()
        newApi.module=self.module
        newApi.project=self.project
        newApi.user=self.user
        newApi.name=self.name
        newApi.url=self.url
        newApi.method=self.method
        newApi.dec=self.dec
        newApi.header=self.header
        newApi.parmasType=self.parmasType
        newApi.parmas=self.parmas
        newApi.parmasExample=self.parmasExample
        newApi.response=self.response
        newApi.responseExample=self.responseExample
        newApi.responseStatus=self.responseStatus
        newApi.responseType=self.responseType
        return newApi
    
    def getCommonData(self,Commonfield):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return Commonfield+"：没有这样的字段"
        com = getattr(self, Commonfield)
        jsonData = []
        if com=="" or com==None:
            jsonData = []
        else:
            jsonData = json.loads(getattr(self, Commonfield))

        if isinstance(jsonData,list):
            try:
                headList = CommonParmasModel.objects.filter(id__in=jsonData)
            except Exception as e:
                globalVars.getLogger().error(Commonfield+"查询失败", CommonValueHandle.text2str(e.message))
                return CommonValueHandle.text2str(e.message)
            else:
                res = []
                for j in jsonData:
                    for i in headList:
                        if j==i.id:
                            tmp = {}
                            tmp["name"] = i.name
                            tmp["default"] = i.default
                            tmp["value"] = i.value
                            tmp["aId"] = self.id
                            tmp["dec"] = i.dec
                            tmp["hId"] = i.id
                            tmp["pId"] = i.id
                            tmp["rId"] = i.id
                            tmp["type"] = i.type
                            res.append(tmp)
                return res
        else:
            globalVars.getLogger().error(Commonfield+"的数据格式不正确")
            return (Commonfield+"的数据格式不正确")
       
    def addCommonData(self,Commonfield,data):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return Commonfield+"：没有这样的字段"
        com = getattr(self, Commonfield)
        jsonData = []
        if com=="" or com==None:
            jsonData = []
        else:
            jsonData = json.loads(getattr(self, Commonfield))
        if isinstance(jsonData,list):
            try:
                newData = CommonParmasModel()
#                 newData.api=self
                if data.has_key("dec"):
                    newData.dec=data["dec"]
                if data.has_key("default"):
                    newData.default = data["default"]
                if data.has_key("type"):
                    newData.type=data["type"]
                if data.has_key("value"):
                    newData.value=data["value"]
                if data.has_key("name"):
                    newData.name=data["name"]
                else:
                    globalVars.getLogger().error("创建失败，header的名称不能为空")
                    return "header的名称不能为空" 
#                 print("newData")
                #print(newData)
                newData.save()
                jsonData.append(newData.id)
                setattr(self,Commonfield,json.dumps(jsonData))
                self.save()
            except Exception as e:
                globalVars.getLogger().error(Commonfield+"创建失败"+CommonValueHandle.text2str(e.message))
                return Commonfield+"创建失败"+CommonValueHandle.text2str(e.message)
            else:
                return newData
        else:
            globalVars.getLogger().error(Commonfield+"的数据格式不正确")
            return Commonfield+"的数据格式不正确"
    
    def setCommonData(self,Commonfield,dataList):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return Commonfield+"：没有这样的字段"
        com = getattr(self, Commonfield)
        jsonData = []
        oldJsonData = []
        if com=="" or com==None:
            oldJsonData = []
        else:
            oldJsonData = json.loads(getattr(self, Commonfield)) 
        try:
            if isinstance(oldJsonData,list):
                for i in oldJsonData:
                    CommonParmasModel.objects.get(pk=i).delete()
            res = []
            for data in dataList:
                newData = CommonParmasModel()
#                 newData.api=self
                if data.has_key("dec"):
                    newData.dec=data["dec"]
                if data.has_key("default"):
                    newData.default = data["default"]
                if data.has_key("type"):
                    newData.type=data["type"]
                if data.has_key("value"):
                    newData.value=data["value"]
                if data.has_key("name"):
                    newData.name=data["name"]
                else:
                    globalVars.getLogger().error("header的名称不能为空")
                    return "header的名称不能为空" 
    #                 print("newData")
    #                 print(newData)
                newData.save()
                #newData.pId=self.project.id
                res.append(newData)
                jsonData.append(newData.id)
            setattr(self,Commonfield,json.dumps(jsonData))
            self.save()
        except Exception as e:
            globalVars.getLogger().error(Commonfield+"创建失败"+CommonValueHandle.text2str(e.message))
            return Commonfield+"创建失败"+CommonValueHandle.text2str(e.message)
        else:
            return res
    
    def delCommonData(self,Commonfield,CommonId):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return Commonfield+"：没有这样的字段"
        com = getattr(self, Commonfield)
        jsonData = []
        if com=="" or com==None:
            jsonData = []
        else:
            jsonData = json.loads(getattr(self, Commonfield))                              
        if isinstance(jsonData,list):
            try:
                CommonId = int(CommonId)
                for i in jsonData:
                    if i==CommonId:
                        CommonParmasModel.objects.get(pk=CommonId).delete()
                        jsonData.remove(i)
                        setattr(self,Commonfield,json.dumps(jsonData))
                        self.save()
            except Exception as e:
                globalVars.getLogger().error(Commonfield+"删除失败"+CommonValueHandle.text2str(e.message))
                return Commonfield+"删除header失败:"+CommonValueHandle.text2str(e.message)
            else:
                return CommonId
        else:
            globalVars.getLogger().error(Commonfield+"的数据格式不正确")
            return Commonfield+"的数据格式不正确"
        
    def changeCommonDataTurn(self,Commonfield,direction,commonId):
        if not getattr(self, Commonfield) and getattr(self, Commonfield)!="":
            return Commonfield+"：没有这样的字段"
        com = getattr(self, Commonfield)
        jsonData = []
        if com=="" or com==None:
            jsonData = []
        else:
            jsonData = json.loads(getattr(self, Commonfield))                     
        if isinstance(jsonData,list):
            commonId = int(commonId)
            for i,v in enumerate(jsonData):
                if v==commonId:
                    if direction=="up":
                        if i!=0:
                            jsonData[i] = jsonData[i-1]
                            jsonData[i-1] = commonId
                    else:
                        if i!=(len(jsonData)-1):
                            jsonData[i] = jsonData[i+1]
                            jsonData[i+1] = v
            try:
                setattr(self,Commonfield,json.dumps(jsonData))
                self.save()
            except Exception as e:
                globalVars.getLogger().error(Commonfield+"删除失败"+CommonValueHandle.text2str(e.message))
                return Commonfield+"删除header失败:"+CommonValueHandle.text2str(e.message)
            else:
                return commonId
        else:
            globalVars.getLogger().error(Commonfield+"的数据格式不正确")
            return Commonfield+"的数据格式不正确"
    
    def getHeader(self):
        return self.getCommonData("header")
    
    def addHeader(self,header):
        return self.addCommonData("header", header)
    
    def delHeader(self,headId):
        return self.delCommonData("header", headId)
    
    def changeHeader(self,direction,commonId):
        return self.changeCommonDataTurn("header",direction,commonId)
        
    def getParmas(self):
        return self.getCommonData("parmas")
    
    def addParmas(self,data):
        return self.addCommonData("parmas", data)
    
    def setParmas(self,data):
        return self.setCommonData("parmas", data)
    
    def delParmas(self,parmasId):
        return self.delCommonData("parmas", parmasId)
    
    def changeParmas(self,direction,commonId):
        return self.changeCommonDataTurn("parmas",direction,commonId)
    
    def getResponse(self):
        return self.getCommonData("response")
    
    def addResponse(self,data):
        return self.addCommonData("response", data)
    
    def setResponse(self,data):
        return self.setCommonData("response", data)
    
    def delResponse(self,responseId):
        return self.delCommonData("response", responseId)
    
    def changeResponse(self,direction,commonId):
        return self.changeCommonDataTurn("response",direction,commonId)
    
    def __unicode__(self):
        return self.name
        