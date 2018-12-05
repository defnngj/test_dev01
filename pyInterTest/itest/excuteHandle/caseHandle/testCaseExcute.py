# -*- coding: utf-8 -*- 
'''
Created on 2017年8月11日

@author: anonymous
'''
from itest.models.testCase import TestCaseModel
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
from itest.models.testCaseResult import TestCaseResultModel
from itest.excuteHandle.dbHandle.mysqlHandleNew import MysqlHandleNew
from itest.excuteHandle.valueHandle.myFuncHandle import myFuncHandleClass
from itest.util import globalVars
import json
import re
import requests
import traceback
import jmespath

# from itest.models.apiDefine import ApiDefine

class TestCaseExcute:
    
    def __init__(self,cId,globalVars,runningVars,extraPickerValue,env,ExcuteType,version):
        self.cId = cId
        self.globalVars = globalVars
        self.runningVars = runningVars
        self.mysqlHandle = MysqlHandleNew()
        self.env = env
        self.extraPickerValue = extraPickerValue
        self.ExcuteType = ExcuteType #如果-1代表是前置案例，不保存结果
        self.version = version
        
        self.testCase = {}
        self.api = {}
        self.requestHead = {}
        self.requestBody = {}
        self.systemAssertResult = []
        self.defineAssertResult = []
        self.sqlAssertResult = []
        self.excuteVars = {}
        self.result = 0
        
        self.response = ""
        self.responseBody = ""
        self.responseHead = ""
        self.responseCookie = ""
        self.responseStatusCode = ""
        self.error = False
        
        self.url = ""
    
    """
    公共断言逻辑
    """
    def __dealAssertTeal(self,response,assertList):
        ret = []
        for i in assertList:
            tmp = {}
            key = i["key"]
#             print tmp
            key = self.__dealValueSetting(key)
            tmp["key"] = key
            
            value = i["value"]
            value = self.__dealValueSetting(value)
            tmp["value"] = value
            
            if 0==i["type"]:
                tmp["type"] = "include"
            else:
                tmp["type"] = "exclude"
            tmp["result"] = self.__isResponseIncludeValue(response,key,value,i["type"])
            tmp["assertType"] = "sys"
            ret.append(tmp)
#         print ret
        return ret
    
    """
    递归断言判断
    """
    def __isResponseIncludeValue(self,response,key,value,atype):
#         print response,key,value,atype
        class ViewDict:
            def __init__(self):
                self.result = False
                pass
            def tell(self,obj,key,value):
                # print key
                # print value
                if self.result:
                    return
                if not (isinstance(obj, dict) or isinstance(obj, list)):
                    return

                if obj.has_key(key):
                    v = obj[key]
                    # print v
                    # print key
                    if isinstance(v, bool):
                        if False==v and (False==value or "false"==value or "False"==value):
                            self.result = True
                        elif True==v and (True==value or "true"==value or "True"==value):
                            self.result = True
                        else:
                            self.result = False
                    else:
                        self.result = CommonValueHandle.textCompare(value, v)

                    if not self.result:
                        for i in obj:
                            if isinstance(obj[i], list):
                                for j in obj[i]:
                                    self.tell(j, key, value)
                            else:
                                self.tell(obj[i], key, value)
                else:
                    for i in obj:
                        if self.result:
                            return
                        if isinstance(obj[i],list):
                            for j in obj[i]:
                                self.tell(j,key,value)
                        else:
                            self.tell(obj[i],key,value)

        key = CommonValueHandle.text2str(key)
        value = CommonValueHandle.text2str(value)
        response = CommonValueHandle.text2str(response)

        if not key or not response:
            return False
        
        if not value or '""' == value or ""==value:
            re = response.find(key)
            if 0==atype:
                return (re > -1)
            else:
                return (re < 0)
        else:
            # print key
            # print value
            re = response.find(key)
            if ((0==atype) and (re < 0)) or ((1==atype) and (re > -1)):
                return False
            # print key
            # print value
            re = response.find(value)
            if ((0==atype) and (re < 0)) or ((1==atype) and (re > -1)):
                return False

            print(key)
            print(value)
            obj = {}
            try:
                obj = json.loads(response)
            except Exception:
                return False
            else:
                v = ViewDict()
                v.tell(obj, key, value)
                r = v.result
                if 0==atype:
                    return (True == r)
                else:
                    return (False == r)
    
    """
    格式有=0，>=0,<=0,>0,<0,!=0
    """
    def __dealSqlAssert(self,sql,sqlAssert):
        return self.mysqlHandle.excuteSqlAssert(self.env, sql, sqlAssert)
    
    """
    变量覆盖
    """
    def __dealValueSetting(self,value):
