from django.db import models

import random
import string 
# Create your models here.

def generate_random_filename(instance, filename):
    return 'photos/%s-%s' % (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50)), filename)


class Photo(models.Model):
    uploaded_file = models.ImageField(upload_to=generate_random_filename)    
    thumb_path = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
