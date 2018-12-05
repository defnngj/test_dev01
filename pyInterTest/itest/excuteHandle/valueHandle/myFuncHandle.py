#coding=utf-8
'''
Created on 2017年12月11日

@author: anonymous
'''
import time,random,re,traceback
from itest.util import globalVars

class myFuncHandleClass:

    """
    自定义函数,获取时间
    """
    def myFuncGetTime(self):
        now = int(time.time()*1000)
        now = str(now)
        return now
        
    """
    自定义函数,获取随机数
    """
    def myFuncGetRandom(self,r=100):
        return random.randint(0,r)

    def functionReplace(self,ss):
        try:
            newStr = str(ss)
            func_time = self.myFuncGetTime()
            newStr = newStr.replace("${func_time}",func_time)

            matchList = re.findall(r'\${func_random\((\d*)\)}', newStr)
            for i in matchList:
                if not i:
                    s = self.myFuncGetRandom()
                    newStr = newStr.replace("${func_random()}", str(s))
                else:
                    p = int(i)
                    s = self.myFuncGetRandom(p)
                    newStr = newStr.replace("${func_random("+i+")}", str(s))
            return newStr
        except:
            traceback.print_exc()
            return ss

if __name__=="__main__":
    print(myFuncHandleClass().functionReplace("${func_random(20)}asdd${func_random(3)}ddd${func_time}fg"))
