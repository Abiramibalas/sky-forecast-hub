# Sky Forecast Hub - Backend API

This is the backend ML API for the Sky Forecast Hub air quality prediction system.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

- `GET /` - Health check endpoint
- `POST /predict` - Predict AQI based on input parameters

### Predict Endpoint

Send a POST request to `/predict` with the following JSON structure:

```json
{
  "Temperature": 25.5,
  "Humidity": 65.2,
  "WindSpeed": 12.3,
  "NO2": 45.2,
  "CO": 2.1,
  "PM25": 35.8,
  "PM10": 42.1
}
```

Response:
```json
{
  "predicted_AQI": 78.5,
  "category": "Moderate"
}
```

## AQI Categories

- 0-50: Good
- 51-100: Moderate
- 101-200: Poor
- 201-300: Very Poor
- 300+: Hazardous

## Data Requirements

The API expects a CSV file named `aqidaily_fiveyears.csv` in the same directory with the following columns:
- Temperature
- Humidity
- WindSpeed
- NO2
- CO
- PM25
- PM10
- AQI (target variable)

