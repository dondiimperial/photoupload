from django.db import models

# Create your models here.
class Photo(models.Model):    
    image_path = models.CharField(max_length=255)    
    thumbnail_path = models.CharField(max_length=255)
