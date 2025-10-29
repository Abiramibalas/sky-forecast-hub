from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from datetime import datetime, timedelta
import random

app = FastAPI(title="Air Quality Prediction API", version="1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081", "http://127.0.0.1:8080", "http://127.0.0.1:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Data Loading and Model Training ----------
DATA_PATH = "aqidaily_fiveyears.csv"
MODEL_PATH = "enhanced_aqi_model.pkl"
SCALER_PATH = "enhanced_scaler.pkl"
FEATURE_NAMES_PATH = "feature_names.pkl"

# Define input schema
class AQIInput(BaseModel):
    Temperature: float
    Humidity: float
    WindSpeed: float
    NO2: float
    CO: float
    PM25: float
    PM10: float

class DateInput(BaseModel):
    date: str  # Format: YYYY-MM-DD


# Load or train model
def train_model():
    df = pd.read_csv(DATA_PATH)

    # Clean dataset (rename columns if needed)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Example assumption: AQI is the target column
    target_col = "aqi"
    if target_col not in df.columns:
        raise ValueError("The dataset must contain a column named 'AQI'.")

    X = df.drop(columns=[target_col])
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    print("✅ Model trained and saved successfully!")
    return model


# Load model, scaler, and feature names
if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(FEATURE_NAMES_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)
    print("✅ Enhanced model loaded successfully!")
else:
    print("❌ Enhanced model files not found. Please run realistic_model_training.py first.")
    # Fallback to old model if available
    if os.path.exists("aqi_model.pkl"):
        model = joblib.load("aqi_model.pkl")
        scaler = None
        feature_names = None
        print("⚠️  Using fallback model")
    else:
        raise FileNotFoundError("No model found. Please train a model first.")


# ---------- API Endpoints ----------
@app.get("/")
def root():
    return {"message": "Air Quality Prediction API is running."}


@app.post("/predict")
def predict_aqi(input_data: AQIInput):
    # Create feature vector based on enhanced model
    if feature_names is not None:
        # Use enhanced model with proper feature engineering
        features = create_prediction_features(input_data)
        data = np.array([features])
        
        # Apply scaling if scaler is available
        if scaler is not None:
            data = scaler.transform(data)
    else:
        # Fallback to original format
        data = np.array([
            [
                input_data.Temperature,
                input_data.Humidity,
                input_data.WindSpeed,
                input_data.NO2,
                input_data.CO,
                input_data.PM25,
                input_data.PM10
            ]
        ])

    prediction = model.predict(data)[0]

    # AQI category logic
    if prediction <= 50:
        category = "Good"
    elif prediction <= 100:
        category = "Moderate"
    elif prediction <= 200:
        category = "Poor"
    elif prediction <= 300:
        category = "Very Poor"
    else:
        category = "Hazardous"

    # Generate explanation based on input values
    explanation = generate_explanation(input_data, prediction, category)

    return {
        "predicted_AQI": round(float(prediction), 2),
        "category": category,
        "explanation": explanation
    }


@app.post("/predict-by-date")
def predict_aqi_by_date(input_data: DateInput):
    """Predict AQI based on historical data patterns for a specific date"""
    try:
        # Parse the input date
        target_date = datetime.strptime(input_data.date, "%Y-%m-%d")
        
        # Generate realistic environmental conditions based on date patterns
        environmental_data = generate_seasonal_data(target_date)
        
        # Create AQIInput object for prediction
        aqi_input = AQIInput(**environmental_data)
        
        # Use enhanced model if available
        if feature_names is not None:
            # Create features for date-based prediction
            features = create_date_prediction_features(target_date, environmental_data)
            data = np.array([features])
            
            # Apply scaling if scaler is available
            if scaler is not None:
                data = scaler.transform(data)
        else:
            # Fallback to original format
            data = np.array([
                [
                    aqi_input.Temperature,
                    aqi_input.Humidity,
                    aqi_input.WindSpeed,
                    aqi_input.NO2,
                    aqi_input.CO,
                    aqi_input.PM25,
                    aqi_input.PM10
                ]
            ])
        
        prediction = model.predict(data)[0]
        
        # AQI category logic
        if prediction <= 50:
            category = "Good"
        elif prediction <= 100:
            category = "Moderate"
        elif prediction <= 200:
            category = "Poor"
        elif prediction <= 300:
            category = "Very Poor"
        else:
            category = "Hazardous"
        
        # Generate explanation for date-based prediction
        explanation = generate_date_explanation(target_date, environmental_data, prediction, category)
        
        return {
            "predicted_AQI": round(float(prediction), 2),
            "category": category,
            "explanation": explanation,
            "estimated_conditions": environmental_data,
            "date": input_data.date
        }
        
    except ValueError as e:
        return {"error": f"Invalid date format. Please use YYYY-MM-DD format. Error: {str(e)}"}
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}


