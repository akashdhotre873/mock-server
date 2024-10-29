from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from importlib import reload
from django.urls import clear_url_caches
from main.settings import collection_mock_call
import json
import sys
from route_holder import urls 

def add_route(request):
    if(request.method == "POST"):
        http_dict = json.loads(request.body)
        collection_mock_call.insert_one(http_dict)
        urls.add_route()
        resp = {"success" : True, "message" : "Endpoint added successfully!"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        resp  = {"success" : False, "message" : "Not Found!"}
        return HttpResponse(json.dumps(resp), content_type="application/json", status=404)
 
