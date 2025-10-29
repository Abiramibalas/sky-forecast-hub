# Sky Forecast Hub API Documentation 📡

## API Overview

**Sky Forecast Hub** uses **FastAPI** - a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.

### 🚀 **API Framework**: FastAPI
- **Version**: 0.104.1
- **Language**: Python 3.8+
- **Server**: Uvicorn ASGI server
- **Documentation**: Automatic OpenAPI/Swagger documentation
- **Validation**: Pydantic models for request/response validation

### 🌐 **Base URL**
```
http://127.0.0.1:8000
```

### 📚 **Interactive Documentation**
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

---

## 🔗 API Endpoints

### 1. **Health Check Endpoint**

#### `GET /`
**Description**: Check if the API is running

**Request**:
```http
GET http://127.0.0.1:8000/
```

**Response**:
```json
{
  "message": "Air Quality Prediction API is running."
}
```

**Status Codes**:
- `200 OK`: API is running successfully

---

### 2. **Manual AQI Prediction Endpoint**

#### `POST /predict`
**Description**: Predict AQI based on manual input of environmental conditions

**Request Body**:
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

**Request Schema** (`AQIInput`):
| Field | Type | Description | Units |
|-------|------|-------------|-------|
| `Temperature` | float | Air temperature | °C |
| `Humidity` | float | Relative humidity | % |
| `WindSpeed` | float | Wind speed | m/s |
| `NO2` | float | Nitrogen dioxide concentration | µg/m³ |
| `CO` | float | Carbon monoxide concentration | mg/m³ |
| `PM25` | float | PM2.5 particulate matter | µg/m³ |
| `PM10` | float | PM10 particulate matter | µg/m³ |

**Response**:
```json
{
  "predicted_AQI": 78.5,
  "category": "Moderate",
  "explanation": "High temperature (25.5°C) can increase ozone formation. Moderate humidity (65.2%) may trap pollutants. Wind speed (12.3 m/s) helps disperse pollutants. Elevated PM2.5 levels (35.8 µg/m³) contribute to air quality concerns. Air quality is acceptable for most people, but sensitive individuals may experience minor respiratory issues."
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `predicted_AQI` | float | Predicted Air Quality Index (0-500+) |
| `category` | string | AQI category (Good, Moderate, Poor, Very Poor, Hazardous) |
| `explanation` | string | Detailed explanation of the prediction |

**Status Codes**:
- `200 OK`: Prediction successful
- `422 Unprocessable Entity`: Invalid input data
- `500 Internal Server Error`: Server error

---

### 3. **Date-Based AQI Prediction Endpoint**

#### `POST /predict-by-date`
**Description**: Predict AQI based on seasonal patterns for a specific date

**Request Body**:
```json
{
  "date": "2024-06-15"
}
```

**Request Schema** (`DateInput`):
| Field | Type | Description | Format |
|-------|------|-------------|--------|
| `date` | string | Target date for prediction | YYYY-MM-DD |

**Response**:
```json
{
  "predicted_AQI": 70.2,
  "category": "Moderate",
  "explanation": "Prediction for June 15, 2024 (Summer season) | Summer conditions may show moderate pollution with better atmospheric mixing. | High temperature (34.7°C) can increase ozone formation. | Air quality is expected to be acceptable for most people, but sensitive individuals may experience minor respiratory issues.",
  "estimated_conditions": {
    "Temperature": 34.7,
    "Humidity": 76.3,
    "WindSpeed": 10.7,
    "NO2": 35.2,
    "CO": 2.1,
    "PM25": 24.1,
    "PM10": 30.5
  },
  "date": "2024-06-15"
}
```

**Response Schema**:
| Field | Type | Description |
|-------|------|-------------|
| `predicted_AQI` | float | Predicted Air Quality Index |
| `category` | string | AQI category |
| `explanation` | string | Seasonal analysis and explanation |
| `estimated_conditions` | object | Estimated environmental conditions for the date |
| `date` | string | The input date |

**Estimated Conditions Schema**:
| Field | Type | Description | Units |
|-------|------|-------------|-------|
| `Temperature` | float | Estimated temperature | °C |
| `Humidity` | float | Estimated humidity | % |
| `WindSpeed` | float | Estimated wind speed | m/s |
| `NO2` | float | Estimated NO2 concentration | µg/m³ |
| `CO` | float | Estimated CO concentration | mg/m³ |
| `PM25` | float | Estimated PM2.5 concentration | µg/m³ |
| `PM10` | float | Estimated PM10 concentration | µg/m³ |

**Status Codes**:
- `200 OK`: Prediction successful
- `422 Unprocessable Entity`: Invalid date format
- `500 Internal Server Error`: Server error

---

## 🎯 AQI Categories

| AQI Range | Category | Health Impact | Recommendation |
|-----------|----------|---------------|----------------|
| **0-50** | Good | Air quality is satisfactory | Normal outdoor activities |
| **51-100** | Moderate | Acceptable for most people | Sensitive groups should limit outdoor activities |
| **101-200** | Poor | Sensitive groups may experience health effects | Avoid outdoor activities for sensitive groups |
| **201-300** | Very Poor | Health alert for everyone | Everyone should avoid outdoor activities |
| **300+** | Hazardous | Emergency conditions | Stay indoors, avoid all outdoor activities |

---

## 🔧 Technical Details

### **CORS Configuration**
The API includes CORS middleware to allow requests from:
- `http://localhost:8080`
- `http://localhost:8081`
- `http://127.0.0.1:8080`
- `http://127.0.0.1:8081`

