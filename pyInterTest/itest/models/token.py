# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.user import Users

"""
token表
"""
class Token(models.Model):
    Token = models.CharField(u'token',max_length=100,blank=False,db_index=True)
    expireDate = models.DateTimeField(u'过期时间',blank=False)
    user = models.ForeignKey(Users,blank=False, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.Token
    
    def getDict(self):
        re = {}
        re["token"] = self.Token
        re["expireDate"] = self.expireDate
        re["uId"] = self.user.id
        re["tId"] = self.id
        return re