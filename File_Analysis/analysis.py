import base64
import io
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

def countnan(df,x):
    #fuction to count total number of nan in the dataframe
    return df[x].isna().sum()


def returnhist(df,column):
    # Prepare histogram data
    # Generate histogram plot of the selected column
    plt.figure(figsize=(6, 4))
    plt.hist(df[column], bins='auto', alpha=0.7, rwidth=0.85)  # Adjust the number of bins as needed
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    
    # Save the histogram plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert the plot to base64 encoding
    histogram_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Close the plot to free memory
    plt.close()

    return histogram_data

def dropOutliers(df,y):
    #drop if full marks is nan
    df = df.dropna(subset=[y]);
    return df


def nan_percent(df,x):
    return (df[x].isna().sum()/df.shape[0])*100
