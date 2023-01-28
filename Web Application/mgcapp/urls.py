
# GenRec - The Smash Group
    # Music Genre Recommender and Classifier
    # Project during Data Science 2
    # WiSe 2022/2023
    # TU Darmstadt

# File urls.py
    # Description: 
        # Django-File were the urls are coded into functions in the file views.py, needed to define the pages/functions of the website

from django.urls import path
from mgcapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload", views.simple_upload, name="upload"),
    path("prediction", views.extraction_view, name="prediction"),
    path("recommender", views.recommender_view, name="recommender"),
    path("discommender", views.recommender_view_worst, name="recommender-worst"),
    
]