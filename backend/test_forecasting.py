"""
Test script for AQI time-series forecasting implementation.
Tests both historical data retrieval and future date forecasting.
"""

import requests
import json
from datetime import datetime, timedelta
import time

def test_api_endpoints():
    """Test the API endpoints for AQI prediction"""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("TESTING AQI TIME-SERIES FORECASTING API")
    print("=" * 60)
    
    # Test 1: Check model status
    print("\n1. CHECKING MODEL STATUS")
    print("-" * 30)
    
    try:
        response = requests.get(f"{base_url}/model-status")
        if response.status_code == 200:
            status = response.json()
            print("✅ Model status retrieved successfully")
            print(f"Random Forest Model: {'✅ Loaded' if status['random_forest_model']['loaded'] else '❌ Not loaded'}")
            print(f"SARIMAX Model: {'✅ Loaded' if status['sarimax_model']['loaded'] else '❌ Not loaded'}")
            
            if status['sarimax_model']['loaded']:
                print(f"   Training range: {status['sarimax_model']['training_date_range'][0]} to {status['sarimax_model']['training_date_range'][1]}")
                print(f"   Validation RMSE: {status['sarimax_model']['validation_rmse']:.2f}")
                print(f"   Model order: {status['sarimax_model']['order']}")
                print(f"   Seasonal order: {status['sarimax_model']['seasonal_order']}")
        else:
            print(f"❌ Failed to get model status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking model status: {e}")
    
    # Test 2: Historical date prediction
    print("\n2. TESTING HISTORICAL DATE PREDICTION")
    print("-" * 30)
    
    historical_dates = [
        "2024-01-15",
        "2024-06-20", 
        "2024-12-25"
    ]
    
    for date in historical_dates:
        try:
            response = requests.post(f"{base_url}/predict-by-date", 
                                  json={"date": date})
            if response.status_code == 200:
                result = response.json()
                if 'error' not in result:
                    source = "Historical" if result.get('is_historical', False) else "Forecast"
                    print(f"✅ {date}: AQI = {result['predicted_AQI']:.1f} ({result['category']}) - {source}")
                else:
                    print(f"❌ {date}: {result['error']}")
            else:
                print(f"❌ {date}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {date}: {e}")
    
    # Test 3: Future date prediction
    print("\n3. TESTING FUTURE DATE PREDICTION")
    print("-" * 30)
    
    future_dates = [
        "2025-01-15",
        "2025-04-09",  # The specific date mentioned in requirements
        "2025-07-20",
        "2025-10-31"
    ]
    
    for date in future_dates:
        try:
            response = requests.post(f"{base_url}/predict-by-date", 
                                  json={"date": date})
            if response.status_code == 200:
                result = response.json()
                if 'error' not in result:
                    source = "Historical" if result.get('is_historical', False) else "Forecast"
                    print(f"✅ {date}: AQI = {result['predicted_AQI']:.1f} ({result['category']}) - {source}")
                    
                    if 'model_info' in result:
                        print(f"   Model: {result['model_info']['type']}, RMSE: {result['model_info']['validation_rmse']:.2f}")
                else:
                    print(f"❌ {date}: {result['error']}")
            else:
                print(f"❌ {date}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {date}: {e}")
    
    # Test 4: Edge cases
    print("\n4. TESTING EDGE CASES")
    print("-" * 30)
    
    edge_cases = [
        "2024-12-31",  # Last day of training data
        "2025-01-01",  # First day after training data
        "invalid-date",  # Invalid date format
        "2025-13-01",   # Invalid month
        "2025-02-30"    # Invalid day
    ]
    
    for date in edge_cases:
        try:
            response = requests.post(f"{base_url}/predict-by-date", 
                                  json={"date": date})
            if response.status_code == 200:
                result = response.json()
                if 'error' not in result:
                    source = "Historical" if result.get('is_historical', False) else "Forecast"
                    print(f"✅ {date}: AQI = {result['predicted_AQI']:.1f} ({result['category']}) - {source}")
                else:
                    print(f"⚠️  {date}: {result['error']}")
            else:
                print(f"❌ {date}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {date}: {e}")
    
    # Test 5: Traditional prediction endpoint
    print("\n5. TESTING TRADITIONAL PREDICTION ENDPOINT")
    print("-" * 30)
    
    try:
        sample_data = {
            "Temperature": 25.0,
            "Humidity": 60.0,
            "WindSpeed": 10.0,
            "NO2": 30.0,
            "CO": 2.0,
            "PM25": 20.0,
            "PM10": 30.0
        }
        
        response = requests.post(f"{base_url}/predict", json=sample_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Traditional prediction: AQI = {result['predicted_AQI']:.1f} ({result['category']})")
        else:
            print(f"❌ Traditional prediction failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Traditional prediction error: {e}")
    
    print("\n" + "=" * 60)
    print("TESTING COMPLETED")
    print("=" * 60)

def test_model_training():
    """Test the model training pipeline"""
    print("\nTESTING MODEL TRAINING PIPELINE")
    print("-" * 40)
    
    try:
        # Import and test the training modules
        from data_preprocessing import AQIDataPreprocessor
        from sarimax_forecaster import AQISARIMAXForecaster
        from model_training import train_aqi_forecasting_model
        
        print("✅ All modules imported successfully")
        
        # Test data preprocessing
        print("\nTesting data preprocessing...")
        preprocessor = AQIDataPreprocessor('aqidaily_fiveyears.csv')
        processed_data = preprocessor.preprocess()
        print(f"✅ Data preprocessing completed. Shape: {processed_data.shape}")
        
        # Test training data preparation
        training_data = preprocessor.get_training_data()
        print(f"✅ Training data prepared. Shape: {training_data.shape}")
        
        # Test exogenous variables
        exog_data = preprocessor.get_exogenous_variables(training_data)
        print(f"✅ Exogenous variables prepared. Shape: {exog_data.shape}")
        
        print("\n✅ Model training pipeline components working correctly")
        
    except Exception as e:
        print(f"❌ Model training pipeline error: {e}")

def main():
    """Main test function"""
    print("Starting AQI Time-Series Forecasting Tests...")
    
    # Test model training components first
    test_model_training()
    
    # Wait a moment for any server to start
    print("\nWaiting 2 seconds for server to be ready...")
    time.sleep(2)
    
    # Test API endpoints
    test_api_endpoints()

if __name__ == "__main__":
    main()
