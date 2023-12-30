import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fancyimpute import IterativeImputer

def scaleto(df,x,y,k):
    #function to scale rows named x and y in range of 0 to k
    for index,rows in df.iterrows():
        df.at[index,x] = rows[x]*k/rows[y]
        df.at[index,y] = rows[y]*k/rows[y]


def countnan(df,x):
    #fuction to count total number of nan in the dataframe
    return df[x].isna().sum()


def returnhist(df,x):
    #function to plot the histogram of column x in dataframe df
    plt.hist(df[column], bins='auto', alpha=0.7, rwidth=0.85)
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()

def dropOutliers(df,x):
    df = df.dropna(subset=[x]);
    return assignment_data.isna().sum()

def calculate_mean_std(df, column):
    # Calculate mean
    mean = df[column].mean()

    # Calculate standard deviation
    std_dev = df[column].std()

    # Print the results
    return mean, std_dev

def nan_percent(df,x):
    return (df[x].isna().sum()/df.shape[0])*100

def interpolate_column(data, column_name, method='linear'):
    """
    Interpolate missing values in a specified column of a DataFrame.

    Parameters:
        data (DataFrame): The input DataFrame.
        column_name (str): The name of the column to interpolate.
        method (str, optional): The interpolation method to use. Default is 'linear'.
            Other options include 'polynomial', 'spline', etc. See Pandas documentation for more options.

    Returns:
        DataFrame: A copy of the input DataFrame with missing values in the specified column interpolated.
    """
    if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Create a copy of the DataFrame to avoid modifying the original data
    interpolated_data = data.copy()

    # Use the interpolate function to fill missing values in the specified column
    interpolated_data[column_name] = interpolated_data[column_name].interpolate(method=method)

    interpolated_data.fillna(interpolated_data.obtained_marks.mean(),inplace = True)

    return interpolated_data

def replace_column_with_array(dataframe, column_name, new_array):
    """
    Replace the values of a specific column in a DataFrame with a NumPy array.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame you want to modify.
    column_name (str): The name of the column to be replaced.
    new_array (np.ndarray): The NumPy array containing the new values.

    Returns:
    pd.DataFrame: The modified DataFrame.
    """

    # Make sure the length of the array matches the number of rows in the DataFrame
    if len(new_array) != len(dataframe):
        raise ValueError("Length of new_array must match the number of rows in the DataFrame")

    # Create a copy of the DataFrame to avoid modifying the original
    updated_dataframe = dataframe.copy()

    # Replace the values in the specified column with the values from the NumPy array
    updated_dataframe[column_name] = new_array

    return updated_dataframe

def iterative_imputer(df,x):
    mice_imputer = IterativeImputer() 
    iterative_row = df[[x]]
    iterative_row = mice_imputer.fit_transform(iterative_row)
    df = replace_column_with_array(df,x,iterative_row)
    return df