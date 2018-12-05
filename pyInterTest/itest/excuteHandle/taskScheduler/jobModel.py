#coding=utf-8
'''
Created on 2017年8月11日

@author: anonymous
'''
from itest.excuteHandle.taskHandle.testTaskExcute import TestTaskExcute
from itest.util import globalVars
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
from itest.excuteHandle.taskScheduler.jobThread import JobThread
from itest.models.taskHistory import TaskHistoryModel
import datetime
from django.core.mail import send_mail
from django.conf import settings

class JobModel:
    
    def __init__(self):
        self.taskId = None
        self.startDateTime = None
        self.repeatType = None
        self.taskType = None
        self.name = None
    
    def __isTimeRight(self):

        now = datetime.datetime.utcnow()
        delta = datetime.timedelta(hours=8) #使用东八区的时间
        now = now + delta
#         globalVars.getLogger().info("当前时间:" + str(now))
        if 0==self.taskType:
            return False
        if self.startDateTime > now:
            return False
        else:
            span = (now - self.startDateTime).days
            isToday = span
            if(self.repeatType > 0):
                isToday = span % self.repeatType 

            if(0==isToday):
                sec = (now - self.startDateTime).seconds #日期相运算不会影响秒级别
                if sec < globalVars.Interval * 60: #判断是否在五分钟内        
                    return True
                else:
                    return False
            else:
                return False
                
#         if 0==self.taskType:#非定时任务
#             if self.startDateTime > now: #如果开始时间大于现在，则不做
#                 return False
#             else:
#                 span = (now - self.startDateTime).days     #判断是否在当天
#                 if(0==span):
#                     sec = (now - self.startDateTime).seconds
#                     if sec < globalVars.Interval * 60: #判断是否在五分钟内        
#                         return True
#                     else:
#                         return False
#                 else:
#                     return False
#                     
#         else:
#             if self.startDateTime > now:
#                 return False
#             else:
#                 if(-1 == self.repeatType or 0 == self.repeatType):
#                     return False
#                 span = (now - self.startDateTime).days
#                 isToday = span % self.repeatType
#                 
#                 if(0==isToday):
#                     sec = (now - self.startDateTime).seconds #日期相运算不会影响秒级别
#                     if sec < globalVars.Interval * 60: #判断是否在五分钟内        
#                         return True
#                     else:
#                         return False
#                 else:
#                     return False
    
    def runJob(self):
        if self.__isTimeRight():  
            globalVars.getLogger().info("开始执行定时任务：")
            globalVars.getLogger().info(self.name)
            excute = TestTaskExcute(self.taskId,-1)
            excute.excute()
            globalVars.getLogger().info("定时任务执行成功")
        else:
            return ""
        
#     def runJobByThread(self):
#         if self.__isTimeRight():  
#             def run(job):
#                 globalVars.getLogger().info("开始执行定时任务：")
#                 globalVars.getLogger().info(job.name)
#                 try:
#                     excute = TestTaskExcute(job.taskId,-1)
#                     ret = excute.excute()
#                     if True!=ret:
#                         globalVars.getLogger().error("执行任务失败:"+ret)
#                 except Exception, e:
#                     globalVars.getLogger().error("定时任务执行失败："+CommonValueHandle.text2str(e.message))
#                 else:
#                     globalVars.getLogger().info("定时任务执行成功")
#             try:
#                 thread.start_new_thread(run, (self))
#             except Exception, e:
#                 globalVars.getLogger().error("创建线程失败："+CommonValueHandle.text2str(e.message))
#         else:
#             return ""
    def runJobByThread(self,index):
        if self.__isTimeRight():  
            # 创建新线程
            thread1 = JobThread(self,index,self.name)
             
            # 开启新线程
            thread1.start()
             
#             # 添加线程到线程列表
#             threads.append(thread1)
#             threads.append(thread2)
#              
            # 等待所有线程完成
#             for t in threads:
#                 t.join()
#             print "Exiting Main Thread"
        else:
            return ""
        
    def runJobByloop(self):
        if self.__isTimeRight():  
            globalVars.getLogger().info("开始执行定时任务：")
            globalVars.getLogger().info(self.name)
            try:
                excute = TestTaskExcute(self.taskId,-1)
                ret = excute.excute()
                if True!=ret:
                    globalVars.getLogger().error("执行任务失败:"+ret)
            except Exception as e:
                globalVars.getLogger().error("定时任务执行失败："+CommonValueHandle.text2str(e.message))
            else:
                historys = TaskHistoryModel.objects.filter(taskId=int(self.taskId)).order_by("-lastResultVersion")
                if len(historys) > 0:
                    current = historys[0]
                    name = current.taskName
                    successRate = current.successRate
                    lastRunningSuccessCount = current.lastRunningSuccessCount
                    lastRunningfailedCount = current.lastRunningfailedCount
                    lastRunningTime = current.lastRunningTime
                    message = u"任务 " + name + u" 的执行结果：\n" + u"执行时间: " + str(lastRunningTime) + u", 成功率:" + str(
                                successRate) + u", 成功:" + str(lastRunningSuccessCount) + u", 失败:" + str(lastRunningfailedCount) + \
                                u"\n 详细报告地址：http://t27.klook.io/history/" + str(current.id)
                    send_mail(u'接口自动化测试报告', message, settings.EMAIL_HOST_USER,settings.EMAIL_RECEIVERS)
                globalVars.getLogger().info("定时任务执行成功")
        else:
            return ""
