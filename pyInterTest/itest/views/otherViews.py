# -*- coding: utf-8 -*-
'''
Created on 2017年8月1日

@author: anonymous
'''

from __future__ import unicode_literals
# from django.http import HttpResponse
from django.shortcuts import render
# from django.template import Context, loader
# from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def handler404(request):
    return render(request,'404.html')
@csrf_exempt
def handler500(request):
    return render(request,'500.html')