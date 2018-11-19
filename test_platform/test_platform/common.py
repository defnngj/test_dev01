from django.http import JsonResponse


def response_succeed(message="请求成功", data={}):
    """
    响应成功
    :param message: 说明
    :param data: 详细数据
    :return:
    """
    content = {
        "success": "true",
        "message": message,
        "data": data,
    }
    return JsonResponse(content)


def response_failed(message="参数错误"):
    """
    响应失败
    :param message:
    :return:
    """
    content = {
        "success": "false",
        "message": message,
    }
    return JsonResponse(content)
