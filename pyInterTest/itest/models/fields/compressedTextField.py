#coding=utf-8
'''
Created on 2017年11月6日

@author: anonymous
'''

from django.db import models
 
class CompressedTextField(models.TextField):
    
    """
    model Fields for storing text in a compressed format (bz2 by default)
    读取数据库的时候调用这个方法
    """
    def from_db_value(self, value, expression, connection, context):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value
    """
    读取数据库完成后，把数据转换为python对象的执行。实际上跟from_db_value大同小异，就是需要多一个判断，判断是不是自己需要的格式：正确的对象，字符串和None
    """
    def to_python(self, value):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value
 
    def get_prep_value(self, value):
        if not value:
            return value
        try:
            value.decode('base64')
            return value
        except Exception:
            try:
                return value.encode('utf-8').encode('bz2').encode('base64')
            except Exception:
                return value