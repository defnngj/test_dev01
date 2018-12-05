# coding=utf-8
from itest.models.user import Users


class UsersDao(object):

    def __init__(self):
        pass

    @staticmethod
    def get_user(user_name, pwd):
        if not user_name or not pwd:
            return None
        try:
            user_obj = Users.objects.get(user=user_name, pwd=pwd)
        except Users.DoesNotExist:
            return None
        else:
            return user_obj

    @staticmethod
    def get_user_by_id(user_id):
        if not user_id:
            return None
        try:
            user_obj = Users.objects.get(id=int(user_id))
        except Users.DoesNotExist:
            return None
        else:
            return user_obj

    @staticmethod
    def get_user_by_all(user_name, pwd, user_id):
        if not user_name or not pwd or not user_id:
            return None
        try:
            user_obj = Users.objects.get(user=user_name, pwd=pwd, id=int(user_id))
        except Users.DoesNotExist:
            return None
        else:
            return user_obj

    @staticmethod
    def get_user_by_name(user_name):
        if not user_name:
            return None
        try:
            user_obj = Users.objects.get(user=user_name)
        except Users.DoesNotExist:
            return None
        else:
            return user_obj

    @classmethod
    def create_user(cls, user_name, pwd):
        try:
            new_user = Users.objects.create(user=user_name, pwd=pwd)
        except Exception:
            return None
        else:
            return new_user

    @classmethod
    def update_user_pwd(cls, user_obj, pwd):
        try:
            user_obj.pwd = pwd
            user_obj.save()
        except Exception:
            return None
        else:
            return True
