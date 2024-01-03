import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fancyimpute import IterativeImputer, IterativeSVD, MatrixFactorization, SoftImpute


def linear_interpolate_column(DataFrame, column_name):
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
    
    # Create a copy of the DataFrame to avoid modifying the original data
    interpolated_data = DataFrame.copy()

    # Use the interpolate function to fill missing values in the specified column
    interpolated_data[column_name] = interpolated_data[column_name].interpolate(method='linear')

    interpolated_data.fillna(interpolated_data[column_name].mean(),inplace = True)

    return interpolated_data


def polynomial_interpolate_column(request):
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
    DataFrame = request.POST.get("DataFrame")
    column_name = request.POST.get("column_name")
    selected_algorithm = request.POST.get("selected_algorithm")
    
    # Create a copy of the DataFrame to avoid modifying the original data
    interpolated_data = DataFrame.copy()

    # Use the interpolate function to fill missing values in the specified column
    interpolated_data[column_name] = interpolated_data[column_name].interpolate(method='polynomial')

    #fillna in first and last data as interpolation doesnot impite those if needed
    interpolated_data.fillna(interpolated_data[column_name].mean(),inplace = True)

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

def impute_mean(df, x):
    df[x] = df[x].fillna(df[x].mean())
    return df

def impute_median(df, x):
    df[x] = df[x].fillna(df[x].median())
    return df


def iterative_svd_fill(df,x, max_iters=10):
    # Convert the DataFrame to a NumPy array
    array_data = df.values

    # Use IterativeSVD to fill NaN values
    imputer = IterativeSVD(max_iters=max_iters)
    filled_data = imputer.fit_transform(array_data)

    # Convert the filled data back to a DataFrame
    filled_df = pd.DataFrame(filled_data, columns=[x])

    return filled_df


# Function to perform matrix factorization using fancyimpute
def matrix_factorization_fill(df, column_name,rank=3, max_iters=100):
    
     # Creating a copy of the DataFrame to avoid modifying the original one
    df_copy = df.copy()
    
    # Extracting the column to be imputed
    column_data = df_copy[column_name].values
    
    # Creating a boolean mask of missing values in the column
    missing_mask = np.isnan(column_data)
    
    # Using matrix factorization to fill missing values
    imputer = MatrixFactorization(rank=rank, max_iters=max_iters)
    
    # Filling the missing values in the column
    filled_column_data = imputer.fit_transform(column_data.reshape(-1, 1)).ravel()
    
    # Assigning the filled values back to the DataFrame
    df_copy.loc[missing_mask, column_name] = filled_column_data[missing_mask]
    
    return df_copy

def soft_fill(df,x):
    # Convert the DataFrame to a NumPy array
    array_data = df.values

    # Use SoftImpute to fill NaN values
    imputer = SoftImpute()
    filled_data = imputer.fit_transform(array_data)

    # Convert the filled data back to a DataFrame
    filled_df = pd.DataFrame(filled_data, columns=df.columns)

    return filled_df