#coding=utf-8
'''
Created on 2017年12月7日

@author: anonymous
'''

from __future__ import absolute_import

from celery import task
from celery.utils.log import get_task_logger
from itest.util import globalVars
from itest.excuteHandle.taskScheduler.jobManager import JobManager

@task
def test_celery(x, y):
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    logger.info('func end -------------------->')
    print(x + y)
    return x + y


@task
def test_multiply(x, y):
    logger = get_task_logger(__name__)
    logger.info('func start  ----------------->')
    logger.info('application:%s', "TEST_APP")
    logger.info('func end -------------------->')
    print(x * y)
    return x * y

@task
def run_job():
    globalVars.getLogger().info('crontab轮训')
    globalVars.getLogger().info('开始轮训定时任务')
    jb = JobManager()
    jb.runJobsByNormalLoop()
    globalVars.getLogger().info('轮训结束')
    print("stop job")