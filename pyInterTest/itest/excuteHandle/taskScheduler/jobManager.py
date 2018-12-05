#coding=utf-8
'''
Created on 2017年11月1日

@author: anonymous
'''

from itest.excuteHandle.taskScheduler.jobModel import JobModel
from itest.models.task import TaskModel
from itest.util.Pool import PoolSingleton
from itest.util import globalVars

class JobManager:
    
    def __init__(self):
        self.jobList = []
        self.pool = PoolSingleton()
    
    def __getJobs(self):
        try:
            tasks = TaskModel.objects.all()
        except Exception as e:
            globalVars.getLogger().error(e)
            self.jobList = []
        else:
            for t in tasks:
                if 0==t.taskType:
                    continue
                else:
                    tmpJob = JobModel()
                    tmpJob.taskType = t.taskType
                    tmpJob.repeatType = t.repeatType
                    tmpJob.startDateTime = t.repeatDateTime
                    tmpJob.taskId = t.id
                    tmpJob.name = t.name
                    self.jobList.append(tmpJob)
    #使用线程池执行
    def runJobs(self):
        self.__getJobs()
        def task(t):
            t.runJob()
        for t in self.jobList:
            self.pool.submitThread(task,t)  # 往线程池里面加入一个task
            
    #使用普通循环执行
    def runJobsByNormal(self):
        self.__getJobs()
        for t in self.jobList:
            t.runJobByThread()
            
    #使用普通循环执行
    def runJobsByNormalLoop(self):
        self.__getJobs()
        for t in self.jobList:
            t.runJobByloop()