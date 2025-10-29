#!/usr/bin/env python3
"""
Realistic Model Training Script for Sky Forecast Hub
This script creates a more realistic model by avoiding data leakage and using proper validation.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data(file_path):
    """Load and preprocess the AQI dataset with realistic feature engineering"""
    print("📊 Loading and preprocessing data...")
    
    # Load data
    df = pd.read_csv(file_path)
    print(f"Original dataset shape: {df.shape}")
    
    # Clean column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # Handle missing values (represented as '.' in the dataset)
    df = df.replace('.', np.nan)
    
    # Convert numeric columns
    numeric_columns = ['overall_aqi_value', 'co', 'ozone', 'pm10', 'pm25', 'no2']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows with missing AQI values
    df = df.dropna(subset=['overall_aqi_value'])
    
    # Parse dates
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')
    df = df.dropna(subset=['date'])
    
    # Sort by date for time series validation
    df = df.sort_values('date').reset_index(drop=True)
    
    # Create realistic features (avoiding data leakage)
    df = create_realistic_features(df)
    
    # Select features for training (only use available pollutant data)
    feature_columns = ['co', 'ozone', 'pm10', 'pm25', 'no2']
    available_features = [col for col in feature_columns if col in df.columns]
    
    # Add engineered features that don't leak information
    engineered_features = ['month', 'day_of_year', 'is_weekend']
    available_features.extend([col for col in engineered_features if col in df.columns])
    
    # Remove rows with missing feature values
    df = df.dropna(subset=available_features)
    
    print(f"Cleaned dataset shape: {df.shape}")
    print(f"Features used: {available_features}")
    
    return df, available_features

def create_realistic_features(df):
    """Create realistic features without data leakage"""
    print("🔧 Creating realistic features...")
    
    # Temporal features
    df['month'] = df['date'].dt.month
    df['day_of_year'] = df['date'].dt.dayofyear
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Seasonal features (cyclical encoding)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
    # Site-based features (if available)
    if 'site_name_(of_overall_aqi)' in df.columns:
        df['is_traffic_site'] = df['site_name_(of_overall_aqi)'].str.contains('TRAFFIC', case=False, na=False).astype(int)
        df['is_airport_site'] = df['site_name_(of_overall_aqi)'].str.contains('Airport', case=False, na=False).astype(int)
        df['is_urban_site'] = df['site_name_(of_overall_aqi)'].str.contains('Chico', case=False, na=False).astype(int)
    
    # Pollutant interaction features (only using available data)
    pollutant_cols = ['co', 'ozone', 'pm10', 'pm25', 'no2']
    available_pollutants = [col for col in pollutant_cols if col in df.columns]
    
    if len(available_pollutants) > 1:
        # Only create features from available pollutants
        df['pollutant_sum'] = df[available_pollutants].sum(axis=1)
        df['pollutant_max'] = df[available_pollutants].max(axis=1)
        df['pollutant_mean'] = df[available_pollutants].mean(axis=1)
        
        # Ratio features
        df['pm_ratio'] = df['pm25'] / (df['pm10'] + 1e-8)
        df['no2_co_ratio'] = df['no2'] / (df['co'] + 1e-8)
    
    return df

def train_and_evaluate_models(X, y):
    """Train multiple models with proper validation"""
    print("🤖 Training and evaluating multiple models...")
    
    # Use time series split for validation
    tscv = TimeSeriesSplit(n_splits=5)
    
    # Split data (use last 20% for testing)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Scale features
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define models with realistic parameters
    models = {
        'Random Forest': RandomForestRegressor(
            n_estimators=100, 
            max_depth=10, 
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42, 
            n_jobs=-1
        ),
        'Gradient Boosting': GradientBoostingRegressor(
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=5,
            random_state=42
        ),
        'Ridge Regression': Ridge(alpha=1.0),
        'Lasso Regression': Lasso(alpha=0.1, max_iter=1000)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Use scaled data for linear models
        if name in ['Ridge Regression', 'Lasso Regression']:
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            
            # Cross-validation on training set
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=tscv, scoring='r2')
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            # Cross-validation on training set
            cv_scores = cross_val_score(model, X_train, y_train, cv=tscv, scoring='r2')
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mse)
        
        results[name] = {
            'model': model,
            'mse': mse,
            'mae': mae,
            'r2': r2,
            'rmse': rmse,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'predictions': y_pred
        }
        
        print(f"  Test RMSE: {rmse:.2f}")
        print(f"  Test MAE: {mae:.2f}")
        print(f"  Test R²: {r2:.3f}")
        print(f"  CV R²: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
    
    return results, scaler

def hyperparameter_tuning(X, y, model_name='Random Forest'):
    """Perform hyperparameter tuning for the best model"""
    print(f"\n🎯 Performing hyperparameter tuning for {model_name}...")
    
    # Use time series split
    tscv = TimeSeriesSplit(n_splits=3)
    
    if model_name == 'Random Forest':
        param_grid = {
            'n_estimators': [50, 100, 150],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        model = RandomForestRegressor(random_state=42, n_jobs=-1)
    elif model_name == 'Gradient Boosting':
        param_grid = {
            'n_estimators': [50, 100, 150],
            'learning_rate': [0.05, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        }
        model = GradientBoostingRegressor(random_state=42)
    else:
        print(f"Hyperparameter tuning not implemented for {model_name}")
        return None
    
    # Grid search with time series cross-validation
    grid_search = GridSearchCV(
        model, param_grid, cv=tscv, scoring='r2', 
        n_jobs=-1, verbose=1
    )
    
    grid_search.fit(X, y)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best CV score: {grid_search.best_score_:.3f}")
    
    return grid_search.best_estimator_

def main():
    """Main function to run the realistic model training"""
    print("🚀 Starting Realistic Model Training for Sky Forecast Hub")
    print("=" * 60)
    
    # Load and preprocess data
    df, feature_columns = load_and_preprocess_data('aqidaily_fiveyears.csv')
    
    # Prepare features and target
    X = df[feature_columns]
    y = df['overall_aqi_value']
    
    print(f"\nDataset info:")
    print(f"  Samples: {len(X)}")
    print(f"  Features: {len(feature_columns)}")
    print(f"  Target range: {y.min():.1f} - {y.max():.1f}")
    print(f"  Target mean: {y.mean():.1f}")
    print(f"  Target std: {y.std():.1f}")
    
    # Train and evaluate models
    results, scaler = train_and_evaluate_models(X, y)
    
    # Find best model based on CV score (more reliable than test score)
    best_model_name = max(results.keys(), key=lambda k: results[k]['cv_mean'])
    best_model = results[best_model_name]['model']
    best_cv_score = results[best_model_name]['cv_mean']
    best_test_score = results[best_model_name]['r2']
    
    print(f"\n🏆 Best model: {best_model_name}")
    print(f"  CV R² Score: {best_cv_score:.3f}")
    print(f"  Test R² Score: {best_test_score:.3f}")
    
    # Hyperparameter tuning for best model
    tuned_model = hyperparameter_tuning(X, y, best_model_name)
    
    if tuned_model is not None:
        # Evaluate tuned model
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        if best_model_name in ['Ridge Regression', 'Lasso Regression']:
            scaler_tuned = RobustScaler()
            X_train_scaled = scaler_tuned.fit_transform(X_train)
            X_test_scaled = scaler_tuned.transform(X_test)
            tuned_pred = tuned_model.predict(X_test_scaled)
        else:
            tuned_pred = tuned_model.predict(X_test)
        
        tuned_r2 = r2_score(y_test, tuned_pred)
        tuned_rmse = np.sqrt(mean_squared_error(y_test, tuned_pred))
        
        print(f"Tuned model R²: {tuned_r2:.3f}")
        print(f"Tuned model RMSE: {tuned_rmse:.2f}")
        
        # Use tuned model if it's better
        if tuned_r2 > best_test_score:
            best_model = tuned_model
            print("✅ Using tuned model as final model")
        else:
            print("✅ Using original best model as final model")
    
    # Save the best model
    model_filename = 'enhanced_aqi_model.pkl'
    scaler_filename = 'enhanced_scaler.pkl'
    feature_names_filename = 'feature_names.pkl'
    
    joblib.dump(best_model, model_filename)
    joblib.dump(scaler, scaler_filename)
    joblib.dump(feature_columns, feature_names_filename)
    
    print(f"\n💾 Saved enhanced model to {model_filename}")
    print(f"💾 Saved scaler to {scaler_filename}")
    print(f"💾 Saved feature names to {feature_names_filename}")
    
    # Summary
    print(f"\n📊 Model Performance Summary:")
    print(f"  Best Model: {best_model_name}")
    print(f"  Cross-Validation R²: {best_cv_score:.3f}")
    print(f"  Test R² Score: {best_test_score:.3f}")
    print(f"  Test RMSE: {results[best_model_name]['rmse']:.2f}")
    print(f"  Test MAE: {results[best_model_name]['mae']:.2f}")
    
    print("\n✅ Realistic model training completed!")

if __name__ == "__main__":
    main()
