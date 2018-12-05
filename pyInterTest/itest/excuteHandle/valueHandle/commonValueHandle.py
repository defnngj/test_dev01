# -*- coding: utf-8 -*- 
'''
Created on 2017年8月11日

@author: anonymous
'''
import re,traceback
from itest.excuteHandle.valueHandle.myFuncHandle import myFuncHandleClass

class CommonValueHandle:
    
    """
    文本替换，如果存在着${变量} 这种情况，则进行替换
    """
    @staticmethod
    def valueReplace(origin,values):
        if not origin or not values:
            return origin
        try:
            newStr = CommonValueHandle.text2str(origin)
            matchList = re.findall(r'\${([^}]+)}',newStr)

            for s in matchList:
                for v in values:
                    v = CommonValueHandle.text2str(v)
                    if(s==v):
                        tmp = "${"+s+"}"
                        ss = CommonValueHandle.text2str(values[v])
                        newStr = newStr.replace(tmp,ss)
                    else:
                        pass
            newStr = myFuncHandleClass().functionReplace(newStr)
            return newStr
        except:
            traceback.print_exc()
            return origin
    
    """
    文本相等判断
    """
    @staticmethod
    def textCompare(first,second):
        if not first and not second:
            return True
        
        if not (isinstance(first, str) or isinstance(first, unicode)):
            first = str(first)
        if not (isinstance(second, str) or isinstance(second, unicode)):
            second = str(second)
            
        if isinstance(first, str):
            first = first.decode("utf-8")
        if isinstance(second, str):
            second = second.decode("utf-8")
        return (first == second)
    
    """
    文本转化为str
    """
    @staticmethod
    def text2str(text):
        if not text:
            return ""
        if not (isinstance(text, str) or isinstance(text, unicode)):
            try:
                text = str(text)
            except:
                return ""
        if isinstance(text, str):
            return text
        else:
            return text.encode("utf-8")
    """
    文本转化为unicode
    """
    @staticmethod
    def text2unicode(text):
        if not text:
            return u""
        if not (isinstance(text, str) or isinstance(text, unicode)):
            text = str(text)
            
        if isinstance(text, str):
            return text.decode("utf-8")
        else:
            return text

if __name__ == '__main__':
    a= "asdfsaf${12}sdfasdf订单1${12}"
    b={}
    b["12"] = u"qwerq"
    print(CommonValueHandle.valueReplace(a,b))