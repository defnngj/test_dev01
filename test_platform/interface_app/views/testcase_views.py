import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from interface_app.form import TestCaseForm
from interface_app.models import TestCase
from project_app.models import Project, Module


# 获取项目模块列表
def get_porject_list(request):
    project_list = Project.objects.all()
    dataList = []
    for project in project_list:
        project_dict = {
            "name": project.name
        }
        module_list = Module.objects.filter(project_id=project.id)
        if len(module_list) != 0:
            module_name = []
            for module in module_list:
                print(module_name)
                module_name.append(module.name)
            
            project_dict["moduleList"] = module_name
            dataList.append(project_dict)

    return JsonResponse({"success":"true", "data":dataList})



# 用例列表
def case_manage(request):
    if request.method == "GET":
        return render(request, "case_manage.html",{
            "type": "list"
        })
    else:
        return HttpResponse("404")


# 创建/调试接口
def debug(request):
    if request.method == "GET":
        form = TestCaseForm()
        return render(request, "api_debug.html", {
            "form": form,
            "type": "debug"
        })
    else:
        return HttpResponse("404")


# 调试接口
def api_debug(request):

    if request.method == "POST":
        url = request.POST.get("req_url")
        method = request.POST.get("req_method")
        parameter = request.POST.get("req_parameter")

        payload = json.loads(parameter.replace("'", "\""))
        
        if method == "get":
            r = requests.get(url, params=payload)

        if method == "post":
            r = requests.post(url, data=payload)
        
        return HttpResponse(r.text)


def save_case(request):
    """
    保存测试用例
    """
    if request.method == "POST":
        name = request.POST.get("name", "")
        url = request.POST.get("req_url", "")
        method = request.POST.get("req_method",  "")
        parameter = request.POST.get("req_parameter", "")
        req_type = request.POST.get("req_type", "")
        header = request.POST.get("header", "")
        module_name = request.POST.get("module", "")

        if url == "" or method == "" or req_type == "" or module_name == "":
            return HttpResponse("必传参数为空")
        
        if parameter == "":
            parameter= "{}"
        
        if header == "":
            header = "{}"
        
        module_obj = Module.objects.get(name=module_name)

        case = TestCase.objects.create(name=name, module=module_obj, url=url, 
                                       req_method=method, req_header= header,
                                       req_type=req_type,
                                       req_parameter=parameter)
        if case is not None:
            return HttpResponse("保存成功！")
        
    else:
         return HttpResponse("404")
