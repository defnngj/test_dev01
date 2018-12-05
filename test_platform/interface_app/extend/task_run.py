import unittest
from ddt import ddt, data, file_data, unpack
import requests
import xmlrunner

global case1
global case2

case = {'first': 1, 'second': 3, 'third': 2}
case1 = {'url': 'http://httpbin.org/post', 'method': 'post', 'data': {'key': 'value'}}
case2 = {'url': 'https://api.github.com/events', 'method': 'get', 'data': {}}

@ddt
class MyTest(unittest.TestCase):

    @unpack
    @data(case1,
          case2)
    def test_dicts_extracted_into_kwargs(self, url, method, data):
        # print("URL", url)
        # print("方法", method)
        # print("参数", data)
        if method == "post":
            r = requests.post(url, data=data)
            self.assertEqual(2+1, 4)

        if method == "get":
            r = requests.get(url, params=data)
            #print(r.text)
            self.assertEqual(2+2, 4)

# 运行测试用例
def run_cases():
    with open('D:/class_dev/test_dev_sample/test_platform/interface_app/extend/results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)

if __name__ == '__main__':
    run_cases()
