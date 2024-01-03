# File_Handling/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Define URL pattern for the file upload view
    path('upload/', views.upload_file, name='upload_file'),
    # Add more URL patterns for other views/functions if needed
]
