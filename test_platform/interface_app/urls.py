from django.urls import path
from interface_app.views import testcase_views


urlpatterns = [
    # guest system interface:
    # ex : /intereface/case_manage/
    # 用例管理
    path('case_manage/', testcase_views.case_manage),
    path('add_case/', testcase_views.add_case),
    path('api_debug/', testcase_views.api_debug),
    path('save_case/', testcase_views.save_case),
    path('get_porject_list', testcase_views.get_porject_list),
    path('search_case_name/', testcase_views.search_case_name),
    path("debug_case/<int:cid>/", testcase_views.debug_case),
    path("get_case_info/", testcase_views.get_case_info),
    path("api_assert/", testcase_views.api_assert),
    
]


