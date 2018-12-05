"""pyInterTest URL Configuration

The `urlpatterns` list routes URLs to loginViews. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function loginViews
    1. Add an import:  from my_app import loginViews
    2. Add a URL to urlpatterns:  url(r'^$', loginViews.home, name='home')
Class-based loginViews
    1. Add an import:  from other_app.loginViews import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from itest.scheduler import startSchedule
from django.contrib import admin
from django.conf.urls import handler404, handler500
from itest.views import login_views
from itest.views import project_views
from itest.views import apiViews
from itest.views import caseViews
from itest.views import testSuiteViews
from itest.views import settingViews
from itest.views import requirementViews
from itest.views import taskViews
from itest.views import resultView
from itest.views import statisticsView
from itest.views import otherViews
from itest.views import historyResultViews
# 
handler404 = otherViews.handler404
handler500 = otherViews.handler500

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', login_views.index, name='index'),  # index
    url(r'^index$', login_views.index, name='index'),  # index
    
    url(r'^login$', login_views.login, name='login'),  # login
    url(r'^logout$', login_views.logout, name='logout'),  # login
    url(r'^register$', login_views.register, name='register'),  # register
    url(r'^reset_pwd$', login_views.reset_pwd, name='resetPwd'),  # resetPwd
    url(r'^user_setting_page$', login_views.user_setting_page, name='user_setting_page'),  # userSettingPage
    
    url(r'^project/add$', project_views.add_project, name='add_project'),  # add project
    url(r'^project/lists$', project_views.get_project_list, name='get_project_list'),  # get project list
    url(r'^project/update$', project_views.update_project, name='update_project_base'),  # update project
    url(r'^project/close$', project_views.close_project, name='close_project'),  # close project
    
    url(r'^project/(\d+)$', apiViews.apiPageIndex, name='apiPageIndex'),  # api page index
    
    url(r'^module/add$', apiViews.addApiModule, name='addModule'),  # add module
    url(r'^module/lists$', apiViews.getApiModules, name='getModuleList'),  # get module list
    url(r'^module/update$', apiViews.updateApiModule, name='updateModule'),  # update module
    url(r'^module/delete$', apiViews.deleteApiModule, name='deleteModule'),  # close module
    
    url(r'^api/add$', apiViews.addApi, name='addApi'),  # add api
    url(r'^api/lists$', apiViews.getApiList, name='getApiList'),  # get  api lists
    url(r'^api/delete$', apiViews.deleteApi, name='deleteApi'),  # delete api
    url(r'^api/detail$', apiViews.getApiDetail, name='getApiDetail'),  # get api detail
    url(r'^api/update/name$', apiViews.updateApiName, name='updateApiName'),  # 
    url(r'^api/update/url$', apiViews.updateApiUrl, name='updateApiUrl'),  #
    url(r'^api/update/dec$', apiViews.updateApiDec, name='updateApidec'),  #
    url(r'^api/update/method$', apiViews.updateApiMethod, name='updateApidec'),  #
    url(r'^api/update/addHeader$', apiViews.updateApiAddHeader, name='updateApiAddHeader'),  #
    url(r'^api/update/delHeader$', apiViews.updateApiDelHeader, name='updateApiDelHeader'),  #
    url(r'^api/update/changeHeader$', apiViews.updateApiChangeHeader, name='updateApiChangeHeader'),  #
    url(r'^api/update/parmasType$', apiViews.updateApiParmasType, name='updateApiParmasType'),  #
    url(r'^api/update/addParmas$', apiViews.updateApiAddParmas, name='updateApiAddParmas'),  #
    url(r'^api/update/delParmas$', apiViews.updateApiDelParmas, name='updateApiDelParmas'),  #
    url(r'^api/update/setParmas$', apiViews.updateAPiSetParmas, name='updateApiSetParmas'),  #
    url(r'^api/update/changeParmas$', apiViews.updateApiChangeParmas, name='updateApiChangeParmas'),  #
    url(r'^api/update/responseType$', apiViews.updateApiResponseType, name='updateApiResponseType'),  #
    url(r'^api/update/addResponse$', apiViews.updateApiAddResponse, name='updateApiAddResponse'),  #
    url(r'^api/update/delResponse$', apiViews.updateApiDelResponse, name='updateApiDelResponse'),  #
    url(r'^api/update/setResponse$', apiViews.updateAPiSetResponse, name='updateApiSetResponse'),  #
    url(r'^api/update/changeResponse$', apiViews.updateApiChangeResponse, name='updateApiChangeResponse'),  #
    url(r'^api/debug$', apiViews.apiDebug, name='apiDebug'),  # api debug
    url(r'^api/copy$', apiViews.copyApi, name='copyCase'),  #copy case
    
    url(r'^case/add$', caseViews.addCase, name='addCase'),  #add case
    url(r'^case/detail$', caseViews.caseDetail, name='caseDetail'),  #get case detail
    url(r'^case/update/base$', caseViews.updateCaseBaseInfo, name='updateCaseBase'),  #get case detail
    url(r'^case/update/header$', caseViews.updateCaseHeader, name='updateCaseHeader'),  #update case header
    url(r'^case/update/parmas$', caseViews.updateCaseParmas, name='updateCaseParmas'),  #update case parmas
    url(r'^case/update/picker$', caseViews.updateCasePicker, name='updateCasePicker'),  #update case picker
    url(r'^case/update/assert$', caseViews.updateCaseAssert, name='updateCaseAssert'),  #update case assert
    url(r'^case/update/pre$', caseViews.updateCasePre, name='updateCasePre'),  #update case pre
    url(r'^case/update/post$', caseViews.updateCasePost, name='updateCasePost'),  #update case post
    url(r'^case/delete$', caseViews.deleteCase, name='deleteCase'),  #delete case
    url(r'^case/copy$', caseViews.copyCase, name='copyCase'),  #copy case
    url(r'^case/update/preRequirement$', caseViews.updateCasePreRequirement, name='updateCasePreRequire'),  #update Case PreRequire
    url(r'^case/update/postRequirement$', caseViews.updateCasePostRequirement, name='updateCasePostRequire'),  #update Case PostRequire
    url(r'^case/update/preSql$', caseViews.updateCasePreSql, name='updateCasePreSql'),  #update Case PreSql
    url(r'^case/update/postSql$', caseViews.updateCasePostSql, name='updateCasePostSql'),  #update Case PostSql
    
    url(r'^suite/add$', testSuiteViews.addTestSuite, name='addSuite'),  #add suite
    url(r'^suite/detail$', testSuiteViews.getTestSuite, name='getSuite'),  #get suite detail
    url(r'^suite/update/cases$', testSuiteViews.updateTestSuiteCases, name='updateSuiteCases'),  #update suite cases
    url(r'^suite/delete$', testSuiteViews.deleteTestSuite, name='deleteSuite'),  #delete suite
    url(r'^suite/list$', testSuiteViews.getTestSuiteList, name='getSuiteList'),  #get suite list
    url(r'^suite/update/base$', testSuiteViews.updateTestSuiteBaseInfo, name='updateSuiteBase'),  #update Suite Base
    url(r'^suite/update/pre$', testSuiteViews.updateTestSuitePre, name='updateSuitePre'),  #update Suite pre
    url(r'^suite/update/post$', testSuiteViews.updateTestSuitePost, name='updateSuitePost'),  #update Suite post
    url(r'^suite/update/cases$', testSuiteViews.updateTestSuitePost, name='updateSuitePost'),  #update Suite post
    url(r'^suite/update/requirement$', testSuiteViews.updateSuiteRequirement, name='updateSuiteRequirement'),  #update Suite requirement
    
    url(r'^requirement/add$', requirementViews.addRequirement, name='addRequirement'),  #add requirement
    url(r'^requirement/delete$', requirementViews.deleteRequirement, name='addRequirement'),  #delete requirement 
    url(r'^requirement/add/picker$', requirementViews.requirementAddPicker, name='addRequirementPicker'),  #add requirement  picker
    url(r'^requirement/delete/picker$', requirementViews.requirementDeletePicker, name='deleteRequirementPicker'),  #delete requirement  picker
    url(r'^requirement/get/picker$', requirementViews.requirementGetPicker, name='getRequirementPicker'),  #get requirement picker
    
    url(r'^setting/add/env$', settingViews.addEnv, name='addEnv'),  #add env
    url(r'^setting/update/env$', settingViews.updateEnv, name='addEnv'),  #add env
    url(r'^setting/delete/env$', settingViews.deleteEnv, name='addEnv'),  #add env
    url(r'^setting/env/list$', settingViews.getEnvList, name='getEnvList'),  #get env list
    
    url(r'^setting/assert/list$', settingViews.getSystemAssertList, name='getAssertList'),  #get assert list
    url(r'^setting/add/assert$', settingViews.addSystemAssert, name='addAssert'),  #add assert 
    url(r'^setting/delete/assert$', settingViews.deleteSystemAssert, name='deleteAssert'),  #delete assert 
    
    url(r'^setting/globalValue/list$', settingViews.getGlobalValuesList, name='getGlobalValueList'),  #get global Value list
    url(r'^setting/add/globalValue$', settingViews.addGlobalValues, name='addGlobalValue'),  #add global value
    url(r'^setting/delete/globalValue$', settingViews.deleteGlobalValues, name='deleteGlobalValue'),  #delete global value
    
    url(r'^setting/save/envSql$', settingViews.saveSqlSetting, name='saveSql'),  #save sql
    url(r'^setting/get/envSql$', settingViews.getSqlSetting, name='getSql'),  #get sql
    url(r'^setting/upload/sshKey$', settingViews.uploadSSHKey, name='uploadSSHKey'),  #upload SSH Key
    
    url(r'^task/add$', taskViews.addTask, name='addTask'),  #add task
    url(r'^task/delete$', taskViews.deleteTask, name='deleteTask'),  #delete task
    url(r'^task/update$', taskViews.updateTask, name='updateTask'),  #update task
    url(r'^task/list$', taskViews.getTaskList, name='getTaskList'),  #get task list
    url(r'^task/get$', taskViews.getTask, name='getTask'),  #get single task 
    url(r'^task/getCases$', taskViews.getCasesList, name='getCases'),  #get cases
    url(r'^task/run$', taskViews.runTask, name='runTask'),  #run task
    url(r'^task/getHistory$', taskViews.getTaskHistory, name='getTaskHistory'),  #get Task History list
#     url(r'^task/getHistoryReport$', taskViews.getTaskHistoryReport, name='getTaskHistoryReport'),  #get Task History Report
    
    url(r'^case/getResult$', resultView.getTestCaseResult, name='getCasesResult'),  #get cases result
    
    url(r'^statistics/summary$', statisticsView.getSummary, name='getSummary'),  #get summary
    url(r'^statistics/chart$', statisticsView.getChart, name='getChart'),  #get chart
    
    url(r'^history/(\d+)$', historyResultViews.getHistoryResultPage, name='getHistoryResultPage'),  # history result page
    
    url(r'^test$', apiViews.apitest, name='test'),  # close module
]

startSchedule()