### **Machine Learning Model**
- **Algorithm**: Gradient Boosting Regressor
- **Accuracy**: 94% cross-validation R² score
- **Features**: 8 engineered features including temporal and seasonal patterns
- **Scaling**: RobustScaler for numerical stability

### **Data Processing**
- **Input Validation**: Pydantic models ensure data integrity
- **Feature Engineering**: Automatic creation of temporal and seasonal features
- **Error Handling**: Comprehensive error responses with meaningful messages

---

## 🧪 Testing the API

### **Using cURL**

#### Health Check:
```bash
curl -X GET "http://127.0.0.1:8000/"
```

#### Manual Prediction:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Temperature": 25.5,
    "Humidity": 65.2,
    "WindSpeed": 12.3,
    "NO2": 45.2,
    "CO": 2.1,
    "PM25": 35.8,
    "PM10": 42.1
  }'
```

#### Date-Based Prediction:
```bash
curl -X POST "http://127.0.0.1:8000/predict-by-date" \
  -H "Content-Type: application/json" \
  -d '{"date": "2024-06-15"}'
```

### **Using Python Requests**

```python
import requests
import json

# Health check
response = requests.get("http://127.0.0.1:8000/")
print(response.json())

# Manual prediction
data = {
    "Temperature": 25.5,
    "Humidity": 65.2,
    "WindSpeed": 12.3,
    "NO2": 45.2,
    "CO": 2.1,
    "PM25": 35.8,
    "PM10": 42.1
}
response = requests.post("http://127.0.0.1:8000/predict", json=data)
print(response.json())

# Date-based prediction
data = {"date": "2024-06-15"}
response = requests.post("http://127.0.0.1:8000/predict-by-date", json=data)
print(response.json())
```

### **Using JavaScript/Fetch**

```javascript
// Health check
fetch('http://127.0.0.1:8000/')
  .then(response => response.json())
  .then(data => console.log(data));

// Manual prediction
const predictionData = {
  Temperature: 25.5,
  Humidity: 65.2,
  WindSpeed: 12.3,
  NO2: 45.2,
  CO: 2.1,
  PM25: 35.8,
  PM10: 42.1
};

fetch('http://127.0.0.1:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(predictionData)
})
.then(response => response.json())
.then(data => console.log(data));

// Date-based prediction
const dateData = { date: "2024-06-15" };
fetch('http://127.0.0.1:8000/predict-by-date', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(dateData)
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🚀 Running the API

### **Start the API Server**:
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Access Points**:
- **API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📊 API Performance

- **Response Time**: < 100ms for predictions
- **Throughput**: Handles multiple concurrent requests
- **Memory Usage**: Optimized with model caching
- **Scalability**: Can be deployed on cloud platforms

---

## 🔒 Security Features

- **Input Validation**: Pydantic models prevent invalid data
- **CORS Protection**: Configured for specific origins
- **Error Handling**: No sensitive information in error messages
- **Rate Limiting**: Can be added for production deployment

---

## 📈 Monitoring & Logging

The API includes comprehensive logging for:
- Request/response cycles
- Model predictions
- Error tracking
- Performance metrics

---

**Sky Forecast Hub API** - Powered by FastAPI and Machine Learning 🌤️
