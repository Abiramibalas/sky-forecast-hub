#!/bin/bash

# Sky Forecast Hub - Automated Setup Script
# This script sets up both frontend and backend for the Sky Forecast Hub project

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting Sky Forecast Hub Setup..."
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js (v18 or higher) first."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is not installed. Please install pip3 first."
        exit 1
    fi
    
    print_success "All prerequisites are installed!"
}

# Setup Frontend
setup_frontend() {
    print_status "Setting up Frontend..."
    
    # Check if package.json exists
    if [ ! -f "package.json" ]; then
        print_error "package.json not found. Are you in the correct directory?"
        exit 1
    fi
    
    # Install dependencies
    print_status "Installing frontend dependencies..."
    npm install
    
    if [ $? -eq 0 ]; then
        print_success "Frontend dependencies installed successfully!"
    else
        print_error "Failed to install frontend dependencies."
        exit 1
    fi
}

# Setup Backend
setup_backend() {
    print_status "Setting up Backend..."
    
    # Create backend directory if it doesn't exist
    if [ ! -d "backend" ]; then
        print_error "Backend directory not found. Are you in the correct directory?"
        exit 1
    fi
    
    cd backend
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found in backend directory."
        exit 1
    fi
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created successfully!"
    else
        print_error "Failed to create virtual environment."
        exit 1
    fi
    
    # Activate virtual environment and install dependencies
    print_status "Installing backend dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Backend dependencies installed successfully!"
    else
        print_error "Failed to install backend dependencies."
        exit 1
    fi
    
    # Check if model files exist, if not, train the model
    if [ ! -f "enhanced_aqi_model.pkl" ] || [ ! -f "enhanced_scaler.pkl" ] || [ ! -f "feature_names.pkl" ]; then
        print_warning "Enhanced model files not found. Training model..."
        python realistic_model_training.py
        
        if [ $? -eq 0 ]; then
            print_success "Model trained successfully!"
        else
            print_warning "Model training failed, but continuing with setup..."
        fi
    else
        print_success "Enhanced model files found!"
    fi
    
    cd ..
}

# Test the setup
test_setup() {
    print_status "Testing the setup..."
    
    # Test backend
    cd backend
    source venv/bin/activate
    
    # Test if the API can start (quick test)
    print_status "Testing backend API..."
    timeout 10s python -c "
import sys
sys.path.append('.')
try:
    from main import app
    print('✅ Backend imports successfully')
except Exception as e:
    print(f'❌ Backend import failed: {e}')
    sys.exit(1)
" || print_warning "Backend test failed, but continuing..."
    
    cd ..
    
    # Test frontend
    print_status "Testing frontend..."
    if npm run build --silent > /dev/null 2>&1; then
        print_success "Frontend builds successfully!"
    else
        print_warning "Frontend build test failed, but continuing..."
    fi
}

# Main setup function
main() {
    echo ""
    print_status "Sky Forecast Hub Setup Starting..."
    echo ""
    
    # Check prerequisites
    check_prerequisites
    echo ""
    
    # Setup frontend
    setup_frontend
    echo ""
    
    # Setup backend
    setup_backend
    echo ""
    
    # Test setup
    test_setup
    echo ""
    
    # Success message
    print_success "🎉 Sky Forecast Hub setup completed successfully!"
    echo ""
    echo "📋 Next Steps:"
    echo "=============="
    echo ""
    echo "1. Start the Backend API (Terminal 1):"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    echo ""
    echo "2. Start the Frontend (Terminal 2):"
    echo "   npm run dev"
    echo ""
    echo "3. Open your browser:"
    echo "   Frontend: http://localhost:8080 (or the port shown by Vite)"
    echo "   Backend API: http://127.0.0.1:8000"
    echo "   API Documentation: http://127.0.0.1:8000/docs"
    echo ""
    echo "🧪 Test the API:"
    echo "   cd backend"
    echo "   source venv/bin/activate"
    echo "   python test_api.py"
    echo "   python test_date_api.py"
    echo ""
    echo "📚 Documentation:"
    echo "   README.md - Quick start guide"
    echo "   PROJECT_DOCUMENTATION.md - Comprehensive documentation"
    echo "   PRESENTATION_SCRIPT.md - Presentation guide"
    echo ""
    print_success "Happy coding! 🌤️"
}

# Run main function
main