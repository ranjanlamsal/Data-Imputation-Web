# File_Analysis/views.py
import plotly.express as px
from django.shortcuts import render
from django.http import JsonResponse
from requests import request
from . import algorithms, analysis  # Import your imputation functions
import os
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from Data_Imputation_Web import settings

imputation_functions = [
        'mean',
        'median',
        'iterative_imputer',
        'linear_interpolate_column'
    ]


def analyze_column(request):
    if request.method == 'POST':
        file_path_initial = request.POST.get('file_path')
        selected_column = request.POST.get('selected_column')
        print(selected_column)
        i = int(request.POST.get('i', 0))
        print(i)

    # i is sent along the request. During initial call of analyze_column function , i.e before imputation
    # file path must be in Initial Directory. Else file padh must be in FInal Directory

    if i == 1:
        file_path = os.path.join(settings.MEDIA_ROOT, 'INITIAL_FILES', file_path_initial)

        df = pd.read_csv(file_path)

        if analysis.isImputable(df,selected_column):
            total_rows = len(df)
            total_nan_values = df[selected_column].isnull().sum()
            nan_percentage = (total_nan_values / total_rows) * 100
            data_type = type(df[selected_column][1])

            mean = df[selected_column].mean()
            median = df[selected_column].median()
        

            SD = df[selected_column].std()

            # Create an interactive histogram using Plotly Express
            fig = px.histogram(df, x=selected_column, title=f'Histogram of {selected_column}')
            histogram_data = fig.to_html(full_html=False, default_height=500, default_width=700)

            analyzed_data = {
                'file_path' : file_path_initial,
                'column_name': selected_column,
                'total_rows': total_rows,
                'total_nan_values': total_nan_values,
                'nan_percentage': nan_percentage,
                'mean': mean,
                'median': median,
                'SD' : SD,
                'histogram_data': histogram_data,
                'imputation_functions': imputation_functions
                # 'histogram_data': analysis.returnhist(df, selected_column),
                
            }
            
            return render(request, 'analyzed_column.html', analyzed_data)
        
        else:
            return render(request, 'error.html', {'error': 'Column Type Error'})
    else : 
        file_path = os.path.join(settings.MEDIA_ROOT, 'FINAL_FILES', file_path_initial)
        df = pd.read_csv(file_path)

        if analysis.isImputable(df,selected_column):
            total_rows = len(df)
            total_nan_values = df[selected_column].isnull().sum()
            nan_percentage = (total_nan_values / total_rows) * 100
            data_type = type(df[selected_column][1])

            mean = df[selected_column].mean()
            median = df[selected_column].median()
        

            SD = df[selected_column].std()

            # Create an interactive histogram using Plotly Express
            fig = px.histogram(df, x=selected_column, title=f'Histogram of {selected_column}')
            histogram_data = fig.to_html(full_html=False, default_height=500, default_width=700)

            analyzed_data = {
                'file_path' : file_path_initial,
                'selected_column': selected_column,
                'total_rows': total_rows,
                'total_nan_values': total_nan_values,
                'nan_percentage': nan_percentage,
                'mean': mean,
                'median': median,
                'SD' : SD,
                'histogram_data': histogram_data,
                'imputation_functions': imputation_functions
                # 'histogram_data': analysis.returnhist(df, selected_column),
                
            }
            
            return render(request, 'post_analysis.html', analyzed_data)
        
        else:
            return render(request, 'error.html', {'error': 'Column Type Error'})
    

def impute_column(request):
    if request.method == 'POST':
        file = request.POST.get('file_path')
        column_name = request.POST.get('column_name')
        imputation_name = request.POST.get('selected_algorithm')  # Capture selected imputation algorithm

    file_path = os.path.join(settings.MEDIA_ROOT, 'INITIAL_FILES', file)
    download_file_path = os.path.join(settings.MEDIA_ROOT, 'FINAL_FILES', file)

    imputation_functions = {
        'mean': algorithms.impute_mean,
        'median': algorithms.impute_median,
        'iterative_imputer' : algorithms.iterative_imputer,
        'linear_interpolate_column' : algorithms.linear_interpolate_column
    }
    if analysis.FileExist(file_path) == False:
        return render(request, 'error.html', {'error': 'file doesnot exists'})

    df = pd.read_csv(file_path)

    if imputation_name not in imputation_functions.keys():
        return render(request, 'error.html', {'error': 'select valid imputation algorithm'})
    
    if column_name not in analysis.num_column(df):
        return render(request, 'error.html', {'error': 'invalid column'})

    # Call the corresponding imputation function based on the received name
    # Perform necessary operations to read and process the column data from the file
    # df is the DataFrame and column_name is the selected column
    try:
        # df = analysis.scaleto(df)
        selected_function = imputation_functions[imputation_name]

        df = selected_function(df, column_name)

        df.to_csv(download_file_path)
        
        return render(request, 'imputed.html',{'file_path': file,'selected_column':column_name})
    except Exception as e:
        return render(request, 'error.html', {'error': f'Error performing imputation: {str(e)}'}, status=500)
