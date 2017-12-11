"""Photos specific default settings. These can be overridden by the project level settings"""

from django.conf import settings

"""The directory where photos are saved"""
SHOW_PER_PAGE = getattr(settings, 'PHOTOS_SHOW_PER_PAGE', 24)

"""Thumbnail dimensions in pixels (THUMNAIL_DIMENSION x THUMNAIL_DIMENSION)"""
THUMNAIL_DIMENSION=360
