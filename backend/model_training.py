"""
Model training script for AQI time-series forecasting.
Handles data preprocessing, model training, and saving.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

from data_preprocessing import AQIDataPreprocessor
from sarimax_forecaster import AQISARIMAXForecaster, generate_future_exogenous_data

def train_aqi_forecasting_model():
    """
    Complete training pipeline for AQI forecasting model.
    """
    print("=" * 60)
    print("AQI TIME-SERIES FORECASTING MODEL TRAINING")
    print("=" * 60)
    
    # Step 1: Data Preprocessing
    print("\n1. DATA PREPROCESSING")
    print("-" * 30)
    
    preprocessor = AQIDataPreprocessor('aqidaily_fiveyears.csv')
    processed_data = preprocessor.preprocess()
    
    # Save processed data for reference
    preprocessor.save_processed_data('processed_aqi_data.csv')
    
    # Step 2: Prepare Training Data
    print("\n2. PREPARING TRAINING DATA")
    print("-" * 30)
    
    # Use data up to 2024-12-31 for training
    training_data = preprocessor.get_training_data(end_date='2024-12-31')
    
    # Prepare time series and exogenous data
    ts_data = training_data['aqi']
    exog_data = preprocessor.get_exogenous_variables(training_data)
    
    print(f"Training data shape: {training_data.shape}")
    print(f"Time series length: {len(ts_data)}")
    print(f"Exogenous variables shape: {exog_data.shape}")
    
    # Step 3: Model Training
    print("\n3. MODEL TRAINING")
    print("-" * 30)
    
    # Initialize SARIMAX forecaster
    forecaster = AQISARIMAXForecaster()
    
    # Fit the model with automatic parameter selection
    forecaster.fit(ts_data, exog_data, auto_parameters=True)
    
    # Step 4: Model Validation
    print("\n4. MODEL VALIDATION")
    print("-" * 30)
    
    # Generate in-sample predictions for validation
    in_sample_pred = forecaster.fitted_model.fittedvalues
    
    # Calculate validation metrics
    mae = np.mean(np.abs(ts_data - in_sample_pred))
    mse = np.mean((ts_data - in_sample_pred) ** 2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((ts_data - in_sample_pred) / ts_data)) * 100
    
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Square Error (RMSE): {rmse:.2f}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    
    # Step 5: Test Future Predictions
    print("\n5. TESTING FUTURE PREDICTIONS")
    print("-" * 30)
    
    # Test predictions for sample future dates
    test_dates = [
        datetime(2025, 1, 15),
        datetime(2025, 4, 9),
        datetime(2025, 7, 20),
        datetime(2025, 10, 31)
    ]
    
    print("Sample future predictions:")
    for test_date in test_dates:
        try:
            exog_future = generate_future_exogenous_data(test_date, training_data)
            prediction = forecaster.predict_single_date(test_date, exog_future)
            print(f"  {test_date.strftime('%Y-%m-%d')}: AQI = {prediction:.1f}")
        except Exception as e:
            print(f"  {test_date.strftime('%Y-%m-%d')}: Error - {str(e)}")
    
    # Step 6: Save Model and Metadata
    print("\n6. SAVING MODEL")
    print("-" * 30)
    
    # Save the trained model
    model_path = 'aqi_sarimax_model.pkl'
    forecaster.save_model(model_path)
    
    # Save model metadata
    metadata = {
        'model_type': 'SARIMAX',
        'order': forecaster.order,
        'seasonal_order': forecaster.seasonal_order,
        'training_data_shape': training_data.shape,
        'training_date_range': (training_data.index.min().strftime('%Y-%m-%d'),
                               training_data.index.max().strftime('%Y-%m-%d')),
        'validation_metrics': {
            'mae': float(mae),
            'rmse': float(rmse),
            'mape': float(mape)
        },
        'aic': float(forecaster.fitted_model.aic),
        'bic': float(forecaster.fitted_model.bic),
        'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    import json
    with open('model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Model saved to: {model_path}")
    print("Model metadata saved to: model_metadata.json")
    
    # Step 7: Generate Forecast Summary
    print("\n7. FORECAST SUMMARY")
    print("-" * 30)
    
    # Generate 30-day forecast
    forecast_result = forecaster.forecast(steps=30)
    
    print(f"30-day forecast statistics:")
    print(f"  Mean AQI: {forecast_result['forecast'].mean():.1f}")
    print(f"  Min AQI: {forecast_result['forecast'].min():.1f}")
    print(f"  Max AQI: {forecast_result['forecast'].max():.1f}")
    print(f"  Std AQI: {forecast_result['forecast'].std():.1f}")
    
    # Categorize predictions
    def categorize_aqi(aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 200:
            return "Poor"
        elif aqi <= 300:
            return "Very Poor"
        else:
            return "Hazardous"
    
    categories = forecast_result['forecast'].apply(categorize_aqi)
    category_counts = categories.value_counts()
    
    print(f"\n30-day forecast categories:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} days ({count/30*100:.1f}%)")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return forecaster, metadata

def load_trained_model():
    """
    Load the trained SARIMAX model.
    
    Returns:
        tuple: (forecaster, metadata)
    """
    if not os.path.exists('aqi_sarimax_model.pkl'):
        raise FileNotFoundError("Trained model not found. Please run train_aqi_forecasting_model() first.")
    
    # Load model
    forecaster = AQISARIMAXForecaster()
    forecaster.load_model('aqi_sarimax_model.pkl')
    
    # Load metadata
    import json
    with open('model_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    print("Trained model loaded successfully!")
    print(f"Model type: {metadata['model_type']}")
    print(f"Training date range: {metadata['training_date_range'][0]} to {metadata['training_date_range'][1]}")
    print(f"Validation RMSE: {metadata['validation_metrics']['rmse']:.2f}")
    
    return forecaster, metadata

def predict_aqi_for_date(target_date_str: str, forecaster=None, training_data=None):
    """
    Predict AQI for a specific date.
    
    Args:
        target_date_str (str): Target date in YYYY-MM-DD format
        forecaster: Trained SARIMAX forecaster (optional)
        training_data: Historical training data (optional)
        
    Returns:
        dict: Prediction results
    """
    if forecaster is None or training_data is None:
        forecaster, metadata = load_trained_model()
        
        # Load training data for exogenous variable generation
        preprocessor = AQIDataPreprocessor('aqidaily_fiveyears.csv')
        processed_data = preprocessor.preprocess()
        training_data = preprocessor.get_training_data(end_date='2024-12-31')
    
    try:
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
        
        # Check if date is in historical range
        historical_start = training_data.index.min()
        historical_end = training_data.index.max()
        
        if historical_start <= target_date <= historical_end:
            # Return actual historical value
            actual_aqi = training_data.loc[target_date, 'aqi']
            return {
                'date': target_date_str,
                'predicted_AQI': float(actual_aqi),
                'is_historical': True,
                'source': 'historical_data'
            }
        else:
            # Generate forecast
            exog_future = generate_future_exogenous_data(target_date, training_data)
            prediction = forecaster.predict_single_date(target_date, exog_future)
            
            return {
                'date': target_date_str,
                'predicted_AQI': float(prediction),
                'is_historical': False,
                'source': 'sarimax_forecast',
                'exogenous_variables': exog_future.to_dict()
            }
            
    except ValueError as e:
        return {
            'error': f"Invalid date format: {str(e)}",
            'date': target_date_str
        }
    except Exception as e:
        return {
            'error': f"Prediction failed: {str(e)}",
            'date': target_date_str
        }

def main():
    """Main function to run training or testing."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        # Train the model
        forecaster, metadata = train_aqi_forecasting_model()
        
    elif len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Test predictions
        test_dates = ['2024-12-15', '2025-01-15', '2025-04-09', '2025-07-20']
        
        print("Testing predictions for sample dates:")
        for test_date in test_dates:
            result = predict_aqi_for_date(test_date)
            if 'error' in result:
                print(f"{test_date}: ERROR - {result['error']}")
            else:
                source = "Historical" if result['is_historical'] else "Forecast"
                print(f"{test_date}: AQI = {result['predicted_AQI']:.1f} ({source})")
    
    else:
        print("Usage:")
        print("  python model_training.py train  # Train the model")
        print("  python model_training.py test   # Test predictions")

if __name__ == "__main__":
    main()
