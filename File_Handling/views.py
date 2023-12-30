# File_Handling.views.py
import pandas as pd
from File_Analysis.analysis import num_column
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import random
import string

from requests import request

def index(request):
    return render(request,'index.html')

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))



def upload_file(request):
    if request.method == 'POST' and 'csv_file' in request.FILES:
        uploaded_file = request.FILES['csv_file']

    # uploaded_file = open(file, 'rb')

    # Validate file size (up to 20MB)
    max_size = 20 * 1024 * 1024  # 20MB in bytes
    if uploaded_file.size > max_size:
        return render(request, 'error.html', {'error': 'file size must not exceed 20 MB'})  # Render an error page for exceeded file size

    fs = FileSystemStorage()

    # Generate a unique filename
    unique_filename = generate_random_string(10) + '_' + uploaded_file.name

    # Define the path to the media directory and create 'INITIAL_FILES' folder if it doesn't exist
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'INITIAL_FILES'), exist_ok=True)
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'FINAL_FILES'), exist_ok=True)

    # Save the uploaded file in the 'INITIAL_FILES' folder and 'FINAL_FILES' within the media directory
    saved_file = fs.save(os.path.join(settings.MEDIA_ROOT, 'INITIAL_FILES', unique_filename), uploaded_file)
    saved_file = fs.save(os.path.join(settings.MEDIA_ROOT, 'FINAL_FILES', unique_filename), uploaded_file)

    df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'INITIAL_FILES', unique_filename))
    # Call the function to analyze the columns of the uploaded file
    column_list = num_column(df) 

    return render(request, 'upload_success.html', {
        'file_path' : unique_filename,
        'column_list': column_list
    })

    # except Exception as e:
    #     return render(request, 'error.html', {'error':'File not found'})

# def request_upload(filepath):
#     try:
#         file = filepath
#         uploaded_file = open(file, 'rb')
#         upload_file(uploaded_file)

#     except Exception as e:
#         return render(request, 'error.html', {'error':'File not found'})

