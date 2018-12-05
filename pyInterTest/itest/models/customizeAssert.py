# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models


"""
自定义 assert
"""
class CustomizeAssertModel(models.Model): 
    
    name = models.TextField(blank=False) #名称，名称不能为空
    key = models.TextField(default="")  #key，值可以为空，当值为空的时候，只判断key，不为空的时候，当做是json格式进行判断
    value = models.TextField(default="") #值
    type = models.IntegerField(default=0)#类型，0包含和 1不包含
    
    sql = models.TextField(default="") #值
    sqlAssert = models.TextField(default="") #值
    assertType = models.CharField(max_length=20,default="common") #sql 或者 common
    
    def __unicode__(self):
        return self.name
    
    def getDict(self):
        re = {}
        re["caId"] = self.id
        re["name"] = self.name
        re["key"] = self.key
        re["value"] = self.value
        re["type"] = self.type
        
        re["sql"] = self.sql
        re["sqlAssert"] = self.sqlAssert
        re["assertType"] = self.assertType
        return re
    
    def updateFromDict(self,obj):
        if obj.has_key("name"):
            self.name = obj["name"]
        if obj.has_key("key"):
            self.key = obj["key"]
        if obj.has_key("value"):
            self.value = obj["value"]
        if obj.has_key("type"):
            self.type = obj["type"]
        if obj.has_key("sql"):
            self.sql = obj["sql"]
        if obj.has_key("sqlAssert"):
            self.sqlAssert = obj["sqlAssert"]
        if obj.has_key("assertType"):
            self.assertType = obj["assertType"]
        self.save()
            