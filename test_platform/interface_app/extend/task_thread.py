import os
import json
import threading
from time import sleep
from interface_app.models import TestTask
from interface_app.models import TestCase
from interface_app.models import TestResult
from interface_app.apps import TASK_PATH, RUN_TASK_FILE
from xml.dom import minidom


class TaskThread():
    """实现测试任务的多线程执行"""

    def __init__(self, task_id):
        self.tid = task_id

    def run_cases(self,  tid):
        task_obj = TestTask.objects.get(id=tid)
        cases_list = task_obj.cases.split(",")
        cases_list.pop(-1)
        task_obj.status = 1   # 修改状态改为执行中
        task_obj.save()

        print(cases_list)
        # run_cases()  #运行函数
        all_cases_dict = {}
        for case_id in cases_list:
            case_obj = TestCase.objects.get(id=case_id)
            case_dict = {
                "url": case_obj.url,
                "method": case_obj.req_method,
                "type_": case_obj.req_type,
                "header": case_obj.req_header,
                "parameter": case_obj.req_parameter,
                "assert_": case_obj.resp_assert
            }
            all_cases_dict[case_obj.id] = case_dict

        print(all_cases_dict)

        cases_str = json.dumps(all_cases_dict)

        cases_data_file = TASK_PATH + "cases_data.json"
        print(cases_data_file)

        with open(cases_data_file, "w+") as f:
            f.write(cases_str)

        # 运行测试
        os.system("python3 " + RUN_TASK_FILE)

    def save_result(self):
        """保存测试结果"""
        dom = minidom.parse(TASK_PATH + 'results.xml')
        root = dom.documentElement
        ts = root.getElementsByTagName('testsuite')
        print("errors", ts[0].getAttribute("errors"))
        print("fail", ts[0].getAttribute("failures"))
        print("tests", ts[0].getAttribute("tests"))

        # TestResult.objects.create("") 保存到结果表里面

    def run(self):
        threads = []
        t = threading.Thread(target=self.run_cases, args=(self.tid,))
        threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()
        sleep(2)
        print("当（任务）线程运行完成之后...")
        self.save_result()

        task_obj = TestTask.objects.get(id=self.tid)
        task_obj.status = 2  # 修改状态执行完成
        task_obj.save()

    def new_run(self):
        threads = []
        t = threading.Thread(target=self.run)
        threads.append(t)

        for t in threads:
            t.start()
