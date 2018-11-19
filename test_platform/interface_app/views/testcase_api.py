import json
import requests
from test_platform import common
from interface_app.models import TestCase
from project_app.models import Project, Module

"""
说明：该文件中的接口由前段JS调用，返回JSON格式数据。
"""


def get_project_list(request):
    """
    获取项目模块列表
    :param request:
    :return: 项目接口列表
    """
    if request.method == "GET":
        project_list = Project.objects.all()
        data_list = []
        for project in project_list:
            project_dict = {
                "name": project.name
            }
            module_list = Module.objects.filter(project_id=project.id)
            if len(module_list) != 0:
                module_name = []
                for module in module_list:
                    module_name.append(module.name)

                project_dict["moduleList"] = module_name
                data_list.append(project_dict)

        return common.response_succeed(data=data_list)

    else:
        return common.response_failed("请求方法错误")


def api_debug(request):
    """
    HTTP接口调试
    :param request:
    :return: 接口调用结果
    """
    if request.method == "POST":
        url = request.POST.get("req_url", "")
        method = request.POST.get("req_method", "")
        type_ = request.POST.get("req_type", "")
        parameter = request.POST.get("req_parameter", "")

        if url == "" or method == "" or type_ == "":
            return common.response_failed("必传参数为空")

        payload = json.loads(parameter.replace("'", "\""))

        if method == "get":
            if type_ == "from":
                r = requests.get(url, params=payload)
            else:
                return common.response_failed("参数类型错误")

        if method == "post":
            if type_ == "from":
                r = requests.post(url, data=payload)
            elif type_ == "json":
                r = requests.post(url, json=payload)
            else:
                return common.response_failed("参数类型错误")

        return common.response_succeed(data=r.text)
    else:
        return common.response_failed("请求方法错误")


def api_assert(request):
    """
    对测试用例的断言进行验证
    :param request:
    :return:
    """
    if request.method == "POST":
        result_text = request.POST.get("result", "")
        assert_text = request.POST.get("assert", "")

        if result_text == "" or assert_text == "":
            return common.response_failed("验证的数据不能为空")

        try:
            assert assert_text in result_text
        except AssertionError:
            return common.response_failed("验证失败!")
        else:
            return common.response_succeed("验证成功!")
    else:
        return common.response_failed("请求方法错误")


def save_case(request):
    """
    保存接口测试用例
    :param request:
    :return:
    """
    if request.method == "POST":
        name = request.POST.get("name", "")
        url = request.POST.get("req_url", "")
        method = request.POST.get("req_method", "")
        parameter = request.POST.get("req_parameter", "")
        req_type = request.POST.get("req_type", "")
        header = request.POST.get("header", "")
        module_name = request.POST.get("module", "")
        assert_text = request.POST.get("assert_text", "")

        if url == "" or method == "" or req_type == "" or module_name == "" or assert_text == "":
            return common.response_failed("必传参数为空")

        if parameter == "":
            parameter = "{}"

        if header == "":
            header = "{}"

        module_obj = Module.objects.get(name=module_name)
        case = TestCase.objects.create(name=name, module=module_obj, url=url,
                                       req_method=method, req_header=header,
                                       req_type=req_type,
                                       req_parameter=parameter, resp_assert=assert_text)
        if case is not None:
            return common.response_succeed("保存成功！")

    else:
        return common.response_failed("请求方法错误")


def get_case_info(request):
    """
    获取接口数据
    :param request:
    :return:
    """
    if request.method == "POST":
        case_id = request.POST.get("caseId", "")
        if case_id == "":
            return common.response_failed("用例id为空")

        case_obj = TestCase.objects.get(pk=case_id)
        module_obj = Module.objects.get(id=case_obj.module_id)
        module_name = module_obj.name  # 模块名称

        project_name = Project.objects.get(id=module_obj.project_id).name  # 项目名称

        case_info = {
            "moduleName": module_name,
            "projectName": project_name,
            "name": case_obj.name,
            "url": case_obj.url,
            "reqMethod": case_obj.req_method,
            "reqType": case_obj.req_type,
            "reqHeader": case_obj.req_header,
            "reqParameter": case_obj.req_parameter,
            "assertText": case_obj.resp_assert,
        }

        return common.response_succeed(data=case_info)

    else:
        return common.response_failed("请求方法错误")

