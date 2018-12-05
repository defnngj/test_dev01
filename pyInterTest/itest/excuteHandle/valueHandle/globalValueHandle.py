# -*- coding: utf-8 -*-
'''
Created on 2017年10月18日

@author: anonymous
'''
from itest.models.globalValue import GlobalValuesModel
from itest.util import globalVars
from itest.excuteHandle.valueHandle.commonValueHandle import CommonValueHandle
from itest.excuteHandle.valueHandle.myFuncHandle import myFuncHandleClass


class GlobalValueHandle:
    
    def getGlobalValue(self,env):
        re = {}
        if not env:
            return "env环境变量不能为空"
        try:
            values = GlobalValuesModel.objects.filter(env=env)
        except Exception as e:
            globalVars.getLogger().error("提取全局变量失败:"+CommonValueHandle.text2str(e.message))
            return "提取全局变量失败:"+CommonValueHandle.text2str(e.message)
        else:
            myfunc = myFuncHandleClass()
            for i in values:
                name = i.name
                if not name:
                    continue

                value = myfunc.functionReplace(i.value)#覆盖函数

                value = self.__getValue(value, i.type)
                re[name] = value
            return re
    
    def __getValue(self,data,dataType):
        re = None
        if not data or not dataType:
            return re
        else:
            if "int"==dataType:
                try:
                    re = int(data)
                except Exception:
                    re = 0
            elif "string" == dataType:
                re = CommonValueHandle.text2str(data)
            elif "float" == dataType:
                try:
                    re = float(data)
                except Exception:
                    re = 0
            elif "boolean" == dataType:
                re = (CommonValueHandle.text2str(data) == str(True))
            elif "bool" == dataType:
                re = (CommonValueHandle.text2str(data) == str(True))
            else:
                pass
            return re