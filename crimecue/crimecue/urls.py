from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("crime/", include("crime_data.urls")),
    path("", lambda request: redirect("crimecue:home")),  # 👈 root redirect
]
