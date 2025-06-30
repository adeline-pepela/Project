"""
URL configuration for model_deployment project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("model_selector.urls")),
]