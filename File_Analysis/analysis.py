#Analysis.py
import base64
import io
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from fancyimpute import IterativeImputer


def FileExist(file_path):
    if os.path.exists(file_path):
        return True
    return False


def isImputable(df, column):
    try:
        int(df[column][0])
        return True
    except Exception as e:
        return False

def num_column(df):
    Total_columns = df.columns.tolist()
    return Total_columns


def scaleto(df,x,y,k):
    '''
    df -> dataframe
    x -> obtained marks
    y -> full marks
    '''
    #function to scale rows named x and y in range of 0 to k
    for index,rows in df.iterrows():
        df.at[index,x] = rows[x]*k/rows[y]
        df.at[index,y] = rows[y]*k/rows[y]
    
    return df

def metaData(df,x):

    total_rows = len(df)
    print(total_rows)
    mean = df[x].mean()
    print(mean)
    total_nan_values = df[x].isna().sum()
    print(total_nan_values)
    nan_percentage = (total_nan_values / total_rows) * 100
    print("metadata function 3")
    
    #data_type = type(df[x][1])
    print("metadata function 4")
    
    median = df[x].median()

    print("metadata function 5")
    SD = df[x].std()


    kurt = df[x].kurt()
    skew = df[x].skew()

    # Create an interactive histogram using Plotly Express
    fig = px.histogram(df, x=x, title=f'Histogram of {x}')
    histogram_data = fig.to_html(full_html=False, default_height=500, default_width=700)

    analyzed_data = {
        'column_name': x,
        'total_rows': total_rows,
        'total_nan_values': total_nan_values,
        'nan_percentage': nan_percentage,
        'mean': mean,
        'median': median,
        'SD' : SD,
        'histogram_data': histogram_data,
        'skewness': skew,
        'kurtesis' : kurt,
        # 'histogram_data': analysis.returnhist(df, selected_column),
        
    }
    print(analyzed_data)
    return analyzed_data


def dropOutliers(df,y):
    #drop if full marks is nan
    df = df.dropna(subset=[y]);
    return df


def nan_percent(df,x):
    return (df[x].isna().sum()/df.shape[0])*100
