from django.shortcuts import render
from django.http import HttpResponse
from interface_app.models import TestCase
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

"""
说明：接口用例文件，返回HTML页面
"""


# 获取用例列表
def case_manage(request):
    testcases = TestCase.objects.all()
    paginator = Paginator(testcases, 5)

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
        return render(request, "case_manage.html", {
            "type": "list",
            "testcases": contacts,
        })
    else:
        return HttpResponse("404")


# 根据用例名称搜索
def search_case_name(request):
    
    if request.method == "GET":
        case_name = request.GET.get('case_name', "")
        cases = TestCase.objects.filter(name__contains=case_name)
        
        paginator = Paginator(cases, 5)
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


# 创建接口测试用例
def add_case(request):
    if request.method == "GET":
        return render(request, "add_case.html", {
            "type": "add"
        })
    else:
        return HttpResponse("404")


# 编辑接口测试用例
def debug_case(request, cid):
    print("调试的用例id", cid)

    if request.method == "GET":
        return render(request, "debug_case.html", {
            "type": "debug"
        })
    else:
        return HttpResponse("404")
