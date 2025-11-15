#!/bin/bash

# Setup script for AQI Time-Series Forecasting
# This script installs dependencies and trains the SARIMAX model

echo "=========================================="
echo "AQI TIME-SERIES FORECASTING SETUP"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Dependencies installed successfully!"

# Check if data file exists
if [ ! -f "aqidaily_fiveyears.csv" ]; then
    echo "❌ Error: aqidaily_fiveyears.csv not found!"
    echo "Please ensure the data file is in the backend directory."
    exit 1
fi

echo "✅ Data file found: aqidaily_fiveyears.csv"

# Train the SARIMAX model
echo ""
echo "Training SARIMAX time-series model..."
echo "This may take several minutes..."

python model_training.py train

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Model training completed successfully!"
    echo ""
    echo "Testing the trained model..."
    python model_training.py test
    
    echo ""
    echo "=========================================="
    echo "SETUP COMPLETED SUCCESSFULLY!"
    echo "=========================================="
    echo ""
    echo "You can now start the API server with:"
    echo "  uvicorn main:app --reload"
    echo ""
    echo "Or test the API with:"
    echo "  python test_forecasting.py"
    echo ""
else
    echo ""
    echo "❌ Model training failed!"
    echo "Please check the error messages above."
    exit 1
fi
