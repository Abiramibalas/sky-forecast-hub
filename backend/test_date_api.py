#!/usr/bin/env python3
"""
Test script for the Date-based Air Quality Prediction API
"""
import requests
import json
from datetime import datetime, timedelta

def test_date_api():
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get("http://127.0.0.1:8000/")
        print(f"Health check: {response.json()}")
        print()
        
        # Test different dates
        test_dates = [
            "2024-01-15",  # Winter
            "2024-06-15",  # Summer
            "2024-03-15",  # Spring
            "2024-09-15",  # Fall
            "2025-12-25",  # Future winter
        ]
        
        for test_date in test_dates:
            print(f"🧪 Testing date: {test_date}")
            print("-" * 50)
            
            response = requests.post(
                "http://127.0.0.1:8000/predict-by-date",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"date": test_date})
            )
            
            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    print(f"❌ Error: {result['error']}")
                else:
                    print(f"✅ Predicted AQI: {result['predicted_AQI']}")
                    print(f"📊 Category: {result['category']}")
                    print(f"📅 Date: {result['date']}")
                    print(f"💡 Explanation: {result['explanation']}")
                    if 'estimated_conditions' in result:
                        conditions = result['estimated_conditions']
                        print(f"🌡️  Estimated Conditions:")
                        print(f"   Temperature: {conditions['Temperature']}°C")
                        print(f"   Humidity: {conditions['Humidity']}%")
                        print(f"   Wind Speed: {conditions['WindSpeed']} m/s")
                        print(f"   PM2.5: {conditions['PM25']} µg/m³")
                        print(f"   PM10: {conditions['PM10']} µg/m³")
            else:
                print(f"❌ Prediction failed: {response.status_code}")
                print(response.text)
            
            print()
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the backend is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_date_api()