#         print "变量覆盖"
        if not value:
            return ""
#         print self.globalVars
        newv = CommonValueHandle.valueReplace(value,self.globalVars)
        newv = CommonValueHandle.valueReplace(newv,self.runningVars)
#         print "完成"
        return newv
    
    """
    执行sql
    """
    def __excuteSql(self,sql):
        sql = self.__dealValueSetting(sql)
        return self.mysqlHandle.excuteSql(self.env, sql)
    
    """
    案例执行函数
    """
    def excute(self):
        if not self.getTestCase() or not self.getApi():
            self.error = True
            globalVars.getLogger().error("案例获取失败,无法执行，请检查设置")
            return "案例获取失败,无法执行，请检查设置"

        if not self.dealPreSql():
            self.error = True
            globalVars.getLogger().error("案例前置条件中的sql语句执行错误，请检查设置.")
            return "案例前置条件中的sql语句执行错误，请检查设置."
        
        self.getHead()
        globalVars.getLogger().info("head：")
        globalVars.getLogger().info(self.requestHead)
        
        self.getParmas()
        globalVars.getLogger().info("body：")
        globalVars.getLogger().info(self.requestBody)

        re = self.sendReuest()
        if True != re:
            self.error = True
            globalVars.getLogger().error("案例执行错误:"+CommonValueHandle.text2str(re))
            return re
#         
        response = self.responseBody

        globalVars.getLogger().info("response:")
        globalVars.getLogger().info(response)
        
        self.getPicker(response)

        globalVars.getLogger().info("变量提取：")
        globalVars.getLogger().info(self.runningVars)

        self.dealSystemAssert(response)
        
        globalVars.getLogger().info("断言：")
        globalVars.getLogger().info(self.systemAssertResult)

        self.dealDefineAssert(response)
        globalVars.getLogger().info(self.defineAssertResult)

        self.dealSqlAssert()
        globalVars.getLogger().info(self.sqlAssertResult)
        
#         re = self.dealPostSql()
        if not self.dealPostSql():
            self.error = True
            globalVars.getLogger().error("案例后置条件中的sql语句执行错误，请检查设置.")
            return "案例后置条件中的sql语句执行错误，请检查设置."
        return True
    """
    获取测试案例
    """
    def getTestCase(self):
        try:
            self.testCase = TestCaseModel.objects.get(pk=int(self.cId))
        except Exception as e:
            globalVars.getLogger().error("获取案例失败:"+CommonValueHandle.text2str(e.message))
            return False
        else:
            return True
    """
    获取案例的api
    """
    def getApi(self):
        self.api = self.testCase.api
        return self.api
        
    """
    获取请求头部
    """
    def getHead(self):
        headDict = {}
        
        apiHead = self.api.getHeader()#api定义的数据
        tmp = self.testCase.headerData
        caseHead = {}
        try:
            caseHead = json.loads(tmp)#case设置的数据
        except Exception:
            caseHead = {}
