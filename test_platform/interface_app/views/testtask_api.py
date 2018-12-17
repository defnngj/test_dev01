from test_platform import common
from interface_app.models import TestTask, TestResult
from interface_app.extend.task_thread import TaskThread


"""
说明：该文件中的接口由前段JS调用，返回JSON格式数据。
"""


# 保存任务
def save_task_data(request):
    if request.method == "POST":
        name = request.POST.get("task_name", "")
        describe = request.POST.get("task_describe", "")
        cases = request.POST.get("task_cases", "")
        if name == "":
            return common.response_failed("任务的名称不能为空")

        # 保存数据库
        task = TestTask.objects.create(name=name, describe=describe, cases=cases)
        if task is None:
            return common.response_failed("创建失败")

        return common.response_succeed(message="创建任务成功！")
    else:
        return common.response_failed("请求方法错误")


# 运行任务
def run_task(request):
    if request.method == "POST":
        tid = request.POST.get("task_id", "")
        if tid == "":
            return common.response_failed("任务ID不能为空")

        task_list = TestTask.objects.all()
        runing_task = 0
        for task in task_list:
            if task.status == 1:
                runing_task = 1
                break
        if runing_task == 1:
            return common.response_failed("当前有任务正在执行...")
        else:
            TaskThread(tid).new_run()
            return common.response_succeed(message="已执行")
    else:
        return common.response_failed("请求方法错误")


# 查看任务结果
def task_result(request):
    if request.method == "POST":
        rid = request.POST.get("result_id", "")
        result_obj = TestResult.objects.get(id=rid)
        data = {
            "result": result_obj.result,
        }
        return common.response_succeed(message="获取成功！", data=data)
    else:
        return common.response_failed("请求方法错误")
