from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from project_app.models import Project
from .forms import ProjectForm


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
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            print(name)
            print(describe)
            Project.objects.create(name=name, describe=describe)
            # process the data in form.cleaned_data as required
            # 
            # redirect to a new URL:
            return HttpResponseRedirect('/manage/project_manage/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm()

    return render(request, 'project_manage.html', {
        'form': form,
        "type": "add",
        })


def edit_project(request, pid):
    print("编辑项目的id:", pid)
    if request.method == 'POST':
        pass
    else:
        form = ProjectForm()

    return render(request, 'project_manage.html', {
        'form': form,
        "type": "edit",
    })
