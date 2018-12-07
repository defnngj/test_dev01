import sys
import json
import unittest
from ddt import ddt, data, file_data, unpack
import requests
import xmlrunner
from os.path import dirname, abspath
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
BASE_PATH = BASE_DIR.replace("\\", "/")
sys.path.append(BASE_PATH)

print("运行测试文件：", BASE_PATH)

# 定义任务的目录
TASK_PATH = BASE_PATH + "/resource/tasks/"


@ddt
class InterfaceTest(unittest.TestCase):

    @unpack
    @file_data(TASK_PATH + "cases_data.json")
    def test_run_casess(self, url, method, type_, header, parameter, assert_):
        print("URL", url)
        print("方法", method)

        if header == "{}":
            header_dict = {}
        else:
            aa = header.replace("\'", "\"")
            header_dict = json.loads(aa)

        if parameter == "{}":
            parameter_dict = {}
        else:
            aa = parameter.replace("\'", "\"")
            parameter_dict = json.loads(aa)

        if method == "get":
            if type_ == "from":
                r = requests.get(url, headers=header_dict, params=parameter_dict)
 
        if method == "post":
            if type_ == "from":
                r = requests.post(url, headers=header_dict, data=parameter_dict)
            elif type_ == "json":
                r = requests.post(url, headers=header_dict, json=parameter_dict)



# 运行测试用例
def run_cases():
    with open(TASK_PATH + 'results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)


if __name__ == '__main__':
    run_cases()
