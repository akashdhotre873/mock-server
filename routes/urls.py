from django.urls import path, clear_url_caches
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from importlib import reload
import sys
import json
from . import views
from routes.models import MockHTTPEntity
from functools import partial


urlpatterns = [
    path("", views.testing, name="index")
]



def add_route(data:MockHTTPEntity):
    updateUrl(data)


def resp(response):
    return HttpResponse(json.dumps(response), content_type="application/json")




def updateUrl(data: MockHTTPEntity):
    global urlpatterns

    def wrapper_for_fun(request):
        partial_fun = partial(resp, data.response)
        return partial_fun()
        
    url = "/" + data.url
    urlpatterns = urlpatterns +  [path(url, wrapper_for_fun, name=data.name)]
    
    urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
      clear_url_caches()
      reload(sys.modules[urlconf])
