from django.urls import path
from . import views

app_name = "crimecue"  # 👈 this makes "crime:home" work

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.home, name="home"),
    path("map/", views.crime_map, name="crime_map"),
]
