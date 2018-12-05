# -*- coding: utf-8 -*-
'''
Created on 2017年9月15日

@author: anonymous
'''

# from __future__ import unicode_literals

import simplejson,os

from itest.models.project import Project
from itest.models.databaseSetting import DatabaseSettingModel
from itest.models.globalValue import  GlobalValuesModel
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle

from itest.models.env import EnvModel
from django.http import HttpResponse
from itest.util import globalVars
from itest.models.publicAssert import PublicAssertModel
from itest.excuteHandle.dbHandle.mysqlHandleNew import MysqlHandleNew
from django.conf import settings

def addEnv(request):  
    req = simplejson.loads(request.body)
    pId = None
    name = None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("pId"):
        pId=req["pId"]
    
    if not name or not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        pro = Project.objects.get(pk=int(pId))
    except Project.DoesNotExist:
        globalVars.getLogger().error("pId不存在")
        return HttpResponse(globalVars.responseJson("false", "项目不存在"), content_type="application/json")   
    else:    
        try:
            env = EnvModel.objects.create(name=name,project=pro)
        except Exception as e:
            globalVars.getLogger().error("新建执行环境失败："+CommonValueHandle.text2str(e.message))
            return HttpResponse(globalVars.responseJson("false", "新建执行环境失败"), content_type="application/json")
        else:
            return HttpResponse(globalVars.responseJson("true","",env.getDict()), content_type="application/json")

def getEnvList(request):  
    req = simplejson.loads(request.body)
    pId = None
    if req.has_key("pId"):
        pId=req["pId"]
    
    if not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        envlist = EnvModel.objects.filter(project_id=int(pId))
    except Project.DoesNotExist:
        globalVars.getLogger().error("pId不存在")
        return HttpResponse(globalVars.responseJson("false", "项目不存在"), content_type="application/json")   
    else:    
        re = []
        for i in envlist:
            re.append(i.getDict())
        return HttpResponse(globalVars.responseJson("true","",re), content_type="application/json")
    
