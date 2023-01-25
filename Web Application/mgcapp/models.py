from django.db import models


# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    prediction_text = models.TextField(verbose_name='Prediction')
    timeSeries = models.ImageField(upload_to='pictures/')
    prediction = models.CharField(max_length=255, blank=True)
    recommender = models.CharField(max_length=255, blank=True)
        


