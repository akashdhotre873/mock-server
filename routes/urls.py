from django.urls import path

from . import views

urlpatterns = [path("", views.add_route, name="add_route")]
