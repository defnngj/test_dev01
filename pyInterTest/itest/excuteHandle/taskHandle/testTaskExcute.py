# -*- coding: utf-8 -*- 
'''
Created on 2017年8月11日

@author: anonymous
'''

# from itest.models.testSuite import TestSuiteModel
from itest.models.task import TaskModel
from itest.models.user import Users
# from itest.models.databaseSetting import DatabaseSettingModel
from itest.excuteHandle.valueHandle.globalValueHandle import GlobalValueHandle
from itest.excuteHandle.dbHandle.mysqlHandleNew import MysqlHandleNew
from itest.excuteHandle.caseHandle.testCaseExcute import TestCaseExcute
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
from itest.util import globalVars
import time,json
# from itest.models.env import EnvModel
"""
任务执行器
"""
class TestTaskExcute:
    
    def __init__(self,tId,uId):
        self.uId = uId
        self.tId = tId
        self.task = None
        self.globalVars = {}
        self.runningVars = {}
        self.mysqlConn = None
        self.suite = None
        self.preRequirement = None
        self.preSql = None
        self.postSql = None
        self.cases = None
        self.success = 0
        self.failed = 0
        self.resultIds = []
        self.preResultIds = []
        self.mysqlHandle = None
        
    """
    执行sql
    """
    def __excuteSql(self,sql):
        sql = CommonValueHandle.valueReplace(sql,self.globalVars)
        sql = CommonValueHandle.valueReplace(sql,self.runningVars)
        return self.mysqlHandle.excuteSql(self.task.env, sql)
    
    def excute(self):
        
        ret = self.getTask()
        if(True != ret):
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，获取任务失败")
            globalVars.getLogger().error("获取任务失败"+ret)
            return "获取任务失败"+ret
        
        if(not self.getSuite()):
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，获取测试套件失败")
            globalVars.getLogger().error("获取测试套件失败")
            return "获取测试套件失败"
        
        
        ret = self.initGlobalVars()
        if isinstance(ret,str) or isinstance(ret,unicode):
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，初始化全局变量失败")
            globalVars.getLogger().error("初始化全局变量失败："+CommonValueHandle.text2str(ret))
            return "初始化全局变量失败："+CommonValueHandle.text2str(ret)
        
        ret = self.initMysqlConnect()
        if not ret:
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，数据库初始化失败,请检查mysql的设置")
            globalVars.getLogger().info("mysql 数据库初始化失败,请检查mysql的设置:"+CommonValueHandle.text2str(ret))
            return "mysql 数据库初始化失败,请检查mysql的设置:"+CommonValueHandle.text2str(ret)
           
        if(not self.doPreSql()):
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，执行前置sql失败，请检查sql语句")
            globalVars.getLogger().error("执行前置sql失败，请检查sql语句")
            return "执行前置sql失败，请检查sql语句"
