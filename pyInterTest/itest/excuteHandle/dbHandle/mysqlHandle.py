# -*- coding: utf-8 -*-
'''
Created on 2017年10月18日

@author: anonymous
'''
from itest.models.databaseSetting import DatabaseSettingModel
from itest.util import globalVars
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
from sshtunnel import SSHTunnelForwarder 
from django.conf import settings

import MySQLdb,paramiko
import re,os

class MysqlHandle:
    
    def __init__(self):
        self.conn = None
        self.server = None
    
    def __del__(self):
        self.closeConn()
    
    def closeConn(self):
        try:
            self.conn.close()
        except:
            self.conn = None
        
        try:
            self.server.close()
        except:
            self.server = None
            
    
    def getMysqlConnect(self,env):
        if not env:
            return "环境变量不能为空"
        settings = DatabaseSettingModel.objects.filter(env=env)
        if(len(settings)<1):
            return None
        setting = settings[0]
        
        host = setting.host
        user = setting.user
        psw = setting.psw
        database = setting.database
        port = setting.port
        
        SSHHost = setting.sshHost
        SSHUser = setting.sshUser
        SSHPort = setting.sshPort
        SSHKey = setting.sshKey
        SSHPsw = setting.sshPsw
        
        if not SSHHost:
            self.conn = self.getMysqlConnectBase(host, user, psw, int(port), database)
        else:
#             self.conn = self.getMysqlConnectSSH(host, user, psw, int(port), database, SSHHost, int(SSHPort), SSHUser, SSHPsw, SSHKey)
            self.conn = self.getMysqlConnectSSH(host,user,psw,int(port),database,SSHHost,int(SSHPort),SSHUser,SSHPsw,SSHKey)
        if not self.conn:
            return "连接数据库失败，请检查设置是否正确"
        else:
            return self.conn

    
    def excuteSql(self,conn,sql):
        if not sql:
            return True
        if not conn:
            return False
        re = True
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data)
        except Exception as e:
            re = False
#             print e
            globalVars.getLogger().error("执行sql失败："+CommonValueHandle.text2str(e.message))
        finally:
            cursor.close
        return re
    

    def excuteSqlAssert(self,conn,sql,sqlAssert):
        if not sql or not sqlAssert or not conn:
            return True
        # 使用cursor()方法获取操作游标 
        cursor = conn.cursor()
        ret = True
        try:
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            nums = len(results)
            try:
                if re.search(r'^=\d+$', sqlAssert):
                    ass = int(sqlAssert[1:])
                    ret =  (ass == nums)  
                elif re.search(r'^!=\d+$', sqlAssert):
                    ass = int(sqlAssert[2:])
                    ret =  (ass != nums)
                elif re.search(r'^>=\d+$', sqlAssert):
                    ass = int(sqlAssert[2:])
                    ret =  (ass >=nums)
                elif re.search(r'^<=\d+$', sqlAssert):
                    ass = int(sqlAssert[2:])
                    ret =  (ass <=nums)
                elif re.search(r'^>\d+$', sqlAssert):
                    ass = int(sqlAssert[1:])
                    ret =  (ass > nums)
                elif re.search(r'^<\d+$', sqlAssert):
                    ass = int(sqlAssert[1:])
                    ret =  (ass < nums)
                else:
                    ret =  False
            except Exception as e:
                globalVars.getLogger().error(e.message)
                ret =  False
        except Exception as e:
            globalVars.getLogger().error("执行sql失败:"+CommonValueHandle.text2str(e.message))
            ret = False
        finally:           
            cursor.close()
        return ret
    
    """
    测试是否连接mysql成功
    """
    def testConnectMysql(self,host,user,psw,port,db):
        self.conn = self.getMysqlConnectBase(host,user,psw,port,db)
        if not self.conn:
            return False
        else:
            self.closeConn()
            return True
    """
    以基础的方式进行mysql连接，并且返回conn
    """
    def getMysqlConnectBase(self,host,user,psw,port,db):
        if not host or not user or not psw or not port or not db:
            return None
        try:
            self.conn=MySQLdb.connect(host=host,user=user,passwd=psw,db=db,port=port)
        except Exception as e:
            globalVars.getLogger().error("连接数据库失败："+CommonValueHandle.text2str(e.message))
            return None
        else:
            return self.conn 
    
    """
    测试是否连接成功
    """
    def testConnectMysqlSSH(self,db_host,db_user,db_psw,db_port,db,sshHost,sshPort,sshUser,sshPsw,sshKey):
        self.conn = self.getMysqlConnectSSH(db_host,db_user,db_psw,db_port,db,sshHost,sshPort,sshUser,sshPsw,sshKey)
        if not self.conn:
            return False
        else:
            self.closeConn()
            return True
