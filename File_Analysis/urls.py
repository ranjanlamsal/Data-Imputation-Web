# File_Handling/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Define URL pattern for the file upload view
    path('analyze_column', views.analyze_column, name='analyze_column'),
    path('impute_column', views.impute_column, name='impute_column'),
]
