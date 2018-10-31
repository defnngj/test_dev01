from django.urls import path
from interface_app import views


urlpatterns = [
    # guest system interface:
    # ex : /intereface/case_manage/
    # 用例管理
    path('case_manage/', views.case_manage),
    path('api_debug/', views.api_debug),
    
]