#     """
#     使用ssh方式进行连接
#     返回conn
#     """
#     def getMysqlConnectSSH(self,db_host,db_user,db_psw,db_port,db,sshHost,sshPort,sshUser,sshPsw,sshKey):
#         if not db_host or not db_user or not db_psw or not db_port or not db or not sshHost or not sshPort or not sshUser:
#             return None
#         if (not sshPsw and not sshKey):
#             return None
# 
#         try:
#             if not sshPsw:
#                 accessory_dir = os.path.join(settings.STATIC_ROOT, "sshKeys")
#                 keyUrl = "%s/%s" % (accessory_dir, sshKey)
#                 if not os.path.exists(keyUrl):
#                     return False
#                 self.server = SSHTunnelForwarder((sshHost, sshPort),ssh_pkey=keyUrl,ssh_username=sshUser,remote_bind_address=(db_host, db_port))
#                 self.server.start()
#             else:
#                 self.server = SSHTunnelForwarder((sshHost, sshPort),ssh_password=sshPsw,ssh_username=sshUser,remote_bind_address=(db_host, db_port))
#                 self.server.start()
#             self.conn = MySQLdb.connect(host='127.0.0.1',port=self.server.local_bind_port,user=db_user,passwd=db_psw,db=db,charset="utf8")   
#                
#         except Exception as e:
#             globalVars.getLogger().error("连接数据库失败："+CommonValueHandle.text2str(e.message))
#             globalVars.getLogger().error(e)
#             return None
#         else:
#             return self.conn
        
        """
    使用ssh方式进行连接
    返回conn
    """
    def getMysqlConnectSSH(self,db_host,db_user,db_psw,db_port,db,sshHost,sshPort,sshUser,sshPsw,sshKey):
        if not db_host or not db_user or not db_psw or not db_port or not db or not sshHost or not sshPort or not sshUser:
            return None
        if (not sshPsw and not sshKey):
            return None

        try:
            if not sshPsw:
                accessory_dir = os.path.join(settings.STATIC_ROOT, "sshKeys")
                keyUrl = "%s/%s" % (accessory_dir, sshKey)
                if not os.path.exists(keyUrl):
                    return False
                
                with SSHTunnelForwarder(
                        (sshHost, sshPort),
                        ssh_pkey=keyUrl,
                        ssh_username=sshUser,
                        remote_bind_address=(db_host, db_port)
                ) as server:
                    print server
                    self.server = server
                    self.conn = MySQLdb.connect(
                        host='127.0.0.1',
                        port=server.local_bind_port,
                        user=db_user,
                        passwd=db_psw,
                        db=db,
                        charset="utf8",
                        cursorclass=MySQLdb.cursors.DictCursor)

                    # print self.conn
                    # cursor = self.conn.cursor()
                    #
                    # try:
                    #     cursor.execute('select * from tag_tbl;')
                    #     data = cursor.fetchall()
                    #     print 123
                    #     print data
                    # except Exception as e:
                    #     print e
                    # self.conn.close()
                    # cursor.close()
            else:
                with SSHTunnelForwarder(
                        (sshHost, sshPort),
                        ssh_password=sshPsw,
                        ssh_username=sshUser,
                        remote_bind_address=(db_host, db_port)
                ) as server:
                    self.server = server
                    self.conn = MySQLdb.connect(
                        host='127.0.0.1',
                        port=server.local_bind_port,
                        user=db_user,
                        passwd=db_psw,
                        db=db,
                        charset="utf8",
                        cursorclass=MySQLdb.cursors.DictCursor)

        except Exception as e:
            globalVars.getLogger().error("连接数据库失败："+CommonValueHandle.text2str(e.message))
            globalVars.getLogger().error(e)
            return None
        else:
            return self.conn