def create_prediction_features(input_data: AQIInput) -> list:
    """Create feature vector for enhanced model prediction"""
    from datetime import datetime
    
    # Get current date for temporal features
    now = datetime.now()
    
    # Basic pollutant features
    features = [
        input_data.CO,
        input_data.NO2,  # Using NO2 as ozone proxy
        input_data.PM10,
        input_data.PM25,
        input_data.NO2  # Using NO2 as second pollutant
    ]
    
    # Temporal features
    features.extend([
        now.month,
        now.timetuple().tm_yday,
        1 if now.weekday() >= 5 else 0  # is_weekend
    ])
    
    return features


def create_date_prediction_features(target_date: datetime, environmental_data: dict) -> list:
    """Create feature vector for date-based prediction using enhanced model"""
    
    # Basic pollutant features
    features = [
        environmental_data['CO'],
        environmental_data['NO2'],  # Using NO2 as ozone proxy
        environmental_data['PM10'],
        environmental_data['PM25'],
        environmental_data['NO2']  # Using NO2 as second pollutant
    ]
    
    # Temporal features
    features.extend([
        target_date.month,
        target_date.timetuple().tm_yday,
        1 if target_date.weekday() >= 5 else 0  # is_weekend
    ])
    
    return features


def generate_seasonal_data(target_date: datetime) -> dict:
    """Generate realistic environmental conditions based on seasonal patterns"""
    
    # Extract month and day for seasonal patterns
    month = target_date.month
    day_of_year = target_date.timetuple().tm_yday
    
    # Seasonal temperature patterns (Northern Hemisphere)
    base_temp = 20 + 10 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
    temperature = base_temp + random.uniform(-5, 5)
    
    # Seasonal humidity patterns
    if month in [6, 7, 8]:  # Summer
        humidity = random.uniform(60, 85)
    elif month in [12, 1, 2]:  # Winter
        humidity = random.uniform(40, 70)
    else:  # Spring/Fall
        humidity = random.uniform(50, 75)
    
    # Wind speed (generally higher in winter/spring)
    if month in [12, 1, 2, 3]:  # Winter/Spring
        wind_speed = random.uniform(8, 18)
    else:
        wind_speed = random.uniform(5, 12)
    
    # Pollutant levels based on seasonal patterns
    # Higher in winter due to heating, lower in summer due to better dispersion
    if month in [12, 1, 2]:  # Winter - higher pollution
        no2 = random.uniform(40, 80)
        co = random.uniform(2, 6)
        pm25 = random.uniform(30, 70)
        pm10 = random.uniform(40, 90)
    elif month in [6, 7, 8]:  # Summer - moderate pollution
        no2 = random.uniform(25, 50)
        co = random.uniform(1, 3)
        pm25 = random.uniform(20, 45)
        pm10 = random.uniform(25, 55)
    else:  # Spring/Fall - moderate pollution
        no2 = random.uniform(30, 60)
        co = random.uniform(1.5, 4)
        pm25 = random.uniform(25, 55)
        pm10 = random.uniform(30, 65)
    
    return {
        "Temperature": round(temperature, 1),
        "Humidity": round(humidity, 1),
        "WindSpeed": round(wind_speed, 1),
        "NO2": round(no2, 1),
        "CO": round(co, 1),
        "PM25": round(pm25, 1),
        "PM10": round(pm10, 1)
    }


def generate_date_explanation(target_date: datetime, conditions: dict, predicted_aqi: float, category: str) -> str:
    """Generate explanation for date-based prediction"""
    
    explanations = []
    
    # Date-specific analysis
    month_name = target_date.strftime("%B")
    season = get_season(target_date.month)
    
    explanations.append(f"Prediction for {target_date.strftime('%B %d, %Y')} ({season} season)")
    
    # Seasonal patterns
    if season == "Winter":
        explanations.append("Winter conditions typically show higher pollution due to heating emissions and temperature inversions.")
    elif season == "Summer":
        explanations.append("Summer conditions may show moderate pollution with better atmospheric mixing.")
    elif season == "Spring":
        explanations.append("Spring conditions often show variable pollution levels with changing weather patterns.")
    elif season == "Fall":
        explanations.append("Fall conditions typically show moderate pollution with seasonal transitions.")
    
    # Condition-based analysis
    if conditions["Temperature"] > 30:
        explanations.append(f"High temperature ({conditions['Temperature']}°C) can increase ozone formation.")
    elif conditions["Temperature"] < 10:
        explanations.append(f"Low temperature ({conditions['Temperature']}°C) may lead to increased heating emissions.")
    
    if conditions["Humidity"] > 80:
        explanations.append(f"High humidity ({conditions['Humidity']}%) can trap pollutants near the ground.")
    
    if conditions["WindSpeed"] < 5:
        explanations.append(f"Low wind speed ({conditions['WindSpeed']} m/s) prevents pollutant dispersion.")
    
    # Primary pollutant analysis
    pollutants = {
        "PM2.5": conditions["PM25"],
        "PM10": conditions["PM10"],
        "NO2": conditions["NO2"],
        "CO": conditions["CO"]
    }
    
    max_pollutant = max(pollutants, key=pollutants.get)
    max_value = pollutants[max_pollutant]
    
    if max_pollutant == "PM2.5" and max_value > 50:
        explanations.append(f"High PM2.5 levels ({max_value} µg/m³) are the primary concern.")
    elif max_pollutant == "PM10" and max_value > 100:
        explanations.append(f"High PM10 levels ({max_value} µg/m³) indicate significant particle pollution.")
    elif max_pollutant == "NO2" and max_value > 60:
        explanations.append(f"Elevated NO2 levels ({max_value} µg/m³) suggest traffic-related pollution.")
    
    # Category-specific explanation
    if category == "Good":
        explanations.append("Overall air quality is expected to be satisfactory with minimal health risks.")
    elif category == "Moderate":
        explanations.append("Air quality is expected to be acceptable for most people, but sensitive individuals may experience minor respiratory issues.")
    elif category == "Poor":
        explanations.append("Air quality may cause health problems for sensitive groups and some discomfort for the general population.")
    elif category == "Very Poor":
        explanations.append("Air quality poses significant health risks, especially for children, elderly, and those with respiratory conditions.")
    elif category == "Hazardous":
        explanations.append("Air quality is extremely dangerous - everyone should avoid outdoor activities and sensitive groups should stay indoors.")
    
    return " | ".join(explanations)


