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

imputation_functions = {
        'Mean',
        'Median',
        'Iterative_Imputer',
        'Linear_Interpolate',
        # 'Iterative_SVD',
        # 'Matrix_Factorization',
        # 'Soft_Imputer'  
        }

def analyze_column(df, column):
    if analysis.isImputable(df,column):
        analyzed_data = analysis.metaData(df, column)
    return analyzed_data

def analyze_column_render(request):
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

        try:
            analyzed_data = analyze_column(df, selected_column)
            analyzed_data.update({'file_path':file_path_initial, 'imputation_functions': imputation_functions}) # update the dictionary
                
            return render(request, 'analyzed_column.html', analyzed_data)
        
        except Exception as e:
            return render(request, 'error.html', {"error": str(e)})
    else : 
        file_path = os.path.join(settings.MEDIA_ROOT, 'FINAL_FILES', file_path_initial)
        df = pd.read_csv(file_path)

        try:
            analyzed_data = analyze_column(df, selected_column)
            analyzed_data.update({'file_path':file_path_initial, 'imputation_functions': imputation_functions}) # update the dictionary
                
            return render(request, 'analyzed_column.html', analyzed_data)
        
        except Exception as e:
            return render(request, 'error.html', {"error": str(e)})
    

def Impute_column(file, column_name, imputation_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'INITIAL_FILES', file)

    if analysis.FileExist(file_path) == False:
        return render(request, 'error.html', {'error': 'file doesnot exists'})

    df = pd.read_csv(file_path)
    df_copy = df.copy()

    imputation_functions = {
        'Mean': algorithms.impute_mean,
        'Median': algorithms.impute_median,
        'Iterative_Imputer' : algorithms.iterative_imputer,
        'Linear_Interpolate' : algorithms.linear_interpolate_column,
        # 'Iterative_SVD': algorithms.iterative_svd_fill,
        # 'Matrix_Factorization': algorithms.matrix_factorization_fill,
        # 'Soft_Imputer': algorithms.soft_fill,
    }
    print("Imputation Name")
    print(imputation_name)
    if imputation_name not in imputation_functions.keys():
        return {'error':'Imputation Algorithm not found'}
    
    if column_name not in analysis.num_column(df_copy):
        return render(request, 'error.html', {'error': 'invalid column'})

    # Call the corresponding imputation function based on the received name
    # Perform necessary operations to read and process the column data from the file
    # df is the DataFrame and column_name is the selected column
    try:
        # df = analysis.scaleto(df)
        selected_function = imputation_functions[imputation_name]

        df_result = selected_function(df_copy, column_name)
        
        return df_result
    except Exception as e:
        return render(request, 'error.html', {'error': f'Error performing imputation: {str(e)}'}, status=500)



def impute_column_render(request):
    if request.method == 'POST':
        file = request.POST.get('file_path')
        column_name = request.POST.get('column_name')
        imputation_name = request.POST.get('selected_algorithm')  # Capture selected imputation algorithm

    download_file_path = os.path.join(settings.MEDIA_ROOT, 'FINAL_FILES', file)
    
    # try:
    imputed_df = Impute_column(file, column_name, imputation_name)

    imputed_df.to_csv(download_file_path)
    original_df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'INITIAL_FILES', file))

    analyzed_data = analysis.metaData(imputed_df, column_name)
    original_data = analysis.metaData(original_df, column_name)

    analyzed_data.update({'file_path':file,'data': analyzed_data, 'original_data':original_data, 'imputation_algorithm': imputation_name})
    
    return render(request, 'imputed.html', analyzed_data)

    # except Exception as e:
    #     return render(request, 'errorr.html', {'error': f'Error performing imputation render: {str(e)}'})


def compare_algorithms_impute(request):
    '''
    A function to imputed a single dataframe with multiple algorithms
    '''
    if request.method == 'POST':
        file = request.POST.get('file_path')
        column_name = request.POST.get('column_name')
        algorithms = request.POST.getlist('selected_algorithms')  # Capture selected imputation algorithm

    download_file_path = os.path.join(settings.MEDIA_ROOT, 'FINAL_FILES', file)
    results = []
    i = 0
    
    print(algorithms)
    for algo in algorithms:
        print(algo)
        imputed_df = Impute_column(file, column_name, str(algo))
        print(imputed_df.head())
        imputed_df.to_csv(download_file_path)
        
        result = analysis.metaData(imputed_df, column_name)
        results.append({'algorithm': algo, 'data': result})
        i = i+1
    
        # except Exception as e:
        #     return render(request, 'error.html', {'error': f'Error performing comparative imputation: {str(e)}'}, status=500)
    # print(results)
    context = {
            'file': file,
            'column_name': column_name,
            'results': results,
        }

    return render(request, 'compare.html', context)
