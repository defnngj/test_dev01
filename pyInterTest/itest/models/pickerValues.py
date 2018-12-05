# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''

from __future__ import unicode_literals

from django.db import models


"""
变量提取表
"""
class PickerValuesModel(models.Model):
    name = models.CharField(max_length=50)#名称
    value=models.CharField(max_length=50)#变量名称
    expression=models.CharField(max_length=500) #提取表达式
    
    def __unicode__(self):
        return self.name
    
    def getDict(self):
        re = {}
        re["vId"] = self.id
        re["name"] = self.name
        re["value"] = self.value
        re["expression"] = self.expression
        return re