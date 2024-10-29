from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.conf import settings
from importlib import reload
import sys
import json
from routes.models import MockHTTPEntity
from functools import partial


class RouteHandlerView(View):
    data = {}

    def findMockEntity(self, method):
        for mock_entity in self.data:
            if mock_entity.get("method") == method:
                return mock_entity
        return None

    def getStatus(self, mock_entity):
        return mock_entity.get("status", 200)
    
    def not_found_resp(self):
        not_found_resp_message = {"success" : False, "message" : "Not Found!"}
        return HttpResponse(json.dumps(not_found_resp_message), content_type="application/json", status=404)

    def getHttpResponse(self, method):
        mock_entity = self.findMockEntity(method=method)
        if mock_entity == None:
            return self.not_found_resp()
        return HttpResponse(json.dumps(mock_entity.get("response")), content_type="application/json", status=self.getStatus(mock_entity))

    def get(self, request, *args, **kwargs):
        return self.getHttpResponse(method="GET")

    def post(self, request, *args, **kwargs):
        return self.getHttpResponse(method="POST")  
    
    def put(self, request, *args, **kwargs):
        return self.getHttpResponse(method="PUT") 

    def patch(self, request, *args, **kwargs):
        return self.getHttpResponse(method="PATCH")   
    
    def delete(self, request, *args, **kwargs):
        return self.getHttpResponse(method="DELETE") 

    def head(self, request, *args, **kwargs):
        return self.getHttpResponse(method="HEAD") 

    def options(self, request, *args, **kwargs):
        return self.getHttpResponse(method="OPTIONS")   

     
   