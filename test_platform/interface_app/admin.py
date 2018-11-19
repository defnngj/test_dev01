from django.contrib import admin
from interface_app.models import TestCase


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ['module', 'name', 'url', 'req_method',
                    'req_type', 'req_header', 'req_parameter', 'resp_assert']


admin.site.register(TestCase, TestCaseAdmin)
