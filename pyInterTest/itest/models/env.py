# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.project import Project

"""
环境
"""
class EnvModel(models.Model): 
    project = models.ForeignKey(Project,blank=False,db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=500,blank=False) #
    
    def __unicode__(self):
        return self.name
    
    def getDict(self):
        re = {}
        re["eId"] = self.id
        re["pId"] = self.project.id
        re["name"] = self.name
        return re