#         print caseHead

        for h in apiHead:
            key = h["name"]
            old_value = h["value"]
            if caseHead.has_key(key):
                old_value = caseHead[key]
            if not old_value:
                headDict[key] = ""
            else:
                new_value = self.__dealValueSetting(old_value)
                headDict[key] = new_value
        if not headDict.has_key("Connection"):
            headDict["Connection"] = "close"
        self.requestHead = headDict
    """
    获取请求的参数
    """   
    def getParmas(self):
        parmasDict = {}
        
        apiParmas = self.api.getParmas()
        tmp = self.testCase.parmasData
        tmp = self.__dealValueSetting(tmp)
        if tmp:
            caseParmas = json.loads(tmp)
        else:
            caseParmas = {}
        
        parmasType = self.api.parmasType
        caseParmasType = self.testCase.dataType
        if("json"==parmasType):#json表单
            if(0==caseParmasType):#0代表是存储的数据是json
                parmasDict = caseParmas
            else:
                def recursionSetObje(obj,array,index):
                    if(index >= len(array)):
                        return
                    if(None == obj):
                        obj = {}
                    key = array[index]
                    if (index==(len(array) - 1)):
                        obj[array[index]] = ""
                    else:
                        l = re.search(r'.*\[\]$', key)
                        if(None==l):
                            if not obj.has_key(key):
                                obj[key] = {}
                            recursionSetObje(obj[key],array,index+1)
                        else:
                            nKey = key[0:(len(key)-2)]
                            if not obj.has_key(nKey):
                                obj[nKey] = []
                                obj[nKey][0] = {}
                            recursionSetObje(obj[nKey][0],array,index+1)  
                        
                for p in apiParmas:
                    name = p["name"]
                    l = str(name).split(".")
                    if(len(l)<2):
                        parmasDict[name] = ""
                    else:
                        recursionSetObje(parmasDict,l,0)
        else:#form表单
            if(0==caseParmasType):#0代表是存储的数据是json,所以数据丢弃掉，设置为空
                for p in apiParmas:
                    name = p["name"]
                    parmasDict[name] = ""
            else:
                for p in apiParmas:
                    name = p["name"]
                    ptype = p["type"]
                    value = ""
                    if(caseParmas.has_key(name)):
                        value = caseParmas[name]
                        value = self.__dealValueSetting(value)
                    if not value:
                        parmasDict[name] = ""
                    else:
                        re = value
                        try:
                            if "int"==ptype:
                                try:
                                    re = int(value)
                                except:
                                    re = 0
                            elif "string" == ptype:
                                re = CommonValueHandle.text2str(value)
                            elif "float" == ptype:
                                try:
                                    re = float(value)
                                except:
                                    re = 0
                            elif "boolean" == ptype:
                                re = ((CommonValueHandle.text2str(value) == str(True)) or (CommonValueHandle.text2str(value)=="true"))
                            elif "bool" == ptype:
                                re = ((CommonValueHandle.text2str(value) == str(True)) or (CommonValueHandle.text2str(value)=="true"))
                            else:
                                re = CommonValueHandle.text2str(value)
                        except:
                            re = CommonValueHandle.text2str(value)
                        parmasDict[name] = re
        self.requestBody = parmasDict
       
    def sendReuest(self):
#         globalVars.getLogger().info(self.api.url)
        url = self.__dealValueSetting(self.api.url)
        self.url = url
#         globalVars.getLogger().info(url)
#         client = requests.Session()
        client = requests.session()
        client.keep_alive = False
        try:
            if "json" == self.api.parmasType:
#                 globalVars.getLogger().info("参数是json")
#                 globalVars.getLogger().info(url)
#                 globalVars.getLogger().info(self.requestHead)
#                 globalVars.getLogger().info(self.requestBody)
                if "get"==self.api.method:
                    self.response = client.get(url,headers=self.requestHead,params=self.requestBody,timeout=20)
                elif "post"==self.api.method:
                    self.response = client.post(url,headers=self.requestHead,json=self.requestBody,timeout=20)
                elif "put"==self.api.method:
                    self.response = client.put(url,headers=self.requestHead,json=self.requestBody,timeout=20)
                elif "delete"==self.api.method:
                    self.response = client.delete(url,headers=self.requestHead,json=self.requestBody,timeout=20)
                else:
                    self.response = ""
                    raise Exception("请求方法不正确！")
            else:
