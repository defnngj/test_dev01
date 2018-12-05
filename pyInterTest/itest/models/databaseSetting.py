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
class DatabaseSettingModel(models.Model): 
    project = models.ForeignKey(Project,blank=False, on_delete=models.CASCADE)
    env = models.ForeignKey(EnvModel,blank=False, on_delete=models.CASCADE)
    host = models.CharField(max_length=500,blank=False) #
    user = models.CharField(max_length=100,blank=False) #
    psw = models.CharField(max_length=100,blank=False) #
    database = models.CharField(max_length=100,blank=False)
    port = models.IntegerField(default=3306)
    type = models.CharField(max_length=50,default="mysql") #
    #下面这些作为保留使用，暂时不用ssh方式
    sshHost = models.CharField(max_length=500) #
    sshUser = models.CharField(max_length=100) #
    sshPsw = models.CharField(max_length=100) #
    sshPort = models.IntegerField(default=22)
    sshKey = models.CharField(max_length=500) #
    
    def __unicode__(self):
        return self.host
    
    def getDict(self):
        content={}
        content["pId"]=self.project.id
        content["eId"]=self.env.id
        content["host"]=self.host
        content["type"]=self.type
        content["user"]=self.user
        content["psw"]=self.psw
        content["port"]=self.port
        content["database"]=self.database
        
        content["sshHost"]=self.sshHost
        content["sshUser"]=self.sshUser
        content["sshPsw"]=self.sshPsw
        content["sshPort"]=self.sshPort
        content["sshKey"]=self.sshKey
        return content