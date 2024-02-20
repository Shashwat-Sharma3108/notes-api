
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"api/", include("users.urls")),
    path(r"notes/", include("notes.urls")),
]