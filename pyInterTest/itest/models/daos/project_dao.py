# coding=utf-8
import traceback
from itest.models.project import Project
from itest.models.apiDefine import ApiDefine
from itest.models.task import TaskModel
from itest.models.user import Users


class ProjectDao(object):
    def __init__(self):
        pass

    @classmethod
    def get_all_projects_list(cls):
        try:
            projects = Project.objects.all()
        except Exception:
            traceback.print_exc()
            return None
        else:
            return projects

    @classmethod
    def get_projects_list_exclude_status_user(cls, status, user_id, exclude):
        if user_id is None and status is None:
            return cls.get_all_projects_list()

        try:
            projects = ""
            if exclude:
                if user_id is None and status is not None:
                    projects = Project.objects.all().exclude(status=int(status))
                if user_id is not None and status is None:
                    projects = Project.objects.all().exclude(user=Users.objects.get(pk=int(user_id)))
                if user_id is not None and status is not None:
                    projects = Project.objects.all().exclude(status=int(status), user=Users.objects.get(pk=int(user_id)))
            else:
                if user_id is None and status is not None:
                    projects = Project.objects.filter(status=int(status))
                if user_id is not None and status is None:
                    projects = Project.objects.filter(user=Users.objects.get(pk=int(user_id)))
                if user_id is not None and status is not None:
                    projects = Project.objects.filter(status=int(status), user=Users.objects.get(pk=int(user_id)))
        except Exception:
            traceback.print_exc()
            return None
        else:
            return projects

    @classmethod
    def transform_projects_content(cls, projects):
        try:
            data_list = list()
            for p in projects:
                tmp = p.get_dict()
                api_count = ApiDefine.objects.filter(project_id=int(p.id)).count()
                task_count = TaskModel.objects.filter(project_id=int(p.id)).count()
                tmp["inter_counts"] = api_count
                tmp["task_counts"] = task_count
                data_list.append(tmp)
        except Exception:
            traceback.print_exc()
            return None
        else:
            return data_list

    @classmethod
    def create_project(cls, name, dec, user, create_time, status):
        try:
            project = Project(name=name, dec=dec, user=user, createTime=create_time, status=status)
            project.save()
        except Exception:
            traceback.print_exc()
            return False
        else:
            return True

    @classmethod
    def update_project_base(cls, project_id, name, dec):
        try:
            project = Project.objects.get(pk=int(project_id))
            project.name = name
            project.dec = dec
            project.save()
        except Exception:
            traceback.print_exc()
            return False
        else:
            return True

    @classmethod
    def update_project_status(cls, project_id, status):
        try:
            project = Project.objects.get(pk=int(project_id))
            project.status = status
            project.save()
        except Exception:
            traceback.print_exc()
            return False
        else:
            return True
