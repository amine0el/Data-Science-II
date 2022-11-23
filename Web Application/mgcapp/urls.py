from django.urls import path
from mgcapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("/upload", views.simple_upload, name="upload"),
    path("/modelUpload", views.model_form_upload, name='model_form_upload')
]