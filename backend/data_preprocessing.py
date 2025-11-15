"""
Data preprocessing module for AQI time-series forecasting.
Handles date parsing, missing values, and creates continuous daily data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AQIDataPreprocessor:
    """Preprocesses AQI data for time-series forecasting."""
    
    def __init__(self, data_path: str):
        """
        Initialize the preprocessor with data path.
        
        Args:
            data_path (str): Path to the CSV file containing AQI data
        """
        self.data_path = data_path
        self.processed_data = None
        self.date_range = None
        
    def load_and_clean_data(self) -> pd.DataFrame:
        """
        Load and clean the raw AQI data.
        
        Returns:
            pd.DataFrame: Cleaned dataframe with proper date index
        """
        # Load the data
        df = pd.read_csv(self.data_path)
        
        # Clean column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        
        # Parse date column
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
        
        # Rename columns to match expected format
        column_mapping = {
            'overall_aqi_value': 'aqi',
            'co': 'co',
            'ozone': 'ozone',
            'pm10': 'pm10',
            'pm25': 'pm25',
            'no2': 'no2'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Select relevant columns
        relevant_columns = ['date', 'aqi', 'co', 'ozone', 'pm10', 'pm25', 'no2']
        df = df[relevant_columns].copy()
        
        # Convert pollutant columns to numeric, handling missing values
        pollutant_columns = ['aqi', 'co', 'ozone', 'pm10', 'pm25', 'no2']
        for col in pollutant_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows where AQI is missing (our target variable)
        df = df.dropna(subset=['aqi'])
        
        # Set date as index
        df = df.set_index('date')
        
        # Sort by date
        df = df.sort_index()
        
        return df
    
    def create_continuous_daily_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create continuous daily data by filling missing dates and interpolating values.
        
        Args:
            df (pd.DataFrame): DataFrame with date index
            
        Returns:
            pd.DataFrame: DataFrame with continuous daily data
        """
        # Create a complete date range
        start_date = df.index.min()
        end_date = df.index.max()
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Reindex to include all dates
        df_complete = df.reindex(date_range)
        
        # Fill missing values using interpolation
        # For pollutants, use forward fill then backward fill
        pollutant_columns = ['co', 'ozone', 'pm10', 'pm25', 'no2']
        for col in pollutant_columns:
            df_complete[col] = df_complete[col].fillna(method='ffill').fillna(method='bfill')
        
        # For AQI, use interpolation
        df_complete['aqi'] = df_complete['aqi'].interpolate(method='linear')
        
        # If there are still missing values at the beginning/end, use mean
        for col in df_complete.columns:
            if df_complete[col].isna().any():
                df_complete[col] = df_complete[col].fillna(df_complete[col].mean())
        
        self.date_range = (start_date, end_date)
        return df_complete
    
    def add_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add temporal features for better forecasting.
        
        Args:
            df (pd.DataFrame): DataFrame with date index
            
        Returns:
            pd.DataFrame: DataFrame with additional temporal features
        """
        df_features = df.copy()
        
        # Extract temporal features
        df_features['year'] = df_features.index.year
        df_features['month'] = df_features.index.month
        df_features['day'] = df_features.index.day
        df_features['day_of_year'] = df_features.index.dayofyear
        df_features['weekday'] = df_features.index.weekday
        df_features['is_weekend'] = (df_features.index.weekday >= 5).astype(int)
        df_features['quarter'] = df_features.index.quarter
        
        # Add seasonal features
        df_features['sin_month'] = np.sin(2 * np.pi * df_features['month'] / 12)
        df_features['cos_month'] = np.cos(2 * np.pi * df_features['month'] / 12)
        df_features['sin_day'] = np.sin(2 * np.pi * df_features['day_of_year'] / 365)
        df_features['cos_day'] = np.cos(2 * np.pi * df_features['day_of_year'] / 365)
        
        # Add lag features for AQI
        df_features['aqi_lag_1'] = df_features['aqi'].shift(1)
        df_features['aqi_lag_7'] = df_features['aqi'].shift(7)
        df_features['aqi_lag_30'] = df_features['aqi'].shift(30)
        
        # Add rolling statistics
        df_features['aqi_rolling_7'] = df_features['aqi'].rolling(window=7).mean()
        df_features['aqi_rolling_30'] = df_features['aqi'].rolling(window=30).mean()
        
        # Add pollutant ratios and interactions
        df_features['pm_ratio'] = df_features['pm25'] / (df_features['pm10'] + 1e-6)
        df_features['pollution_index'] = (df_features['pm25'] + df_features['pm10'] + df_features['no2']) / 3
        
        return df_features
    
    def preprocess(self) -> pd.DataFrame:
        """
        Complete preprocessing pipeline.
        
        Returns:
            pd.DataFrame: Fully preprocessed data ready for modeling
        """
        print("Loading and cleaning data...")
        df = self.load_and_clean_data()
        
        print("Creating continuous daily data...")
        df = self.create_continuous_daily_data(df)
        
        print("Adding temporal features...")
        df = self.add_temporal_features(df)
        
        # Remove rows with NaN values (from lag features)
        df = df.dropna()
        
        self.processed_data = df
        print(f"Preprocessing complete. Data shape: {df.shape}")
        print(f"Date range: {df.index.min()} to {df.index.max()}")
        
        return df
    
    def get_training_data(self, end_date: str = '2024-12-31') -> pd.DataFrame:
        """
        Get training data up to a specific end date.
        
        Args:
            end_date (str): End date for training data (YYYY-MM-DD format)
            
        Returns:
            pd.DataFrame: Training data
        """
        if self.processed_data is None:
            self.preprocess()
        
        end_date = pd.to_datetime(end_date)
        training_data = self.processed_data[self.processed_data.index <= end_date].copy()
        
        print(f"Training data shape: {training_data.shape}")
        print(f"Training date range: {training_data.index.min()} to {training_data.index.max()}")
        
        return training_data
    
    def get_exogenous_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract exogenous variables for SARIMAX model.
        
        Args:
            df (pd.DataFrame): Preprocessed dataframe
            
        Returns:
            pd.DataFrame: Exogenous variables
        """
        exogenous_cols = [
            'co', 'ozone', 'pm10', 'pm25', 'no2',
            'month', 'day_of_year', 'is_weekend',
            'sin_month', 'cos_month', 'sin_day', 'cos_day',
            'pm_ratio', 'pollution_index'
        ]
        
        return df[exogenous_cols]
    
    def save_processed_data(self, output_path: str = 'processed_aqi_data.csv'):
        """
        Save processed data to CSV file.
        
        Args:
            output_path (str): Output file path
        """
        if self.processed_data is not None:
            self.processed_data.to_csv(output_path)
            print(f"Processed data saved to {output_path}")
        else:
            print("No processed data available. Run preprocess() first.")


def main():
    """Test the preprocessing pipeline."""
    preprocessor = AQIDataPreprocessor('aqidaily_fiveyears.csv')
    processed_data = preprocessor.preprocess()
    
    # Save processed data
    preprocessor.save_processed_data()
    
    # Show basic statistics
    print("\nBasic Statistics:")
    print(processed_data.describe())
    
    # Show data info
    print("\nData Info:")
    print(processed_data.info())


if __name__ == "__main__":
    main()
