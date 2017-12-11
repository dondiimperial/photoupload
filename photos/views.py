from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import PhotoUploadForm
from .models import Photo
from .settings import SHOW_PER_PAGE

# Create your views here.
def home(request):
    """Displays all uploaded images"""
    # Sorted by most recently uploaded.
    photos = Photo.objects.all().order_by('-uploaded_at')
    paginator = Paginator(photos, SHOW_PER_PAGE)
    page = request.GET.get('page')
    paginated_photos = paginator.get_page(page)

    
    return render(request, 'photos/home.html', {'paginated_photos': paginated_photos})

@login_required
def upload(request):
    """Handle photo uploads"""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your photo has been uploaded.')
            return HttpResponseRedirect(reverse('photos:home'))
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form': form})

