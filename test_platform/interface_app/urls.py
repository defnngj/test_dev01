from django.urls import path
from interface_app.views import testcase_views
from interface_app.views import testcase_api
from interface_app.views import testtask_view
from interface_app.views import testtask_api



urlpatterns = [
    # guest system interface:
    # ex : /interface/case_manage/
    # 用例管理
    path('case_manage/', testcase_views.case_manage),
    path('add_case/', testcase_views.add_case),
    path('search_case_name/', testcase_views.search_case_name),
    path("debug_case/<int:cid>/", testcase_views.debug_case),

    # 用例管理 -- 由JS调用的接口
    path('get_project_list', testcase_api.get_project_list),
    path('api_debug/', testcase_api.api_debug),
    path("api_assert/", testcase_api.api_assert),
    path('save_case/', testcase_api.save_case),
    path('update_case/', testcase_api.update_case),
    path("get_case_info/", testcase_api.get_case_info),

    # 任务管理
    path('task_manage/', testtask_view.task_manage),
    path('add_task/', testtask_view.add_task),
    path('edit_task/<int:tid>/', testtask_view.edit_task),
    path('task_result_list/<int:tid>/', testtask_view.task_result_list),

    # 任务管理--由JS调用的接口
    path('get_case_list', testcase_api.get_case_list),
    path('save_task_data/', testtask_api.save_task_data),
    path('run_task/', testtask_api.run_task),
    path('task_result/', testtask_api.task_result),
    path('get_task_info/', testtask_api.get_task_info),
    path('updata_task/', testtask_api.updata_task),
    path('delete_task/', testtask_api.delete_task),

]


