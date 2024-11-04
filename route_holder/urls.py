import json
import sys
from functools import partial
from importlib import reload

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import clear_url_caches, path

from main.settings import collection_mock_call
from routes.models import MockHTTPEntity

from . import views

urlpatterns = []


def reloadURLsWrapper():
    reloadUrls()


def add_route():
    reloadUrls()


def update_routes():
    reloadUrls()


def resp(request, response):
    return HttpResponse(json.dumps(response), content_type="application/json")


def reloadUrls():
    global urlpatterns
    urlpatterns = []

    parsed_mock_entities = findAndGroupMockEntities()

    for url, parsed_group in parsed_mock_entities.items():
        urlpatterns = urlpatterns + [
            path(url, views.RouteHandlerView.as_view(data=parsed_group))
        ]

    urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        clear_url_caches()
        reload(sys.modules[urlconf])


def findAndGroupMockEntities():
    all_mock_call_entities = collection_mock_call.find({})
    data = {}
    for mock_entity in all_mock_call_entities:
        url = mock_entity.get("url")
        if data.get(url) == None:
            data[url] = []
        data[url].append(mock_entity)
    return data
