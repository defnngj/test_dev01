# -*- coding: utf-8 -*-
'''
Created on 2017年9月7日

@author: anonymous
'''

import requests
from itest.util import globalVars
# from itest.util import globalVars

class RequestDebug:
    def __init__( self, url, method,header,parmasType,form,json):
        self.url = url
        self.method = method
        self.header = header
        self.parmasType = parmasType
        self.form = form
        self.json = json
        self.formDeal = {}
        self.response = {}
        for i in form:
            print(i)
            if self.formDeal.has_key(i["name"]):#如果存在，则进行数组处理
                if isinstance(self.formDeal[i["name"]],list):#如果已经是数组，则直接追加
                    self.formDeal[i["name"]].append(i["value"])
                else:
                    tmp = self.formDeal[i["name"]]#如果不是数组，则创建数组，并且追加
                    self.formDeal[i["name"]] = []
                    self.formDeal[i["name"]].extend([tmp,i["value"]])
                     
            else:
                self.formDeal[i["name"]] = i["value"]
        print(self.formDeal)
# 
    def send(self):

        client = requests.session()
        client.keep_alive = False
        if "json" == self.parmasType:
            globalVars.getLogger().info("参数是json")
            globalVars.getLogger().info(str(self.url))
            globalVars.getLogger().info(str(self.header))
            globalVars.getLogger().info(str(self.json))
            
            if "get"==self.method:
                self.response = client.get(self.url,headers=self.header,params=self.json,timeout=20)
            elif "post"==self.method:
                self.response = client.post(self.url,headers=self.header,json=self.json,timeout=20)
            elif "put"==self.method:
                self.response = client.put(self.url,headers=self.header,json=self.json,timeout=20)
            elif "delete"==self.method:
                self.response = client.delete(self.url,headers=self.header,json=self.json,timeout=20)
            else:
                return {}
        else:
            globalVars.getLogger().info("参数是form")
            globalVars.getLogger().info(str(self.url))
            globalVars.getLogger().info(str(self.header))
            globalVars.getLogger().info(str(self.formDeal))
            
            if "get"==self.method:
                self.response = client.get(self.url,headers=self.header,params=self.formDeal,timeout=20)
            elif "post"==self.method:
                self.response = client.post(self.url,headers=self.header,data=self.formDeal,timeout=20)
            elif "put"==self.method:
                self.response = client.put(self.url,headers=self.header,data=self.formDeal,timeout=20)
            elif "delete"==self.method:
                self.response = client.delete(self.url,headers=self.header,data=self.formDeal,timeout=20)
            else:
                return {}
        return self.response
    
    def getResponseHeader(self):
        
        if(any(self.response)):
            r = {}
            for i in self.response.headers:
                r[i] = self.response.headers[i]
            return r
#             return globalVars.objTodict(self.response.headers)
        else:
            return {}
        
    def getResponseBody(self):
        if(any(self.response)):
            return self.response.text
        else:
            return {}
        
    def getResponseStatus(self):
        if(any(self.response)):
            return self.response.status_code
        else:
            return ""
    
    def getRequest(self):
        data = {}
        data["url"] = self.url
        data["head"] = self.header
        if("json" == self.parmasType):
            data["json"] = self.json
        else:
            data["form"] = self.formDeal
        data["parmasType"] = self.parmasType
        return data
    
    def __del__(self):
        class_name = self.__class__.__name__
        print(class_name,"销毁")
