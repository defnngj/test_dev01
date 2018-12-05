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

import MySQLdb,traceback
import re,os
from multiprocessing import Process, Queue

class MysqlHandleNew:
    
    def __init__(self):
        self.conn = None
        self.server = None
        self.cursor = None
    
    def __del__(self):
        self.closeConn()
    
    def closeConn(self):
        pass
        # try:
        #     self.cursor.close()
        #     self.cursor = None
        # except:
        #     self.cursor = None
        #
        # try:
        #     self.conn.close()
        #     self.conn = None
        # except:
        #     self.conn = None
        #
        # try:
        #     self.server.close()
        #     self.server = None
        # except:
        #     self.server = None



    """
    测试是否连接mysql成功
    """
    def testConnectMysql(self, host, user, psw, port, db):
        self.conn = self.getMysqlConnectBase(host, user, psw, port, db)
        if not self.conn:
            return False
        else:
            self.closeConn()
            return True
    """
    以基础的方式进行mysql连接，并且返回conn
    """
    def getMysqlConnectBase(self, host, user, psw, port, db):
        if not host or not user or not psw or not port or not db:
            return None
        try:
            self.conn = MySQLdb.connect(host=host, user=user, passwd=psw, db=db, port=port)
        except Exception as e:
            globalVars.getLogger().error("连接数据库失败：" + CommonValueHandle.text2str(e.message))
            return None
        else:
            return self.conn


    """
    测试是否连接成功
    """
    def testConnectMysqlSSH(self, db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey):
        ret = self.getMysqlConnectSSH(db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey)
        if not ret:
            return False
        else:
            # self.closeConn()
            return True
    """
    使用ssh方式进行连接
    返回conn
    """
    def getMysqlConnectSSH(self, db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey):

        def run1(q,db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey):
            if not db_host or not db_user or not db_psw or not db_port or not db or not sshHost or not sshPort or not sshUser:
                globalVars.getLogger().error("参数错误")
                q.put(0)
                return
            if (not sshPsw and not sshKey):
                globalVars.getLogger().error("参数错误")
                q.put(0)
                return
            try:
                if not sshPsw:
                    accessory_dir = os.path.join(settings.STATIC_ROOT, "sshKeys")
                    keyUrl = "%s/%s" % (accessory_dir, sshKey)
                    if not os.path.exists(keyUrl):
                        globalVars.getLogger().error(keyUrl+"路径不存在")
                        q.put(0)
                        return

                    with SSHTunnelForwarder(
                            (sshHost, sshPort),
                            ssh_pkey=keyUrl,
                            ssh_username=sshUser,
                            remote_bind_address=(db_host, db_port)
                    ) as server:
                        # print server
                        conn = MySQLdb.connect(
                            host='127.0.0.1',
                            port=server.local_bind_port,
                            user=db_user,
                            passwd=db_psw,
                            db=db,
                            charset="utf8",
                            cursorclass=MySQLdb.cursors.DictCursor)
                else:
                    with SSHTunnelForwarder(
                            (sshHost, sshPort),
                            ssh_password=sshPsw,
                            ssh_username=sshUser,
                            remote_bind_address=(db_host, db_port)
                    ) as server:
                        conn = MySQLdb.connect(
                            host='127.0.0.1',
                            port=server.local_bind_port,
                            user=db_user,
                            passwd=db_psw,
                            db=db,
                            charset="utf8",
                            cursorclass=MySQLdb.cursors.DictCursor)

            except Exception as e:
                globalVars.getLogger().error("连接数据库失败：" + CommonValueHandle.text2str(e.message))
                traceback()
                q.put(0)
                return
            else:
                globalVars.getLogger().error("连接数据库失败：")
                q.put(1)
                return

        q = Queue(1)
        p1 = Process(target=run1, args=(q,db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey))
        p1.start()
        p1.join()
        ret = q.get()
        return ret

    """
    执行mysql语句
    """
    def excuteSql(self,env,sql):
        if not sql:
            return True
        sql = sql.strip()
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

        ret = True
        if not SSHHost:  # 基础连接方式
            globalVars.getLogger().info("使用基础连接方式")
            ret = self.__baseExcuteSql(host,user,psw,port,database,sql,"None")
        else:   #ssh连接方式
            globalVars.getLogger().info("使用ssh连接方式")
            ret = self.__sshExcuteSql(host, user, psw, port, database, SSHHost, SSHPort, SSHUser, SSHPsw, SSHKey,sql,"None")
        self.closeConn()
        return ret

    """
    执行mysql的断言语句
    """
    def excuteSqlAssert(self,env,sql,sqlAssert):
        sql = sql.strip()
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

        ret = True
        if not SSHHost:  # 基础连接方式
            globalVars.getLogger().info("使用基础连接方式")
            ret = self.__baseExcuteSql(host,user,psw,port,database,sql,sqlAssert)
        else:   #ssh连接方式
            globalVars.getLogger().info("使用ssh连接方式")
            ret = self.__sshExcuteSql(host, user, psw, port, database, SSHHost, SSHPort, SSHUser, SSHPsw, SSHKey,sql,sqlAssert)
        self.closeConn()
        return ret

    def __runSql(self,conn,sql):
        if not sql:
            return True
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            data = cursor.fetchall()
            print(data)
        except Exception as e:
            conn.rollback()
            globalVars.getLogger().error("执行sql失败：" + CommonValueHandle.text2str(e.message))
            return False
        else:
            cursor.close()
            conn.close()
            return True

    def __runSqlAssert(self,conn,sql,sqlAssert):
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
        else:
            cursor.close()
            conn.close()
        return ret

    def __baseExcuteSql(self,host,user,psw,port,database,sql,sqlAssert):
        if not sql:
            return True

        if not host or not user or not psw or not port or not database:
            return False

        try:
            self.conn = MySQLdb.connect(host=host, user=user, passwd=psw, db=database, port=int(port))
            if "None" == sqlAssert:
                return self.__runSql(self.conn,sql)
            else:
                return self.__runSqlAssert(self.conn,sql,sqlAssert)

        except Exception as e:
            globalVars.getLogger().error("连接mysql失败，请检查设置:" + CommonValueHandle.text2str(e.message))
            return False


    def __sshExcuteSql(self, db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey,sql,sqlAssert):

        def run1(q,db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey,sql,sqlAssert):

            def runSql(conn, sql):
                if not sql:
                    return 1
                if not conn:
                    return 0
                try:
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    data = cursor.fetchall()
                    print(data)
                except Exception as e:
                    conn.rollback()
                    globalVars.getLogger().error("执行sql失败：" + CommonValueHandle.text2str(e.message))
                    return 0
                else:
                    cursor.close()
                    conn.close()
                    return 1

            def runSqlAssert(conn, sql, sqlAssert):
                if not sql or not sqlAssert or not conn:
                    return 1
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
                            ret = (ass == nums)
                        elif re.search(r'^!=\d+$', sqlAssert):
                            ass = int(sqlAssert[2:])
                            ret = (ass != nums)
                        elif re.search(r'^>=\d+$', sqlAssert):
                            ass = int(sqlAssert[2:])
                            ret = (ass >= nums)
                        elif re.search(r'^<=\d+$', sqlAssert):
                            ass = int(sqlAssert[2:])
                            ret = (ass <= nums)
                        elif re.search(r'^>\d+$', sqlAssert):
                            ass = int(sqlAssert[1:])
                            ret = (ass > nums)
                        elif re.search(r'^<\d+$', sqlAssert):
                            ass = int(sqlAssert[1:])
                            ret = (ass < nums)
                        else:
                            ret = False
                    except Exception as e:
                        globalVars.getLogger().error(e.message)
                        ret = False
                except Exception as e:
                    globalVars.getLogger().error("执行sql失败:" + CommonValueHandle.text2str(e.message))
                    ret = False
                else:
                    cursor.close()
                    conn.close()
                if ret:
                    return 1
                else:
                    return 0

            if not sql:
                q.put(1)
                return

            if not db_host or not db_user or not db_psw or not db_port or not db or not sshHost or not sshPort or not sshUser:
                q.put(0)
                return

            if (not sshPsw and not sshKey):
                q.put(0)
                return

            try:
                if not sshPsw:
                    accessory_dir = os.path.join(settings.STATIC_ROOT, "sshKeys")
                    keyUrl = "%s/%s" % (accessory_dir, sshKey)
                    if not os.path.exists(keyUrl):
                        q.put(0)
                        return

                    with SSHTunnelForwarder(
                            (sshHost, int(sshPort)),
                            ssh_pkey=keyUrl,
                            ssh_username=sshUser,
                            remote_bind_address=(db_host, int(db_port))
                    ) as server:
                        conn = MySQLdb.connect(
                            host='127.0.0.1',
                            port=server.local_bind_port,
                            user=db_user,
                            passwd=db_psw,
                            db=db,
                            charset="utf8",
                            cursorclass=MySQLdb.cursors.DictCursor)
                        if "None" == sqlAssert:
                            q.put(runSql(conn,sql))
                        else:
                            q.put(runSqlAssert(conn,sql,sqlAssert))
                        return
                else:
                    with SSHTunnelForwarder(
                            (sshHost, int(sshPort)),
                            ssh_password=sshPsw,
                            ssh_username=sshUser,
                            remote_bind_address=(db_host, int(db_port))
                    ) as server:
                        conn = MySQLdb.connect(
                            host='127.0.0.1',
                            port=server.local_bind_port,
                            user=db_user,
                            passwd=db_psw,
                            db=db,
                            charset="utf8",
                            cursorclass=MySQLdb.cursors.DictCursor)

                        if "None" == sqlAssert:
                            q.put(runSql(conn,sql))
                        else:
                            q.put(runSqlAssert(conn,sql,sqlAssert))
                        return
            except Exception as e:
                traceback()
                globalVars.getLogger().error("连接数据库失败：" + CommonValueHandle.text2str(e.message))
                q.put(0)
                return

        q = Queue(1)
        p1 = Process(target=run1,args=(q, db_host, db_user, db_psw, db_port, db, sshHost, sshPort, sshUser, sshPsw, sshKey,sql,sqlAssert))
        p1.start()
        p1.join()
        ret = q.get()
        if 0==ret:
            return False
        else:
            return True

    
