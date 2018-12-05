# coding=utf-8
"""
Created on 2017年7月31日

@author: anonymous
"""
import datetime
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from itest.models.token import Token
from itest.util import globalVars
from django.http import HttpResponseRedirect
from django.core.cache import cache
from itest.util.globalVars import logger


class CommonMiddleware(MiddlewareMixin):
    '''
    classdocs
    中间件，用来打印所有的请求以及响应，判断token是否符合要求
    '''
    @staticmethod
    def is_token_valid(token):
        value = cache.get(token)      
        if value is None:
            token_obj = Token.objects.filter(Token=token)
            if token_obj.count() >0:
                token_obj = Token.objects.get(Token=token)
                  
                if token_obj.expireDate > datetime.datetime.now():
                    cache.set(token, token_obj.expireDate, settings.REDIS_TIMEOUT)
                    return True
                else:
                    return False
            else:
                return False
        else:
            if value > datetime.datetime.now():
                return True
            else:
                return False

    def process_request(self, request):
        # 如果不存在token或者token不存在，则重定向到login页面
        path = request.path
        if path == "/login" or path == "/register":
            return None
        else:
            print(globalVars.IToken)
            # 不存在token
            if not request.COOKIES.get(globalVars.IToken, ''):
                return HttpResponseRedirect(reverse('login'))
#            存在token
            token = request.COOKIES[globalVars.IToken] 
            if self.is_token_valid(token):
                return None
            else:
                return HttpResponseRedirect(reverse('login'))

    # def process_response(self, request, response):
    #     logger.info("中间件执行完成")
    #     return response
