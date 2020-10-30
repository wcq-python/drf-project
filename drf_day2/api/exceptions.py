from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    error = "%s %s %s" % (context["view"], context["request"].method, exc),
    print(error)
    # 先让DRF处理异常,根据返回值来判断异常是否被处理
    response = drf_exception_handler(exc, context)
    # 如果返回None，代表DRF无法处理异常，需要自定义处理
    if response is None:
        return Response({"error_message": "请稍等，程序猿正在加紧处理中。。。"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 如果不为None，说明异常已被处理
    return response
