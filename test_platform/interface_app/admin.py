from django.contrib import admin
from interface_app.models import TestCase, TestTask


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'req_method',
                    'req_type', 'req_header', 'req_parameter', 'resp_assert']


class TestTaskAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'describe', 'cases']


admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(TestTask, TestTaskAdmin)
