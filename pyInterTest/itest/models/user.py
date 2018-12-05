# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals
from django.db import models


class Users(models.Model):
    """
    用户表
    """
    user = models.CharField(u'名称', max_length=30, blank=False)
    pwd = models.CharField(u'密码', max_length=20, blank=False)
    
    def __unicode__(self):
        return self.user
    
    def getDict(self):
        re = dict()
        re["user"] = self.user
        re["pwd"] = self.pwd
        re["uId"] = self.id
        return re

    def get_dict(self):
        re = dict()
        re["user"] = self.user
        re["pwd"] = self.pwd
        re["uId"] = self.id
        return re
