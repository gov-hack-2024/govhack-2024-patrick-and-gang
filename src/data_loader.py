# src/data_loader.py

import pandas as pd
from typing import Optional


def load_data(file_path: str, preprocess: bool = True) -> pd.DataFrame:
    """
    Load and optionally preprocess data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.
        preprocess (bool): Whether to preprocess the data.

    Returns:
        pd.DataFrame: Loaded and preprocessed data.
    """
    # Load the data
    data = pd.read_csv(file_path)

    if preprocess:
        # Example preprocessing: remove missing values and normalize columns
        data = data.dropna()
        for col in data.select_dtypes(include=['float64', 'int64']).columns:
            data[col] = (data[col] - data[col].mean()) / data[col].std()

    return data


def get_feature_target_split(data: pd.DataFrame, target_column: str) -> tuple:
    """
    Split the data into features and target.

    Args:
        data (pd.DataFrame): The data to split.
        target_column (str): The name of the target column.

    Returns:
        tuple: Features (X) and target (y).
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return X, y
