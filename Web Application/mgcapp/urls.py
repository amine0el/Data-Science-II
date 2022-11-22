from django.urls import path
from mgcapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("/upload", views.simple_upload, name="upload"),
]