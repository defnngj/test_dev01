#coding=utf-8
'''
Created on 2017年11月1日

@author: anonymous
'''
# from apscheduler.schedulers.background import BackgroundScheduler
from itest.util import globalVars
from itest.excuteHandle.taskScheduler.jobManager import JobManager

def startSchedule():
    pass
#     globalVars.getLogger().info('设置定时任务')
#     sched = BackgroundScheduler()
#     def my_job():
#         globalVars.getLogger().info('开始轮训定时任务')
#         jb = JobManager()
#         jb.runJobs()
#     sched.add_job(my_job, 'interval', seconds=globalVars.Interval*60)
#     sched.start()
    
    
def startRunJob():
    globalVars.getLogger().info('crontab轮训')
    globalVars.getLogger().info('开始轮训定时任务')
    jb = JobManager()
    jb.runJobsByNormalLoop()
#     jb.runJobs()
#     jb.runJobsByNormal()