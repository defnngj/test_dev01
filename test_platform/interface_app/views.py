from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def case_manage(request):
    if request.method == "GET":
        return render(request, "case_manage.html",{
            "type": "list"
        })
    else:
        return HttpResponse("404")


# 创建/调试接口
def api_debug(request):
    if request.method == "GET":
        return render(request, "api_debug.html", {
            "type": "debug"
        })
    else:
        return HttpResponse("404")
