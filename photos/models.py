from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image
from .settings import THUMNAIL_DIMENSION
import math
import random
import string 
import os

from django.dispatch import receiver

def generate_random_filename(instance, filename):
    """Randomize the filename so that prior uploads aren't inadverdently overwritten"""
    return 'photos/%s-%s' % (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50)), filename)


class Photo(models.Model):
    """The photo model stores the path to the image and thumbnail files relative to MEDIA_ROOT"""
    uploaded_file = models.ImageField(upload_to=generate_random_filename)    
    thumb_path = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Photo)
def _generate_thumbnail(sender, instance, created, *args, **kwargs):
    """Generate and save the corresponding thumbnail for an image then update the image with its path"""
    # Only generate the thumbnail if a Photo is being created.
    if created:
        # Open the uploaded photo.
        image = Image.open(os.path.join(settings.MEDIA_ROOT, instance.uploaded_file.name))

        # Resize the smaller side to match the desired dimensions.
        # This minimizes the cropped area.
        w, h = image.size
        scale_by = (THUMNAIL_DIMENSION / min(w, h))
        scaled_image = image.resize((math.ceil(w * scale_by), math.ceil(h * scale_by)), Image.ANTIALIAS)

        # Crop the scaled photo at the center
        resized_width, resized_height = scaled_image.size
        left = (resized_width - THUMNAIL_DIMENSION) / 2 + 1
        upper  = (resized_height - THUMNAIL_DIMENSION) / 2 + 1
        right = left + THUMNAIL_DIMENSION
        lower = upper + THUMNAIL_DIMENSION
        cropped_image = scaled_image.crop((left, upper, right, lower))

        # Save the cropped image as the thumbnail
        cropped_image_path = generate_random_filename(None, 'thumb.' + instance.uploaded_file.name.split('.')[-1])
        cropped_image.save(os.path.join(settings.MEDIA_ROOT, cropped_image_path))
        # Update the saved Photo with the path to the cropped image
        instance.thumb_path = cropped_image_path
        instance.save()
