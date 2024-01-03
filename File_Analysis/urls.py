# File_Handling/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Define URL pattern for the file upload view
    path('analyze_column', views.analyze_column_render, name='analyze_column'),
    path('impute_column', views.impute_column_render, name='impute_column'),
    path('compare_algo/', views.compare_algorithms_impute, name='compare_algorithms_impute')
]
