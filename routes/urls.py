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

