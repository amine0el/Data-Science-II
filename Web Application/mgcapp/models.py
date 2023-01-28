
# GenRec - The Smash Group
    # Music Genre Recommender and Classifier
    # Project during Data Science 2
    # WiSe 2022/2023
    # TU Darmstadt

# File models.py
    # Description: 
        # Definitions for Django Database Columns used to store the songs and additional data of it


from django.db import models


# Creation of new Class "Document" to store songs (document) and additional data (name, upload time, prediction etc)
class Document(models.Model):
    name = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    prediction_text = models.TextField(verbose_name='Prediction')
    timeSeries = models.ImageField(upload_to='pictures/')
    prediction = models.CharField(max_length=255, blank=True)
    recommender = models.CharField(max_length=255, blank=True)
    extraction = models.FileField(upload_to='extractions/')


