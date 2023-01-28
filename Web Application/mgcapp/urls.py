from django.urls import path
from mgcapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload", views.simple_upload, name="upload"),
    path("prediction", views.extraction_view, name="prediction"),
    path("recommender", views.recommender_view, name="recommender"),
    path("discommender", views.recommender_view_worst, name="recommender-worst"),
    
]