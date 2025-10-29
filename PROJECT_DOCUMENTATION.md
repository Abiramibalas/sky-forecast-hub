# Sky Forecast Hub 🌤️

**An Advanced Air Quality Prediction System using Machine Learning**

## 📋 Project Overview

Sky Forecast Hub is a comprehensive air quality prediction system that combines modern web technologies with advanced machine learning algorithms to provide accurate AQI (Air Quality Index) predictions. The system offers two prediction modes: manual input-based predictions and date-based seasonal predictions.

## 🎯 Key Features

### 🔬 **Dual Prediction Modes**
- **Manual Input Prediction**: Enter specific environmental conditions (temperature, humidity, wind speed, pollutants) for instant AQI predictions
- **Date-Based Prediction**: Select any date to get AQI predictions based on seasonal patterns and historical data

### 🤖 **Advanced Machine Learning**
- **Enhanced Gradient Boosting Model** with 94% cross-validation accuracy
- **Feature Engineering**: Temporal, seasonal, and pollutant interaction features
- **Hyperparameter Optimization**: Tuned for maximum performance
- **Time Series Validation**: Realistic evaluation using historical data patterns

### 📊 **Intelligent Analysis**
- **Detailed Explanations**: AI-powered analysis of prediction factors
- **Seasonal Intelligence**: Understanding of winter heating, summer mixing, etc.
- **Health Recommendations**: Category-specific health guidance
- **Real-time Predictions**: Instant results with comprehensive analysis

### 🎨 **Modern User Interface**
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Interactive Dashboard**: Beautiful charts and visualizations
- **Real-time Updates**: Live predictions with loading states
- **Accessibility**: Clean, intuitive interface

## 🏗️ Architecture

### **Frontend (React + TypeScript)**
```
src/
├── components/          # Reusable UI components
│   ├── ui/             # shadcn/ui component library
│   ├── Hero.tsx        # Landing section
│   ├── PredictionForm.tsx # Manual input prediction
│   ├── DatePredictionForm.tsx # Date-based prediction
│   ├── AQICard.tsx     # Results display
│   ├── ChartSection.tsx # Data visualization
│   └── Navbar.tsx      # Navigation
├── pages/              # Page components
├── hooks/              # Custom React hooks
└── lib/                # Utility functions
```

### **Backend (FastAPI + Python)**
```
backend/
├── main.py                    # FastAPI application
├── realistic_model_training.py # Model training script
├── enhanced_aqi_model.pkl     # Trained ML model
├── enhanced_scaler.pkl        # Data scaler
├── feature_names.pkl          # Feature names
├── aqidaily_fiveyears.csv     # Training dataset
├── requirements.txt           # Python dependencies
└── test_*.py                 # API testing scripts
```

## 🚀 Quick Start Guide

### **Prerequisites**
- **Node.js** (v18 or higher)
- **Python 3.8+**
- **npm** or **yarn**

### **Step 1: Clone and Setup**
```bash
# Clone the repository
git clone <your-repo-url>
cd sky-forecast-hub-main

# Run automated setup
./setup.sh
```

### **Step 2: Manual Setup (Alternative)**

#### **Frontend Setup**
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

#### **Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Step 3: Access the Application**
- **Frontend**: http://localhost:8081
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## 🔧 Technical Implementation

### **Machine Learning Pipeline**

1. **Data Preprocessing**
   - Handles missing values and data cleaning
   - Converts categorical data to numerical features
   - Implements proper train/test split

2. **Feature Engineering**
   - **Temporal Features**: month, day_of_year, is_weekend
   - **Seasonal Encoding**: Cyclical month and day features
   - **Pollutant Interactions**: Ratios and combinations
   - **Site-based Features**: Traffic, airport, urban classifications

3. **Model Training**
   - **Algorithm**: Gradient Boosting Regressor
   - **Hyperparameters**: learning_rate=0.1, max_depth=3, n_estimators=150
   - **Validation**: TimeSeriesSplit for realistic evaluation
   - **Scaling**: RobustScaler for numerical stability

4. **Performance Metrics**
   - **Cross-Validation R²**: 0.940
   - **Test R² Score**: 0.994
   - **Test RMSE**: 1.37
   - **Test MAE**: 0.47

### **API Endpoints**

#### **Manual Prediction**
```http
POST /predict
Content-Type: application/json

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

**Response:**
```json
{
  "predicted_AQI": 78.5,
  "category": "Moderate",
  "explanation": "High temperature (25.5°C) can increase ozone formation..."
}
```

#### **Date-Based Prediction**
```http
POST /predict-by-date
Content-Type: application/json

{
  "date": "2024-06-15"
}
```

**Response:**
```json
{
  "predicted_AQI": 70.2,
  "category": "Moderate",
  "explanation": "Prediction for June 15, 2024 (Summer season)...",
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

## 📊 AQI Categories

| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| **0-50** | Good | Air quality is satisfactory |
| **51-100** | Moderate | Acceptable for most people |
| **101-200** | Poor | Sensitive groups may experience health effects |
| **201-300** | Very Poor | Health alert for everyone |
| **300+** | Hazardous | Emergency conditions |

## 🧪 Testing

### **API Testing**
```bash
cd backend
source venv/bin/activate

# Test manual prediction
python test_api.py

# Test date-based prediction
python test_date_api.py

# Compare model performance
python model_comparison.py
```

### **Frontend Testing**
```bash
# Run linting
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📈 Performance Improvements

### **Model Accuracy Enhancements**
- **Data Quality**: Removed 1,197 rows with missing data
- **Feature Engineering**: Added 8 engineered features
- **Algorithm Selection**: Gradient Boosting vs Random Forest
- **Hyperparameter Tuning**: Optimized for maximum performance
- **Validation Strategy**: Time series cross-validation

### **Before vs After**
| Metric | Original | Enhanced | Improvement |
|--------|----------|----------|-------------|
| Cross-Validation R² | ~0.8 | **0.940** | +17.5% |
| Test RMSE | ~5-10 | **1.37** | 70-85% reduction |
| Features | 7 basic | **8 engineered** | Better feature set |
| Validation | Basic split | **Time series CV** | More realistic |

## 🌟 Key Innovations

1. **Dual Prediction System**: Manual input + date-based predictions
2. **Seasonal Intelligence**: Automatic seasonal pattern recognition
3. **Explainable AI**: Detailed explanations for every prediction
4. **Real-time Processing**: Instant predictions with comprehensive analysis
5. **Production-Ready**: Robust error handling and validation

## 🔮 Future Enhancements

- **Real-time Data Integration**: Connect to weather APIs
- **Mobile Application**: React Native version
- **User Authentication**: Personal prediction history
- **Advanced Visualizations**: Interactive charts and maps
- **Multi-location Support**: Predictions for different cities
- **Alert System**: Push notifications for poor air quality

## 📚 Technologies Used

### **Frontend**
- **React 18** with TypeScript
- **Vite** for build tooling
- **shadcn/ui** component library
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **TanStack Query** for state management

### **Backend**
- **FastAPI** for REST API
- **Scikit-learn** for machine learning
- **Pandas & NumPy** for data processing
- **Gradient Boosting** for predictions
- **Joblib** for model persistence
- **Uvicorn** as ASGI server

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Sky Forecast Hub** - Predicting air quality for a healthier tomorrow 🌤️
