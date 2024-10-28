from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from importlib import reload
from django.urls import clear_url_caches
from main.settings import collection_mock_call
import json
import sys
from . import urls 
from routes.models import MockHTTPEntity

def testing(request):
    if(request.method == "POST"):
        http_dict = json.loads(request.body)
        mock_http_entity = MockHTTPEntity(http_dict)
        print(mock_http_entity)
        collection_mock_call.insert_one(http_dict)
        urls.add_route(data=mock_http_entity)
        resp = {"success" : True, "message" : "Endpoint added successfully!"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp  = {"success" : False, "message" : "Not Found!"}
        return HttpResponse(json.dumps(resp), content_type="application/json", status=404)
 
