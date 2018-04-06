import ipaddress
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import PhotoUploadForm
from .models import Photo
from .settings import SHOW_PER_PAGE


def get_ip(request):
    try:
        x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward:
            ip = x_forward.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip = ""
    return ip

def home(request):
    """Displays all uploaded images"""
    # Sorted by most recently uploaded.
    client_ip = get_ip(request)
    if ipaddress.ip_address(client_ip).__class__ is ipaddress.IPv6Address:
        msg = 'You are great!'
        ip_valid = True
    else:
        msg = 'Oh, sorry...'
        ip_valid = False
    photos = Photo.objects.all().order_by('-uploaded_at')
    paginator = Paginator(photos, SHOW_PER_PAGE)
    page = request.GET.get('page')
    paginated_photos = paginator.get_page(page)

    return render(request, 'photos/home.html', {'paginated_photos': paginated_photos, 'msg': msg, 'ip_valid': ip_valid})

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
            messages.info(request, 'Your photo has been uploaded.')
            return HttpResponseRedirect(reverse('photos:home'))
    else:
        form = PhotoUploadForm()
    return render(request, 'photos/upload.html', {'form': form})

