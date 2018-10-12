from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project_app.models import Project


@login_required
def project_manage(request):
    """
    项目列表管理
    """
    username = request.session.get('user1', '')
    project_all = Project.objects.all()
    return render(request, "project_manage.html", {
        "user": username,
        "projects": project_all,
        "type": "list"
    })


@login_required
def add_project(request):
    """
    添加项目
    """
    return render(request, "project_manage.html", {"type": "add"})

