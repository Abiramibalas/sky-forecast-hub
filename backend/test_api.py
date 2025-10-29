#!/usr/bin/env python3
"""
Test script for the Air Quality Prediction API
"""
import requests
import json

# Test data
test_data = {
    "Temperature": 25.5,
    "Humidity": 65.2,
    "WindSpeed": 12.3,
    "NO2": 45.2,
    "CO": 2.1,
    "PM25": 35.8,
    "PM10": 42.1
}

def test_api():
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Health check: {response.json()}")
        
        # Test prediction endpoint
        print("\nTesting prediction endpoint...")
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction successful!")
            print(f"Predicted AQI: {result['predicted_AQI']}")
            print(f"Category: {result['category']}")
            if 'explanation' in result:
                print(f"Explanation: {result['explanation']}")
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the backend is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
