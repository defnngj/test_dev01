# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
# from itest.models.apiDefine import ApiDefine


"""
公共参数定义
"""
class CommonParmasModel(models.Model):
    name = models.CharField(max_length=60,blank=False)
    type = models.CharField(max_length=60)
    value = models.TextField()
    default = models.TextField()
    dec = models.TextField()
#     api = models.ForeignKey(ApiDefine,blank=False, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.name
    
    def getDict(self):
        re={}
        re["comId"] = self.id
        re["name"] = self.name
        re["type"] = self.type
        re["value"] = self.value
        re["default"] = self.default
        re["dec"] = self.dec
        return re
        