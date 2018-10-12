from django.contrib import admin
from project_app.models import Project, Module


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'status', 'create_time', 'id']


class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'create_time', 'project', 'id']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Module, ModuleAdmin)
