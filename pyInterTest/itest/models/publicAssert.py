# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
公共断言
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.project import Project


"""
public assert
"""
class PublicAssertModel(models.Model): 
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    name = models.TextField(blank=False) #名称，名称不能为空
    key = models.TextField(default="")  #key，值可以为空，当值为空的时候，只判断key，不为空的时候，当做是json格式进行判断
    value = models.TextField(default="") #值
    type = models.IntegerField(default=0)#类型，0包含和 1不包含
    
    def __unicode__(self):
        return self.name
    
    def getDict(self):
        re = {}
        re["sId"] = self.id
        re["pId"] = self.project.id
        re["name"] = self.name
        re["key"] = self.key
        re["value"] = self.value
        re["type"] = self.type
        return re