def deleteEnv(request):  
    req = simplejson.loads(request.body)
    eId = None
    if req.has_key("eId"):
        eId=req["eId"]
    
    if not eId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        env = EnvModel.objects.get(pk=int(eId))
        env.delete()
    except Exception as e:
        globalVars.getLogger().error("删除执行环境失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除执行环境失败"), content_type="application/json")   
    else:    
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def updateEnv(request):  
    req = simplejson.loads(request.body)
    eId = None
    name = None
    if req.has_key("eId"):
        eId=req["eId"]
    if req.has_key("name"):
        name=req["name"]
    
    if not eId or not name:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        env = EnvModel.objects.get(pk=int(eId))
        env.name = name
        env.save()
    except Exception as e:
        globalVars.getLogger().error("修改执行环境失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "修改执行环境失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true","",env.getDict()), content_type="application/json")      

def addSystemAssert(request):
    req = simplejson.loads(request.body)
    name = None
    key = None
    value = ""
    atype = 0
    pId = None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("key"):
        key=req["key"]
    if req.has_key("value"):
        value=req["value"]
    if req.has_key("type"):
        atype=req["type"]
    if req.has_key("pId"):
        pId=req["pId"]
    
    if not name or not key or not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        publicAssert = PublicAssertModel.objects.create(name=name,key=key,value=value,type=atype,project_id=int(pId))
    except Exception as e:
        globalVars.getLogger().error("添加全局断言失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "添加全局断言失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true","",publicAssert.getDict()), content_type="application/json")
    
def deleteSystemAssert(request):
    req = simplejson.loads(request.body)
    sId = None
    if req.has_key("sId"):
        sId=req["sId"]
    
    if not sId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        publicAssert = PublicAssertModel.objects.get(pk=int(sId))
        publicAssert.delete();
    except Exception as e:
        globalVars.getLogger().error("删除全局断言失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除全局断言失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
    
def getSystemAssertList(request):
    req = simplejson.loads(request.body)
    pId = None
    if req.has_key("pId"):
        pId=req["pId"]
    if not pId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        publicAssertList = PublicAssertModel.objects.filter(project_id=int(pId))
    except Exception as e:
        globalVars.getLogger().error("删除全局断言失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除全局断言失败"), content_type="application/json")   
    else:
        re = []
        for i in publicAssertList:
            re.append(i.getDict())
        return HttpResponse(globalVars.responseJson("true","",re), content_type="application/json")
    
def addGlobalValues(request):
    req = simplejson.loads(request.body)
    name = None
    value = ""
    atype = None
    pId = None
    eId = None
    if req.has_key("name"):
        name=req["name"]
    if req.has_key("value"):
        value=req["value"]
    if req.has_key("type"):
        atype=req["type"]
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("eId"):
        eId=req["eId"]
    if not name or not value or not pId or not atype:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        values = GlobalValuesModel.objects.create(name=name,value=value,type=atype,project_id=int(pId),env_id=int(eId))
    except Exception as e:
        globalVars.getLogger().error("添加全局断言失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "添加全局断言失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true","",values.getDict()), content_type="application/json")
#     
def deleteGlobalValues(request):
    req = simplejson.loads(request.body)
    gId = None
    if req.has_key("gId"):
        gId=req["gId"]
     
    if not gId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        value = GlobalValuesModel.objects.get(pk=int(gId))
        value.delete();
    except Exception as e:
        globalVars.getLogger().error("删除全局变量失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除全局变量失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")
#     
def getGlobalValuesList(request):
    req = simplejson.loads(request.body)
    eId = None
    if req.has_key("eId"):
        eId=req["eId"]
    if not eId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        valueList = GlobalValuesModel.objects.filter(env_id=int(eId))
    except Exception as e:
        globalVars.getLogger().error("删除全局断言失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "删除全局断言失败"), content_type="application/json")   
    else:
        re = []
        for i in valueList:
            re.append(i.getDict())
        return HttpResponse(globalVars.responseJson("true","",re), content_type="application/json")

def getSqlSetting(request):
    req = simplejson.loads(request.body)
    eId = None

    if req.has_key("eId"):
        eId=req["eId"]

    if not eId:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    try:
        sql = DatabaseSettingModel.objects.filter(env_id=int(eId))
        currentSql = None
        
    except Exception as e:
        globalVars.getLogger().error("保存sql设置失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "保存sql设置失败"), content_type="application/json")   
    else:
        if 0<len(sql):
            currentSql=sql[0]
            return HttpResponse(globalVars.responseJson("true","",currentSql.getDict()), content_type="application/json")
        else:
            return HttpResponse(globalVars.responseJson("true",""), content_type="application/json")

def saveSqlSetting(request):
    req = simplejson.loads(request.body)
    eId = None
    pId = None
    sType="mysql"
    host=None
    user=None
    psw=None
    port=None
    database=None
    SSHHost = ""
    SSHPort = 22
    SSHUser = ""
    SSHPsw = ""
    SSHKey = ""
    if req.has_key("eId"):
        eId=req["eId"]
    if req.has_key("pId"):
        pId=req["pId"]
    if req.has_key("type"):
        sType=req["type"]
    if req.has_key("host"):
        host=req["host"]
    if req.has_key("user"):
        user=req["user"]
    if req.has_key("psw"):
        psw=req["psw"]
    if req.has_key("port"):
        port=req["port"]
    if req.has_key("database"):
        database=req["database"]
    if req.has_key("SSHHost"):
        SSHHost=req["SSHHost"]
    if req.has_key("SSHPort"):
        SSHPort=req["SSHPort"]
    if req.has_key("SSHUser"):
        SSHUser=req["SSHUser"]
    if req.has_key("SSHPsw"):
        SSHPsw=req["SSHPsw"]
    if req.has_key("SSHKey"):
        SSHKey=req["SSHKey"]
    if not eId or not pId or not host or not user or not psw or not port or not database:
        globalVars.getLogger().error("参数不正确，请检查请求参数")
        return HttpResponse(globalVars.responseJson("false", "参数不正确，请检查请求参数"), content_type="application/json")
    
    sqlHandle = MysqlHandleNew()
    connect = None
    if not SSHHost:
        connect = sqlHandle.testConnectMysql(host, user, psw, int(port), database)
    else:
        connect = sqlHandle.testConnectMysqlSSH(host, user, psw, int(port), database,SSHHost,int(SSHPort),SSHUser,SSHPsw,SSHKey)
    if not connect:
        sqlHandle.closeConn()
        return HttpResponse(globalVars.responseJson("false", "连接数据库失败，请重新设置"), content_type="application/json")
    sqlHandle.closeConn()
    globalVars.getLogger().info("连接数据库成功")
    sql = DatabaseSettingModel.objects.filter(env_id=int(eId))
    currentSql = None
    if 0==len(sql):
#             currentSql=DatabaseSettingModel.objects.create(project_id=pId,env_id=eId,type=sType,host=host,user=user,psw=psw,port=port,database=database)
        currentSql=DatabaseSettingModel()
    else:
        currentSql=sql[0]
    
    try:
        currentSql.type=sType
        currentSql.host=host
        currentSql.user=user
        currentSql.psw=psw
        currentSql.port=port
        currentSql.database=database
        
        currentSql.sshHost=SSHHost
        currentSql.sshUser=SSHUser
        currentSql.sshPort=SSHPort
        currentSql.sshKey=SSHKey
        currentSql.sshPsw=SSHPsw
        
        currentSql.project_id = pId
        currentSql.env_id = eId
        currentSql.save()
    except Exception as e:
        globalVars.getLogger().error("保存sql设置失败:"+CommonValueHandle.text2str(e.message))
        return HttpResponse(globalVars.responseJson("false", "保存sql设置失败"), content_type="application/json")   
    else:
        return HttpResponse(globalVars.responseJson("true","",currentSql.getDict()), content_type="application/json")
    
def uploadSSHKey(request):
    file_obj = request.FILES.get('file')
    recv_size = file_obj._size
    
    if recv_size > 1024000:
        return HttpResponse(globalVars.responseJson("false", "上传失败，文件不能大于1M"), content_type="application/json")
    else:
        if file_obj:   # 处理附件上传到方法
            accessory_dir = os.path.join(settings.STATIC_ROOT, "sshKeys")
            if not os.path.isdir(accessory_dir):
                os.mkdir(accessory_dir)
#             timestr = time.strftime("%Y%m%d%H%M%S",time.localtime())
#             upload_file = "%s/%s_%s" % (accessory_dir, file_obj.name,timestr)
            upload_file = "%s/%s" % (accessory_dir, file_obj.name)
            with open(upload_file, 'wb') as new_file:
                for chunk in file_obj.chunks():
                    new_file.write(chunk)
    #         order_id = time.strftime("%Y%m%d%H%M%S",time.localtime())
    #         cache.set(order_id,upload_file)
            return HttpResponse(globalVars.responseJson("true","",{"fileName":file_obj.name}), content_type="application/json")
#         return HttpResponse(order_id)