#                 print "参数是form"
                globalVars.getLogger().info("参数是form")
#                 globalVars.getLogger().info(url)
#                 globalVars.getLogger().info(self.requestHead)
#                 globalVars.getLogger().info(self.requestBody)
                if "get"==self.api.method:
                    self.response = client.get(url,headers=self.requestHead,params=self.requestBody,timeout=20)
                elif "post"==self.api.method:
                    self.response = client.post(url,headers=self.requestHead,data=self.requestBody,timeout=20)
                elif "put"==self.api.method:
                    self.response = client.put(url,headers=self.requestHead,data=self.requestBody,timeout=20)
                elif "delete"==self.api.method:
                    self.response = client.delete(url,headers=self.requestHead,data=self.requestBody,timeout=20)
                else:
                    self.response = ""
                    raise Exception("请求方法不正确！")            
        except Exception as e:
            globalVars.getLogger().error("执行请求失败："+CommonValueHandle.text2str(e.message))
            return "执行请求失败："+CommonValueHandle.text2str(e.message)
        else:
            self.responseBody = self.response.text
            self.responseStatusCode = self.response.status_code
            self.responseHead = self.response.headers
            return True
    """
    变量提取，只支持json格式
    """
    def getPicker(self,response):
        def getNext(obj,array,index):
            if not obj or index>(len(array)-1):
                return ""
            key = array[index]
            if(index == len(array)-1):
                l = re.findall(r'\[[0-9]+\]$', key)
                if not l:
                    ret = ""
                    try:
                        ret = obj[key]
                    except Exception:
                        return ""
                    else:
                        return ret
                else: 
                    num = 0
                    numstr = l[0]
                    for i in l:
                        numstr = i
                        s = i[1:len(i)-1]
                        num = int(s)
                    ret = ""
                    tmp = key.split(numstr)
                    if len(tmp) < 1:
                        return ""
                    key = tmp[0]
                    try:
                        ret = obj[key][num]
                    except Exception:
                        return ""
                    else:
                        return ret
            else:
                l = re.findall(r'\[[0-9]+\]$', key)
                n = {}
                if not l:
                    try:
                        n = obj[key]
                    except Exception:
                        return ""
                else:
                    num = 0
                    numstr = l[0]
                    for i in l:
                        numstr = i
                        s = i[1:len(i)-1]
                        num = int(s)
                    tmp = key.split(numstr)
                    if len(tmp) < 1:
                        return ""
                    key = tmp[0]
                    n = {}
                    try:
                        n = obj[key][num]
                    except Exception:
                        return ""
                return getNext(n,array,index+1)
                
        pickers = self.testCase.getValuePicker() + self.extraPickerValue
        obj = {}
        try:
            obj = json.loads(response)
        except Exception:
            return

        myfunc = myFuncHandleClass()
        for p in pickers:
            key = p["value"]
            expression = p["expression"]
            # l = CommonValueHandle.text2str(expression).split(".")
            # value = getNext(obj,l,0)
            # value = myfunc.functionReplace(value)  # 覆盖函数
            # self.runningVars[key] = value
            # self.excuteVars[key] = value

            value = jmespath.search(expression, obj)
            if value != None:
                value = myfunc.functionReplace(value)
                self.runningVars[key] = value
                self.excuteVars[key] = value

    """
    前置sql执行
    """
    def dealPreSql(self):
        try:
            preSql = self.testCase.preSql
            globalVars.getLogger().info("执行前置sql:" + str(preSql))
            re = self.__excuteSql(preSql)
        except Exception as e:
            print(e)
            traceback.print_exc()
            globalVars.getLogger().info("执行前置sql失败：" + str(preSql) + CommonValueHandle.text2str(e.message))
            return False
        else:
            return re

    """
    后置sql执行
    """
    def dealPostSql(self):
        try:
            postSql = self.testCase.postSql
            globalVars.getLogger().info("执行后置sql:" + str(postSql))
            re = self.__excuteSql(postSql)
        except Exception as e:
            globalVars.getLogger().info("执行后置sql失败：" + str(postSql) + CommonValueHandle.text2str(e.message))
            return False
        else:
            return re
    
    """
    系统断言
    """
    def dealSystemAssert(self,response):
        mySysAssertIds = self.testCase.getPreAssert()
        sysAssert = self.testCase.getPublicAssert()
        mySysAssert =[]
        for i in sysAssert:
            if i["sId"] in mySysAssertIds:
                mySysAssert.append(i)
        ret = self.__dealAssertTeal(response, mySysAssert)
        self.systemAssertResult = ret
    """
    自定义断言
    """   
    def dealDefineAssert(self,response):
        definedAssert = self.testCase.getOtherAssert()
