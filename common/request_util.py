from django.http import HttpResponse

from .exceptions import RequestRejectedException


def is_none(param, message = "value can not be null."):
    if param == None:
        resp = {"success" : False, "message" : message}
        raise RequestRejectedException(message=message, status=400)

def is_blank(param: str, message = "value can not be null or blank."):
    if param == None or param == "" or param.isspace():
        raise RequestRejectedException(message=message, status=400)

def allowed_values(param: str, allowed_values: list, message = "Given value is not allowed."):
    if param not in allowed_values:
        raise RequestRejectedException(message=message, status=400)
