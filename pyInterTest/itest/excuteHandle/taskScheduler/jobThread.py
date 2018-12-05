#coding=utf-8
'''
Created on 2017年11月28日

@author: anonymous
'''
from itest.util import globalVars
from itest.excuteHandle.taskHandle.testTaskExcute import TestTaskExcute
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
import threading

class JobThread(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self, job, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.job = job
        
    def run(self): 
        globalVars.getLogger().info("开始执行定时任务：")
        globalVars.getLogger().info("线程名称:"+self.name)
        globalVars.getLogger().info("线程Id:"+self.threadID)
        try:
            excute = TestTaskExcute(self.job.taskId,-1)
            ret = excute.excute()
            if True!=ret:
                globalVars.getLogger().error("执行任务失败:"+ret)
        except Exception as e:
            globalVars.getLogger().error("定时任务执行失败："+CommonValueHandle.text2str(e.message))
        else:
            globalVars.getLogger().info("定时任务执行成功")
        globalVars.getLogger().info("线程名称:"+self.name+"--执行完毕")