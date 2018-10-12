from django.urls import path
from project_app import views


urlpatterns = [
    # guest system interface:
    # ex : /manage/project_manage/
    path('project_manage/', views.project_manage),
    path('add_project/',  views.add_project)
]
