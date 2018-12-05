#coding=utf-8
'''
Created on 2017年11月1日

@author: anonymous
'''
from concurrent.futures import ThreadPoolExecutor
    
class PoolSingleton(object):

    # 定义静态变量实例
    __instance = None

    def __init__(self):
        self.Pool = ThreadPoolExecutor(max_workers=4)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(PoolSingleton, cls).__new__(cls, *args, **kwargs)
#             print cls
        return cls.__instance
    
    def submitThread(self,task,parmas):
        self.Pool.submit(task,parmas)