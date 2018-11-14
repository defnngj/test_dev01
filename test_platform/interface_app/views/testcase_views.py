import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from interface_app.form import TestCaseForm
from interface_app.models import TestCase
from project_app.models import Project, Module
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
                module_name.append(module.name)
            
            project_dict["moduleList"] = module_name
            dataList.append(project_dict)

    return JsonResponse({"success":"true", "data":dataList})



# 用例列表
def case_manage(request):
    testcases = TestCase.objects.all()
    paginator = Paginator(testcases, 2)

    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    
    if request.method == "GET":
        return render(request, "case_manage.html",{
            "type": "list",
            "testcases": contacts,
        })
    else:
        return HttpResponse("404")


# 搜索用例的名称
def search_case_name(request):
    
    if request.method == "GET":
        case_name = request.GET.get('case_name', "")
        cases = TestCase.objects.filter(name__contains=case_name)
        
        paginator = Paginator(cases, 2)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页数不是整型, 取第一页.
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页数超出查询范围，取最后一页
            contacts = paginator.page(paginator.num_pages)
        
        return render(request, "case_manage.html", {
            "type": "list",
            "testcases": contacts,
            "case_name": case_name,
        })
    else:
        return HttpResponse("404")


# 创建/调试用例
def add_case(request):
    if request.method == "GET":
        form = TestCaseForm()
        return render(request, "add_case.html", {
            "form": form,
            "type": "add"
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


# 编辑/调试用例
def debug_case(request, cid):
    print("调试的用例id", cid)

    if request.method == "GET":
        form = TestCaseForm()
        return render(request, "debug_case.html", {
            "form": form,
            "type": "debug"
        })
    else:
        return HttpResponse("404")

# 获取接口信息接口
def get_case_info(request):
    if request.method == "POST":
        case_id = request.POST.get("caseId", "")
        if case_id == "":
           return JsonResponse({"success":"false", "message":"case id Null."})
        case_obj = TestCase.objects.get(pk=case_id)
        case_info = {
            "name": case_obj.name,
            "url": case_obj.url,
            "req_method": case_obj.req_method,
            "req_type": case_obj.req_type,
            "req_header": case_obj.req_header,
            "req_parameter": case_obj.req_parameter,
        }
        return JsonResponse({"success": "true", "message": "ok", "data": case_info})

    else:
        return HttpResponse("404")
