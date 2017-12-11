from django.db import models
from django.conf import settings

# Create your models here.
class Photo(models.Model):
    uploaded_file = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
