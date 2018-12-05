# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.project import Project
from itest.models.env import EnvModel

"""
golbal values
"""
class GlobalValuesModel(models.Model): 
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    env = models.ForeignKey(EnvModel,blank=False, on_delete=models.CASCADE)
    name = models.TextField(blank=False) #名称，名称不能为空
    value = models.TextField(blank=False) #值，值可以为空，当值为空的时候，只判断name，不为空的时候，当做是json格式进行判断
    type = models.TextField(default="string") #类型，boolean,int, string 三种
    
    def __unicode__(self):
        return self.name
    
    def getDict(self):
        re = {}
        re["gId"] = self.id
        re["eId"] = self.env.id
        re["pId"] = self.project.id
        re["name"] = self.name
        re["value"] = self.value
        re["type"] = self.type
        return re