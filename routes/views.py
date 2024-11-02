from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from importlib import reload
from django.urls import clear_url_caches
from main.settings import collection_mock_call
import json
import sys
from route_holder import urls 
from rest_framework.decorators import api_view
from common.request_util import is_none, is_blank, allowed_values
from common.exceptions import RequestRejectedException
from common.constants import allowed_http_methods



@api_view(['POST'])
def add_route(request):
    try:
        if(request.method == "POST"):
            request_body = json.loads(request.body)
            validateRequestBody(request_body)
            validateIfMockAlreadyPresent(request_body)
            collection_mock_call.insert_one(request_body)
            urls.add_route()
            resp = {"success" : True, "message" : "Endpoint added successfully!"}
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp  = {"success" : False, "message" : "Not Found!"}
            return HttpResponse(json.dumps(resp), content_type="application/json", status=404)
    except RequestRejectedException as ex:
        message = str(ex)
        resp = {"success" : False, "message" : message}
        return HttpResponse(json.dumps(resp), status= ex.status, content_type="application/json")

 
def validateRequestBody(request_body):
    url = request_body.get("url")
    response = request_body.get("response")
    method = request_body.get("method")
    status = request_body.get("status")
    validateURL(url)
    is_none(param=response, message="response can not be null.")
    validateMethod(method)
    validateStatus(status)

def validateIfMockAlreadyPresent(request_body):
    url = request_body.get("url")
    method = request_body.get("method")
    mock_request = collection_mock_call.find_one({"url" :url, "method": method})
    if mock_request != None:
        raise RequestRejectedException(message="A record with this url and method already exists!", status=400)

def validateURL(url):
    if type(url) is not str:
        raise RequestRejectedException(message="url is not a string.", status=400)
    is_blank(param=url, message="url can not be null or blank.")

def validateMethod(method):
    if type(method) is not str:
        raise RequestRejectedException(message="method is not a string.", status=400)
    allowed_values(param=method,allowed_values=allowed_http_methods ,message=method + " is not a valid value.")

def validateStatus(status):
    if status == None:
        return
    if type(status) is not int:
        raise RequestRejectedException(message="status is not an integer.", status=400)
    if status > 599 or status < 100:
        raise RequestRejectedException(message="Invalid status code passed.", status=400)

