# Sky Forecast Hub 🌤️

**Advanced Air Quality Prediction System using Machine Learning**

[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-blue.svg)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.5-orange.svg)](https://scikit-learn.org/)

## 🎯 Project Overview

Sky Forecast Hub is a comprehensive air quality prediction system that combines modern web technologies with advanced machine learning algorithms to provide accurate AQI (Air Quality Index) predictions. The system offers **two prediction modes**: manual input-based predictions and date-based seasonal predictions.

### ✨ Key Features

- 🔬 **Dual Prediction Modes**: Manual input + Date-based predictions
- 🤖 **Enhanced ML Model**: 94% cross-validation accuracy with Gradient Boosting
- 📊 **Intelligent Analysis**: AI-powered explanations for every prediction
- 🎨 **Modern UI**: Responsive design with real-time updates
- 🌍 **Seasonal Intelligence**: Understanding of environmental patterns

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v18 or higher)
- **Python 3.8+**
- **npm** or **yarn**

### Installation & Setup

#### Option 1: Automated Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd sky-forecast-hub-main

# Run automated setup
./setup.sh
```

#### Option 2: Manual Setup

**Frontend:**
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

**Backend:**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application
- **Frontend**: http://localhost:8081
- **Backend API**: http://127.0.0.1:8000
- **API Documentation**: http://127.0.0.1:8000/docs

## 🔧 Technical Architecture

### Frontend Stack
- **React 18** + **TypeScript** + **Vite**
- **shadcn/ui** component library
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **TanStack Query** for state management

### Backend Stack
- **FastAPI** for REST API
- **Scikit-learn** for machine learning
- **Gradient Boosting** algorithm
- **Pandas & NumPy** for data processing
- **Joblib** for model persistence

### ML Model Performance
- **Cross-Validation R²**: 0.940
- **Test R² Score**: 0.994
- **Test RMSE**: 1.37
- **Test MAE**: 0.47
- **Features**: 8 engineered features

## 📊 API Endpoints

### Manual Prediction
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

### Date-Based Prediction
```http
POST /predict-by-date
Content-Type: application/json

{
  "date": "2024-06-15"
}
```

## 🧪 Testing

```bash
cd backend
source venv/bin/activate

# Test API endpoints
python test_api.py
python test_date_api.py

# Compare model performance
python model_comparison.py
```

## 📈 Model Improvements

| Metric | Original | Enhanced | Improvement |
|--------|----------|----------|-------------|
| Cross-Validation R² | ~0.8 | **0.940** | +17.5% |
| Test RMSE | ~5-10 | **1.37** | 70-85% reduction |
| Features | 7 basic | **8 engineered** | Better feature set |
| Validation | Basic split | **Time series CV** | More realistic |

## 🎯 AQI Categories

| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| **0-50** | Good | Air quality is satisfactory |
| **51-100** | Moderate | Acceptable for most people |
| **101-200** | Poor | Sensitive groups may experience health effects |
| **201-300** | Very Poor | Health alert for everyone |
| **300+** | Hazardous | Emergency conditions |

## 🔮 Future Enhancements

- Real-time weather API integration
- Mobile application (React Native)
- User authentication and prediction history
- Multi-location support
- Advanced visualizations and alerts

## 📚 Project Structure

```
sky-forecast-hub/
├── src/                    # Frontend React app
│   ├── components/         # UI components
│   ├── pages/             # Page components
│   └── hooks/             # Custom hooks
├── backend/               # Python FastAPI backend
│   ├── main.py           # API application
│   ├── realistic_model_training.py # Model training
│   ├── enhanced_aqi_model.pkl # Trained model
│   └── requirements.txt  # Dependencies
├── setup.sh             # Automated setup script
└── README.md           # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---

**Sky Forecast Hub** - Predicting air quality for a healthier tomorrow 🌤️