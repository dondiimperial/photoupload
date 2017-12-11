from django.http import HttpResponse #Will probably delete this later
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import Photo

# Create your views here.
def home(request):
    """Displays all uploaded images"""
    return HttpResponse('photos home')

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            thumb_name = 'thumb_%s' % uploaded_file.name
            model = Photo(image_path=uploaded_file.name, thumbnail_path=thumb_name)
            model.save()
            
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('photos:home'))
    else:
        form = UploadFileForm()
    return render(request, 'photos/upload.html', {'form': form})

