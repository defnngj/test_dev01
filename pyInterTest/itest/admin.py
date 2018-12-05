# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib import admin

# Register your models here.
from django.contrib import admin
from itest.models.user import Users
from itest.models.token import Token
from itest.models.testSuite import TestSuiteModel
from itest.models.testCaseResult import TestCaseResultModel
from itest.models.testCase import TestCaseModel
from itest.models.taskHistory import TaskHistoryModel
from itest.models.task import TaskModel
from itest.models.requirement import RequirementModel
from itest.models.publicAssert import PublicAssertModel
from itest.models.project import Project
from itest.models.pickerValues import PickerValuesModel
from itest.models.globalValue import GlobalValuesModel
from itest.models.env import EnvModel
from itest.models.databaseSetting import DatabaseSettingModel
from itest.models.customizeAssert import CustomizeAssertModel
from itest.models.commonParmas import CommonParmasModel
from itest.models.apiDefine import ApiDefine
from itest.models.apiModules import ApiModules
 
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user','pwd')
admin.site.register(Users,UsersAdmin)

class TokenAdmin(admin.ModelAdmin):
    list_display = ('Token','expireDate',"user")
admin.site.register(Token,TokenAdmin)

class TestSuiteModelAdmin(admin.ModelAdmin):
    list_display = ('project','user',"name","dec","preSql","postSql","casesId","preRequirement","postRequirement")
admin.site.register(TestSuiteModel,TestSuiteModelAdmin)

class testCaseResultAdmin(admin.ModelAdmin):
    list_display = ('project','url',"method","parmasType","taskId","caseId","version","requestHead","requestCookie","requestBody","responseHead","responseCookie","responseBody","pickerValues","asserts","success","responseStatus","preSql","postSql")
admin.site.register(TestCaseResultModel,testCaseResultAdmin)

class TestCaseModelAdmin(admin.ModelAdmin):
    list_display = ('project','user',"name","dec","api","preRequirement","postRequirement","preSql","postSql","preAssert","otherAssert","sqlAssert","headerData","parmasData","dataType","valuePicker")
admin.site.register(TestCaseModel,TestCaseModelAdmin)

class TaskHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('taskId','taskName',"suiteId","envId","project","taskType","repeatDateTime","repeatType","status","successRate","nextResultVersion","lastResultVersion","lastRunningTime","lastRunningUser","lastRunningSuccessCount","lastRunningfailedCount","lastRunningResultIdList","lastRunningPreResultIdList")
admin.site.register(TaskHistoryModel,TaskHistoryModelAdmin)

class TaskModelAdmin(admin.ModelAdmin):
    list_display = ('name','suite',"env","project","taskType","repeatDateTime","repeatType","status","successRate","nextResultVersion","lastResultVersion","lastRunningTime","lastRunningUser","lastRunningSuccessCount","lastRunningfailedCount","lastRunningResultIdList","lastRunningPreResultIdList")
admin.site.register(TaskModel,TaskModelAdmin)

class RequirementModelAdmin(admin.ModelAdmin):
    list_display = ('case','sql',"pickerValue","type")
admin.site.register(RequirementModel,RequirementModelAdmin)

class PublicAssertModelAdmin(admin.ModelAdmin):
    list_display = ('project','name',"key","value","type")
admin.site.register(PublicAssertModel,PublicAssertModelAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','dec',"user","createTime","status")
admin.site.register(Project,ProjectAdmin)

class GlobalValuesModelAdmin(admin.ModelAdmin):
    list_display = ('project','env',"name","value","type")
admin.site.register(GlobalValuesModel,GlobalValuesModelAdmin)

class PickerValuesModelAdmin(admin.ModelAdmin):
    list_display = ('name','value',"expression")
admin.site.register(PickerValuesModel,PickerValuesModelAdmin)

class EnvModelAdmin(admin.ModelAdmin):
    list_display = ('project','name')
admin.site.register(EnvModel,EnvModelAdmin)

class DatabaseSettingModelAdmin(admin.ModelAdmin):
    list_display = ('project','env','host','user','psw','database','port','type','sshHost','sshUser','sshPsw','sshPort','sshKey')
admin.site.register(DatabaseSettingModel,DatabaseSettingModelAdmin)

class CustomizeAssertModelAdmin(admin.ModelAdmin):
    list_display = ('name','key','value','type','sql','sqlAssert','assertType')
admin.site.register(CustomizeAssertModel,CustomizeAssertModelAdmin)

class CommonParmasModelAdmin(admin.ModelAdmin):
    list_display = ('name','type','value','default','dec')
admin.site.register(CommonParmasModel,CommonParmasModelAdmin)

class ApiDefineAdmin(admin.ModelAdmin):
    list_display = ('module','project','user','name','url','method','dec','header','parmasType','parmas','parmasExample','responseStatus','responseType','response','responseExample')
admin.site.register(ApiDefine,ApiDefineAdmin)

class ApiModulesAdmin(admin.ModelAdmin):
    list_display = ('name','project','parentId')
admin.site.register(ApiModules,ApiModulesAdmin)