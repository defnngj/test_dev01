# -*- coding: utf-8 -*-
'''
Created on 2017年9月26日

@author: anonymous
'''

from __future__ import unicode_literals

from django.db import models
import json

from itest.models.testCase import TestCaseModel
from itest.models.pickerValues import PickerValuesModel

 
"""
条件表
"""
class RequirementModel(models.Model):
    case = models.ForeignKey(TestCaseModel,blank=False, on_delete=models.CASCADE)
    sql = models.TextField(default="")
    pickerValue = models.TextField(default="[]")
    type = models.CharField(max_length=30)#前置pre和后置post
    
    def __unicode__(self):
        return self.case.name
    
    def getPickerValue(self):
        if not self.pickerValue:
            return []
        else:
            res = []
            vIds = []
            try:
                vIds = json.loads(self.pickerValue)
            except Exception:
                vIds = []
            if isinstance(vIds,list):
                for vId in vIds:
                    p = PickerValuesModel.objects.get(pk=int(vId))
                    res.append(p.getDict())
                return res
            else:
                return []
    
    def addPickerValue(self,vId):
        tmp = []
        if self.pickerValue:
            try:
                tmp = json.loads(self.pickerValue)
            except Exception:
                tmp = []
            if not isinstance(tmp,list):
                tmp = []
        tmp.append(vId)
        self.pickerValue = json.dumps(tmp)
        self.save()
        
    def deletePickerValue(self,vId):
        tmp = []
        if self.pickerValue:
            try:
                tmp = json.loads(self.pickerValue)
            except Exception:
                tmp = []
            if not isinstance(tmp,list):
                tmp = []
        for i in tmp:
            if vId==i:
                tmp.remove(i)
                break
        self.pickerValue = json.dumps(tmp)
        self.save()
    
    def deleteAllPickerValue(self):
        tmp = []
        if self.pickerValue:
            try:
                tmp = json.loads(self.pickerValue)
            except Exception:
                tmp = []
            if not isinstance(tmp,list):
                tmp = []
        for i in tmp:
            try:
                v = PickerValuesModel.objects.get(pk=int(i))
                v.delete()
            except Exception:
                pass
            tmp.remove(i)
        self.pickerValue = json.dumps(tmp)
        self.save()
    
    def delete(self, using=None, keep_parents=False):
        self.deleteAllPickerValue()
        return models.Model.delete(self, using=using, keep_parents=keep_parents)
    
    def createFromDict(self,dicts):
        if(dict.has_key("cId")):
            self.case = TestCaseModel.objects.get(dicts["cId"])
        if(dict.has_key("type")):
            self.case = TestCaseModel.objects.get(dicts["type"])
        if(dict.has_key("pickerValue")):
            ps = dict.has_key("pickerValue")
            re = []
            for i in ps:
                p = PickerValuesModel
                if(i.has_key("name")):
                    p.name = i["name"]
                if(i.has_key("value")):
                    p.name = i["value"]
                if(i.has_key("expression")):
                    p.name = i["expression"]
                p.save()
                re.append(p.id)
            try:
                self.pickerValue = json.dumps(re)
            except Exception:
                pass
        self.save()
            
    
    def getDict(self):
        re = {}
        re["cId"] = self.case.id
        re["name"] = self.case.name
        re["sql"] = self.sql
        re["type"] = self.type
        re["rId"] = self.id
        re["pickerValue"] = self.getPickerValue()
        return re
    
    