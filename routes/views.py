import json
import sys
from importlib import reload

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import clear_url_caches

from common.constants import allowed_http_methods, urls_already_in_use
from common.exceptions import RequestRejectedException
from common.request_util import allowed_values, is_blank, is_none
from main.settings import collection_mock_call
from route_holder import urls


def add_route(request):
    try:
        if request.method == "POST":
            request_body = json.loads(request.body)
            validateAddRouteRequestBody(request_body)
            validateIfMockAlreadyPresent(request_body)
            collection_mock_call.insert_one(request_body)
            urls.add_route()
            resp = {"success": True, "message": "Endpoint added successfully!"}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if request.method == "PUT":
            request_body = json.loads(request.body)
            validateUpdateRouteRequestBody(request_body)
            url = request_body.get("url")
            method = request_body.get("method")
            query = {"method": method, "url": url}
            update_result = collection_mock_call.replace_one(
                query, request_body, upsert=True
            )
            updated_existing = update_result.raw_result.get("updatedExisting")
            message = (
                "Endpoint updated successfully!"
                if updated_existing
                else "Endpoint added successfully!"
            )
            urls.update_routes()
            resp = {"success": True, "message": message}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if request.method == "DELETE":
            request_body = json.loads(request.body)
            validateDeleteRouteRequestBody(request_body)
            url = request_body.get("url")
            method = request_body.get("method")
            query = {"method": method, "url": url}
            collection_mock_call.delete_one(query)
            urls.update_routes()
            resp = {"success": True, "message": "Endpoint deleted successfully!"}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # For invalid methods
        resp = {"success": False, "message": "Method Not Allowed"}
        return HttpResponse(
            json.dumps(resp), content_type="application/json", status=405
        )

    except RequestRejectedException as ex:
        message = str(ex)
        resp = {"success": False, "message": message}
        return HttpResponse(
            json.dumps(resp), status=ex.status, content_type="application/json"
        )


def validateAddRouteRequestBody(request_body):
    validateAddOrUpdateRouteRequestBody(request_body=request_body)


def validateUpdateRouteRequestBody(request_body):
    validateAddOrUpdateRouteRequestBody(request_body=request_body)


def validateDeleteRouteRequestBody(request_body):
    url = request_body.get("url")
    method = request_body.get("method")
    validateURL(url)
    validateMethod(method)


def validateAddOrUpdateRouteRequestBody(request_body):
    url = request_body.get("url")
    response = request_body.get("response")
    method = request_body.get("method")
    status = request_body.get("status")
    headers = request_body.get("headers")
    validateURL(url)
    is_none(param=response, message="response can not be null.")
    validateMethod(method)
    validateStatus(status)
    validateHeaders(headers)


def validateIfMockAlreadyPresent(request_body):
    url = request_body.get("url")
    method = request_body.get("method")
    mock_request = collection_mock_call.find_one({"url": url, "method": method})
    if mock_request != None:
        raise RequestRejectedException(
            message="A record with this url and method already exists!", status=400
        )


def validateURL(url):
    is_none(param=url, message="url can not be null.")
    if type(url) is not str:
        raise RequestRejectedException(message="url is not a string.", status=400)
    if url in urls_already_in_use:
        raise RequestRejectedException(
            message="This is an application url, can not be used!", status=400
        )
    is_blank(param=url, message="url can not be null or blank.")


def validateMethod(method):
    if type(method) is not str:
        raise RequestRejectedException(message="method is not a string.", status=400)
    allowed_values(
        param=method,
        allowed_values=allowed_http_methods,
        message=method + " is not a valid value.",
    )


def validateStatus(status):
    if status == None:
        return
    if type(status) is not int:
        raise RequestRejectedException(message="status is not an integer.", status=400)
    if status > 599 or status < 100:
        raise RequestRejectedException(
            message="Invalid status code passed.", status=400
        )


def validateHeaders(headers):
    if headers == None:
        return
    if isinstance(headers, dict):
        return
    raise RequestRejectedException(message="Invalid headers passed.", status=400)