#         globalVars.getLogger().info(definedAssert)
        ret = self.__dealAssertTeal(response, definedAssert)
        self.defineAssertResult = ret
    """
    sql断言
    """
    def dealSqlAssert(self):
        sqlAssert = self.testCase.getSqlAssert()
        ret = []
        for i in sqlAssert:
            tmp = {}
            sql = i["sql"]
            sql = self.__dealValueSetting(sql)
            tmp["sql"] = sql
            
            ass = i["sqlAssert"]
            ass = self.__dealValueSetting(ass)
            tmp["sqlAssert"] = ass
            
            tmp["result"] = self.__dealSqlAssert(i["sql"], i["sqlAssert"])
            tmp["assertType"] = "sql"
            ret.append(tmp)
        self.sqlAssertResult = ret
    
    def saveResult(self,tId,message):
        try:
            pickerValue = json.dumps(self.excuteVars)
            assertsList = self.systemAssertResult + self.defineAssertResult +self.sqlAssertResult 
            asserts = json.dumps(assertsList)
            self.result = 0
            for i in assertsList:
                if False == i["result"]:
                    self.result = -1
                    break
            if self.error:
                self.result = -1
            
            result = TestCaseResultModel()
            result.project = self.api.project
            result.version = self.version
            
            if self.requestHead:
                result.requestHead = json.dumps(self.requestHead)
            else:
                result.requestHead = "{}"
            
            if self.requestBody:
                result.requestBody = json.dumps(self.requestBody)
            else:
                result.requestBody = "{}"
                
            result.requestCookie = "{}"
#             print type(self.responseHead)
            responseHead = {}
            for i in self.responseHead:
                responseHead[i]=self.responseHead[i]
            
            result.responseHead = json.dumps(responseHead)
            
            responseCooike = {}
            for i in self.responseCookie:
                responseCooike[i]=self.responseCookie[i]
            
            result.responseCookie = json.dumps(responseCooike)
            result.responseBody = self.responseBody
            result.pickerValues = pickerValue
            result.asserts = asserts
            result.success = self.result
            result.responseStatus = self.responseStatusCode
            
            result.preSql = self.testCase.preSql
            result.postSql = self.testCase.postSql
            
            result.taskId = tId
            result.caseId = self.cId
            
            result.url = self.url
            result.method = self.api.method
            
            result.parmasType = self.api.parmasType
            result.message = message
            
            result.save()
            return result.id
        except Exception as e:
            globalVars.getLogger().error("保存数据失败："+CommonValueHandle.text2str(e.message))
            return -1
    
#     """
#     前置条件
#     """
#     def dealPreRequire(self):
#         preRquire = self.testCase.getPreRequirement()
#         for i in preRquire:
#             cId = i["cId"]
#             pickerValue = i["pickerValue"]
#             try:
#                 tmpCase = TestCaseModel.objects.get(pk=int(cId))
#             except Exception as e:
#                 print "执行前置案例失败"
#                 return False
            
#     """
#     后置条件
#     """
#     def dealPostRequire(self):
#         postRequire = self.testCase.getPostRequirement()
#         for i in postRequire:
#             cId = i["cId"]
#             pickerValue = i["pickerValue"]
#             try:
#                 tmpCase = TestCaseModel.objects.get(pk=int(cId))
#             except Exception as e:
#                 print "执行后置案例失败"
#                 return False