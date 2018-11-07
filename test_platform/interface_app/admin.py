from django.contrib import admin
from interface_app.models import TestCase

# project = models.ForeignKey(Project, on_delete=models.CASCADE)
# module = models.ForeignKey(Module, on_delete=models.CASCADE)
# name = models.CharField("名称", max_length=100, blank=False, default="")
# url = models.TextField("URL", default="")
# req_method = models.CharField("方法", max_length=10, default="")
# req_type = models.CharField("参数类型", max_length=10, default="")
# req_header = models.TextField("header", default="")
# req_parameter = models.TextField("参数", default="")
# reponses_assert = models.TextField("验证", default="")


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['module', 'name', 'url', 'req_method',
                    'req_type', 'req_header', 'req_parameter', 'reponses_assert']

admin.site.register(TestCase, TestCaseAdmin)
