"""photoupload URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    url('', include('photos.urls', namespace='photos')),
    # Override the login url from the django-registration-redux. 
    # Otherwise there is no way to set redirect_authenticated_user to true for
     url(r'^accounts/login/$', auth_views.login, {'redirect_authenticated_user': True}, name='auth_login'),
    # For the same rationale as above we override the logout view to customize the next page.
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': 'photos:home'}, name='logout'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
