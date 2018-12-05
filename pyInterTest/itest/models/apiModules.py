# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.project import Project


"""
api模块表
"""
class ApiModules(models.Model):
    name = models.CharField(max_length=30,blank=False)
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    parentId= models.IntegerField(blank=False)
    def __unicode__(self):
        return self.name
    
    def getDict(self):
        re = {}
        re["name"] = self.name
        re["parentId"] = self.parentId
        re["pId"] = self.project.id
        re["mId"] = self.id
        return re
        
        