# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''
from __future__ import unicode_literals

from django.db import models
from itest.models.user import Users
# from itest.models.apiDefine import ApiDefine
# from itest.models.task import TaskModel
import json


class Project(models.Model):
    """
    项目表
    """
    name = models.CharField(max_length=30,blank=False)
    dec = models.TextField()
    user = models.ForeignKey(Users,blank=False, on_delete=models.CASCADE)
    createTime = models.DateTimeField(blank=False)
    status = models.IntegerField(blank=False)#-1代表关闭，0代表已开启 1代表有任务

    def __unicode__(self):
        return self.name
    
    def to_json(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))
    
    def get_dict(self):
        tmp = dict()
        tmp["name"] = self.name
        tmp["dec"] = self.dec
        tmp["user_id"] = self.user.id
        tmp["user_name"] = self.user.user
        tmp["status"] = self.status
        tmp["project_id"] = self.id
        tmp["create_time"] = self.createTime.strftime('%Y-%m-%d %H:%M:%S')
        return tmp
    