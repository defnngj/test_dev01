# coding=utf-8
import datetime
import traceback
from itest.models.token import Token


class TokenDao(object):
    def __init__(self):
        pass

    @classmethod
    def get_token_by_user(cls, user):
        try:
            token_obj = Token.objects.get(user=user)  # 查找数据
        except Token.DoesNotExist:
            return None
        else:
            return token_obj

    @classmethod
    def get_token_by_token(cls, token):
        try:
            token_obj = Token.objects.get(Token=token)  # 查找数据
        except Token.DoesNotExist:
            return None
        else:
            return token_obj

    @classmethod
    def del_token(cls, token):
        try:
            token_obj = Token.objects.get(Token=token)  # 查找数据
        except Token.DoesNotExist:
            return False
        else:
            token_obj.delete()
            return True

    @classmethod
    def update_token(cls, token_obj, token, time):
        try:
            token_obj.expireDate = time
            token_obj.Token = token
            token_obj.save()
        except Exception:
            traceback.print_exc()
            return False
        else:
            return True

    @classmethod
    def create_token(cls, user, token, time):
        try:
            token = Token.objects.create(user=user, expireDate=time, Token=token)
        except Exception:
            traceback.print_exc()
            return None
        else:
            return token
