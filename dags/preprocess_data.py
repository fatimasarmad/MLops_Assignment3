
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

def preprocess_data(input_file='raw_data.csv', output_file='processed_data.csv'):
    """
    Preprocess weather data by handling missing values and normalizing numerical fields.
    
    Args:
        input_file (str): Path to the raw data CSV file
        output_file (str): Path to save the processed data
    """
    print(f"Starting preprocessing of {input_file}...")
    
    # Read the data
    try:
        df = pd.read_csv(input_file)
        print(f"Successfully loaded data with {df.shape[0]} rows and {df.shape[1]} columns")
    except Exception as e:
        print(f"Error loading data: {e}")
        return False
    
    # Display data info before preprocessing
    print("\nData before preprocessing:")
    print(df.head())
    print(f"\nMissing values before preprocessing:\n{df.isnull().sum()}")
    
    # Handle missing values
    numerical_columns = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)']
    
    # Fill missing values in numerical columns with column means
    for col in numerical_columns:
        if df[col].isnull().any():
            mean_value = df[col].mean()
            df[col] = df[col].fillna(mean_value)
            print(f"Filled missing values in {col} with mean: {mean_value:.2f}")
    
    # Fill missing weather conditions with "unknown"
    if df['Weather Condition'].isnull().any():
        df['Weather Condition'] = df['Weather Condition'].fillna('unknown')
        print("Filled missing Weather Condition values with 'unknown'")
    
    # Normalize numerical fields using Min-Max scaling
    scaler = MinMaxScaler()
    
    # Create new normalized columns while preserving original data
    for col in numerical_columns:
        norm_col_name = f"{col.split(' ')[0]}_Normalized"
        df[norm_col_name] = scaler.fit_transform(df[[col]])
        print(f"Created normalized column: {norm_col_name}")
    
    # Add a derived feature: temperature difference from daily mean
    df['Date'] = pd.to_datetime(df['Date and Time']).dt.date
    daily_mean_temp = df.groupby('Date')['Temperature (°C)'].transform('mean')
    df['Temp_Diff_From_Daily_Mean'] = df['Temperature (°C)'] - daily_mean_temp
    print("Added feature: Temperature difference from daily mean")
    
    # Display data info after preprocessing
    print("\nData after preprocessing:")
    print(df.head())
    print(f"\nMissing values after preprocessing:\n{df.isnull().sum()}")
    
    # Save preprocessed data
    try:
        df.to_csv(output_file, index=False)
        print(f"\nSuccessfully saved preprocessed data to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving processed data: {e}")
        return False

if __name__ == "__main__":
    preprocess_data()