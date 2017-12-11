from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from PIL import Image
from .forms import PhotoUploadForm
from .models import Photo, generate_random_filename
from .settings import SHOW_PER_PAGE, THUMNAIL_DIMENSION
import os

# Create your views here.
def home(request):
    """Displays all uploaded images"""
    # Sorted by most recently uploaded.
    photos = Photo.objects.all().order_by('-uploaded_at')
    paginator = Paginator(photos, SHOW_PER_PAGE)
    page = request.GET.get('page')
    paginated_photos = paginator.get_page(page)

    return render(request, 'photos/home.html', {'paginated_photos': paginated_photos})

def detail(request, photo_id):
    """View a single photo"""
    photo = get_object_or_404(Photo, pk=photo_id)

    return render(request, 'photos/detail.html', {'photo': photo})
    
@login_required
def upload(request):
    """Handle photo uploads"""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            saved_photo = form.save()

            uploaded_file_name = saved_photo.uploaded_file.name
            
            # Generate thumbnail
            image = Image.open(form.cleaned_data['uploaded_file'])

            # Resize the smaller side to match the desired dimensions.
            w, h = image.size
            import math
            scale_by = (THUMNAIL_DIMENSION / min(w, h))
            scaled_image = image.resize((math.ceil(w * scale_by), math.ceil(h * scale_by)), Image.ANTIALIAS)
            
            #crop at the center
            resized_width, resized_height = scaled_image.size
            left = (resized_width - THUMNAIL_DIMENSION) / 2 + 1
            upper  = (resized_height - THUMNAIL_DIMENSION) / 2 + 1
            right = left + THUMNAIL_DIMENSION
            lower = upper + THUMNAIL_DIMENSION

            cropped_image = scaled_image.crop((left, upper, right, lower))

            cropped_image_file_name = generate_random_filename(None, 'thumb.' + uploaded_file_name.split('.')[-1])
            
            cropped_image.save(os.path.join(settings.MEDIA_ROOT, cropped_image_file_name))
            saved_photo.thumb_path = cropped_image_file_name
            saved_photo.save()
            
            messages.info(request, 'Your photo has been uploaded.')
            return HttpResponseRedirect(reverse('photos:home'))
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form': form})