def get_season(month: int) -> str:
    """Get season based on month"""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"


def generate_explanation(input_data: AQIInput, predicted_aqi: float, category: str) -> str:
    """Generate explanation for the AQI prediction based on input parameters"""
    
    explanations = []
    
    # Temperature analysis
    if input_data.Temperature > 30:
        explanations.append(f"High temperature ({input_data.Temperature}°C) can increase ozone formation and particle suspension.")
    elif input_data.Temperature < 10:
        explanations.append(f"Low temperature ({input_data.Temperature}°C) may lead to increased heating emissions.")
    
    # Humidity analysis
    if input_data.Humidity > 80:
        explanations.append(f"High humidity ({input_data.Humidity}%) can trap pollutants near the ground.")
    elif input_data.Humidity < 30:
        explanations.append(f"Low humidity ({input_data.Humidity}%) allows particles to remain airborne longer.")
    
    # Wind speed analysis
    if input_data.WindSpeed < 5:
        explanations.append(f"Low wind speed ({input_data.WindSpeed} m/s) prevents pollutant dispersion.")
    elif input_data.WindSpeed > 15:
        explanations.append(f"High wind speed ({input_data.WindSpeed} m/s) helps disperse pollutants.")
    
    # Pollutant analysis - identify primary contributors
    pollutants = {
        "PM2.5": input_data.PM25,
        "PM10": input_data.PM10,
        "NO2": input_data.NO2,
        "CO": input_data.CO
    }
    
    # Find the highest pollutant
    max_pollutant = max(pollutants, key=pollutants.get)
    max_value = pollutants[max_pollutant]
    
    # Add pollutant-specific explanations
    if max_pollutant == "PM2.5":
        if max_value > 50:
            explanations.append(f"High PM2.5 levels ({max_value} µg/m³) are the primary concern - these fine particles can penetrate deep into lungs.")
        elif max_value > 25:
            explanations.append(f"Elevated PM2.5 levels ({max_value} µg/m³) contribute significantly to air quality concerns.")
    elif max_pollutant == "PM10":
        if max_value > 100:
            explanations.append(f"High PM10 levels ({max_value} µg/m³) indicate significant coarse particle pollution.")
        elif max_value > 50:
            explanations.append(f"Elevated PM10 levels ({max_value} µg/m³) contribute to air quality degradation.")
    elif max_pollutant == "NO2":
        if max_value > 100:
            explanations.append(f"High NO2 levels ({max_value} µg/m³) suggest heavy traffic or industrial emissions.")
        elif max_value > 50:
            explanations.append(f"Elevated NO2 levels ({max_value} µg/m³) indicate moderate traffic-related pollution.")
    elif max_pollutant == "CO":
        if max_value > 10:
            explanations.append(f"High CO levels ({max_value} mg/m³) indicate incomplete combustion from vehicles or industry.")
        elif max_value > 5:
            explanations.append(f"Elevated CO levels ({max_value} mg/m³) suggest moderate combustion-related pollution.")
    
    # Add category-specific explanation
    if category == "Good":
        explanations.append("Overall air quality is satisfactory with minimal health risks.")
    elif category == "Moderate":
        explanations.append("Air quality is acceptable for most people, but sensitive individuals may experience minor respiratory issues.")
    elif category == "Poor":
        explanations.append("Air quality may cause health problems for sensitive groups and some discomfort for the general population.")
    elif category == "Very Poor":
        explanations.append("Air quality poses significant health risks, especially for children, elderly, and those with respiratory conditions.")
    elif category == "Hazardous":
        explanations.append("Air quality is extremely dangerous - everyone should avoid outdoor activities and sensitive groups should stay indoors.")
    
    # Combine explanations
    if explanations:
        return " | ".join(explanations)
    else:
        return f"Predicted AQI of {predicted_aqi:.1f} falls into the {category} category based on current environmental conditions."