#         
        ret = self.doSuitePreRequirement()
        if True !=ret:
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，前置条件执行失败，请检查是否正确")
            globalVars.getLogger().error("前置条件执行失败，请检查是否正确:"+CommonValueHandle.text2str(ret))
            return "前置条件执行失败，请检查是否正确:"+CommonValueHandle.text2str(ret)
            
        
        ret = self.doSuiteCase()
        if True !=ret:
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，案例执行失败")
            globalVars.getLogger().error("案例执行失败，请联系管理员:"+CommonValueHandle.text2str(ret))
            return "前置条件执行失败，请联系管理员:"+CommonValueHandle.text2str(ret)
         
        if(not self.doPostSql()):
            self.changeTaskStatus(-1)
            self.saveTaskLastResult("执行失败，执行后置sql失败，请检查sql语句")
            globalVars.getLogger().error("执行后置sql失败，请检查sql语句")
            return "执行后置sql失败，请检查sql语句"

        self.saveTaskLastResult("执行成功！")
        self.changeTaskStatus(1)
        return True
    
    def saveTaskLastResult(self,message):
        #关闭mysql连接
        self.closeMysqlConnect()
        
        self.saveTaskResult()
        self.task.lastRunningResult = message
        self.task.save()
        
    def getTask(self):
        try:
            self.task = TaskModel.objects.get(pk=int(self.tId))
        except Exception as e:
            return CommonValueHandle.text2str(e.message)
        else:
            return True
    
    def getSuite(self):
        self.suite = self.task.suite
        return self.suite
    
    #初始化全局变量
    def initGlobalVars(self):
        globalVars.getLogger().info("初始化全局变量")
        valueHandle = GlobalValueHandle()
        self.globalVars = valueHandle.getGlobalValue(self.task.env)
        return self.globalVars
    
    #初始化mysql连接
    def initMysqlConnect(self):
        globalVars.getLogger().info("正在连接数据库")
        self.mysqlHandle = MysqlHandleNew()
        return self.mysqlHandle
        # self.mysqlConn = self.mysqlHandle.getMysqlConnect(self.task.env)
        # return self.mysqlConn
    
    #关闭mysql连接
    def closeMysqlConnect(self):
        globalVars.getLogger().info("关闭数据库连接")
        if self.mysqlHandle:
            self.mysqlHandle.closeConn()
    
    #执行前置sql
    def doPreSql(self):
        self.preSql = str(self.suite.preSql).strip()
        globalVars.getLogger().info("执行前置sql条件："+str(self.preSql))
        if not self.preSql:
            return True
        else:
            return self.__excuteSql(self.preSql)
    
    #执行后置sql
    def doPostSql(self):
        self.postSql = str(self.suite.postSql).strip()
        globalVars.getLogger().info("执行后置sql条件："+str(self.postSql))
        if not self.postSql:
            return True
        else:
            return self.__excuteSql(self.postSql)
    
    #执行前置案例
    """
    如果执行错误，则直接停止
    """
    def doSuitePreRequirement(self):
        try:
            globalVars.getLogger().info("执行前置条件")
            self.preRequirement = self.suite.getPreRequirement()
            for i in self.preRequirement:
                te = TestCaseExcute(i["cId"],self.globalVars,self.runningVars,i["pickerValue"],self.task.env,-1,self.task.nextResultVersion)
                re = te.excute()
                if isinstance(re,str):
                    globalVars.getLogger().info("执行前置条件出现错误！"+CommonValueHandle.text2str(re))
                    return "执行前置条件出现错误！"+CommonValueHandle.text2str(re)
                reId = te.saveResult(self.task.id,"执行成功")
                self.preResultIds.append(reId)
        except Exception as e:
            globalVars.getLogger().err("前置案例执行失败："+CommonValueHandle.text2str(e.message))
            return CommonValueHandle.text2str(e.message)
        else:
            return True
            
    #执行案例
    """
    如果执行错误，不直接停止，继续执行下一个
    """
    def doSuiteCase(self):
        try:
            globalVars.getLogger().info("开始执行案例")
            self.cases = self.suite.getCases()
            for i in self.cases:
                globalVars.getLogger().info(" ")
                globalVars.getLogger().info("案例名称："+ CommonValueHandle.text2str(i["name"]))
                te = TestCaseExcute(i["cId"],self.globalVars,self.runningVars,[],self.task.env,0,self.task.nextResultVersion)
                re = te.excute()
                reId = -1
                if True != re:
                    globalVars.getLogger().info("执行案例出现错误！"+CommonValueHandle.text2str(re))
                    reId = te.saveResult(self.task.id,"执行案例出现错误！"+CommonValueHandle.text2str(re))
                    self.failed= self.failed+1
                else:
                    reId = te.saveResult(self.task.id,"执行成功")
#                     self.resultIds.append(reId)
                    if te.result > -1:
                        self.success= self.success+1
                    else:
                        self.failed= self.failed+1
                self.resultIds.append(reId)
        except Exception as e:
            globalVars.getLogger().err("案例执行失败："+CommonValueHandle.text2str(e.message))
            return CommonValueHandle.text2str(e.message)
        else:
            return True
            
    #保存前置案例
    def saveTaskResult(self):
        globalVars.getLogger().info("保存案例数据")
        try:
#             if 0==(self.success + self.failed):
#                 self.task.successRate = 0
#             else:
#                 success = float(self.success)
#                 failed = float(self.failed)
#                 rate = success / (success + failed)
#                 rate2 = round(rate,2) * 100 #保留2位小数
#                 self.task.successRate = int(rate2)
#                 
#             self.task.lastResultVersion = self.task.nextResultVersion
#             self.task.nextResultVersion = self.task.nextResultVersion+1
#             self.task.lastRunningfailedCount = self.failed
#             self.task.lastRunningSuccessCount = self.success
#    
            failed = 0
            if 0==(self.success + self.failed):
                self.task.successRate = 0
            else:
                success = float(self.success)
                tmps = self.suite.getCases()
                failed = len(tmps) - success
                rate = success / (success + failed)
                rate2 = round(rate,2) * 100 #保留2位小数
                self.task.successRate = int(rate2)
                
            self.task.lastResultVersion = self.task.nextResultVersion
            self.task.nextResultVersion = self.task.nextResultVersion+1
            self.task.lastRunningfailedCount = failed
            self.task.lastRunningSuccessCount = self.success
            
            try:
                u = Users.objects.get(pk=int(self.uId))
                self.task.lastRunningUser = u.user
            except Exception:
                self.task.lastRunningUser = "system"
                
            self.task.lastRunningTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.task.lastRunningResultIdList = json.dumps(self.resultIds)
            self.task.lastRunningPreResultIdList = json.dumps(self.preResultIds)
            self.task.save()
            
            self.task.createHistory()#保存历史数据
            return True
        except Exception as e:
            globalVars.getLogger().error("保存结果失败:"+CommonValueHandle.text2str(e.message))
            return False
        
    def changeTaskStatus(self,status):
        self.task.status = status
        self.task.save()
    