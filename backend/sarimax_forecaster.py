"""
SARIMAX time-series forecasting model for AQI prediction.
Handles seasonality, trends, and exogenous variables.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
import matplotlib.pyplot as plt
import warnings
from typing import Tuple, Optional, Dict, Any
import joblib
from datetime import datetime, timedelta
import itertools

warnings.filterwarnings('ignore')

class AQISARIMAXForecaster:
    """SARIMAX model for AQI time-series forecasting."""
    
    def __init__(self, order: Tuple[int, int, int] = (1, 1, 1), 
                 seasonal_order: Tuple[int, int, int, int] = (1, 1, 1, 12)):
        """
        Initialize SARIMAX forecaster.
        
        Args:
            order (tuple): (p, d, q) parameters for ARIMA
            seasonal_order (tuple): (P, D, Q, s) parameters for seasonal component
        """
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.fitted_model = None
        self.training_data = None
        self.exogenous_data = None
        self.is_fitted = False
        
    def find_best_parameters(self, ts_data: pd.Series, exog_data: pd.DataFrame = None,
                           max_p: int = 3, max_d: int = 2, max_q: int = 3,
                           max_P: int = 2, max_D: int = 1, max_Q: int = 2,
                           seasonal_periods: int = 12) -> Tuple[Tuple, Tuple]:
        """
        Find the best SARIMAX parameters using grid search.
        
        Args:
            ts_data (pd.Series): Time series data
            exog_data (pd.DataFrame): Exogenous variables
            max_p, max_d, max_q: Maximum values for ARIMA parameters
            max_P, max_D, max_Q: Maximum values for seasonal parameters
            seasonal_periods (int): Seasonal period
            
        Returns:
            tuple: Best (order, seasonal_order) parameters
        """
        print("Searching for best SARIMAX parameters...")
        
        # Generate parameter combinations
        p_values = range(0, max_p + 1)
        d_values = range(0, max_d + 1)
        q_values = range(0, max_q + 1)
        P_values = range(0, max_P + 1)
        D_values = range(0, max_D + 1)
        Q_values = range(0, max_Q + 1)
        
        best_aic = float('inf')
        best_params = None
        
        param_combinations = list(itertools.product(p_values, d_values, q_values, 
                                                  P_values, D_values, Q_values))
        
        print(f"Testing {len(param_combinations)} parameter combinations...")
        
        for i, (p, d, q, P, D, Q) in enumerate(param_combinations):
            try:
                order = (p, d, q)
                seasonal_order = (P, D, Q, seasonal_periods)
                
                model = SARIMAX(ts_data, exog=exog_data, order=order, 
                              seasonal_order=seasonal_order, enforce_stationarity=False,
                              enforce_invertibility=False)
                fitted_model = model.fit(disp=False, maxiter=50)
                
                if fitted_model.aic < best_aic:
                    best_aic = fitted_model.aic
                    best_params = (order, seasonal_order)
                    
                if (i + 1) % 50 == 0:
                    print(f"Processed {i + 1}/{len(param_combinations)} combinations...")
                    
            except Exception as e:
                continue
        
        print(f"Best AIC: {best_aic:.2f}")
        print(f"Best parameters: order={best_params[0]}, seasonal_order={best_params[1]}")
        
        return best_params
    
    def fit(self, ts_data: pd.Series, exog_data: pd.DataFrame = None,
            auto_parameters: bool = True) -> None:
        """
        Fit the SARIMAX model to the data.
        
        Args:
            ts_data (pd.Series): Time series data (AQI values)
            exog_data (pd.DataFrame): Exogenous variables
            auto_parameters (bool): Whether to automatically find best parameters
        """
        print("Fitting SARIMAX model...")
        
        self.training_data = ts_data.copy()
        self.exogenous_data = exog_data.copy() if exog_data is not None else None
        
        if auto_parameters:
            # Find best parameters
            best_order, best_seasonal_order = self.find_best_parameters(
                ts_data, exog_data, max_p=2, max_d=1, max_q=2,
                max_P=1, max_D=1, max_Q=1, seasonal_periods=12
            )
            self.order = best_order
            self.seasonal_order = best_seasonal_order
        
        # Create and fit the model
        self.model = SARIMAX(
            ts_data, 
            exog=exog_data,
            order=self.order,
            seasonal_order=self.seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        
        self.fitted_model = self.model.fit(disp=False, maxiter=200)
        self.is_fitted = True
        
        print(f"Model fitted successfully!")
        print(f"Order: {self.order}")
        print(f"Seasonal Order: {self.seasonal_order}")
        print(f"AIC: {self.fitted_model.aic:.2f}")
        print(f"BIC: {self.fitted_model.bic:.2f}")
    
    def forecast(self, steps: int, exog_future: pd.DataFrame = None,
                confidence_level: float = 0.95) -> Dict[str, Any]:
        """
        Generate forecasts for future periods.
        
        Args:
            steps (int): Number of steps to forecast
            exog_future (pd.DataFrame): Future exogenous variables
            confidence_level (float): Confidence level for prediction intervals
            
        Returns:
            dict: Forecast results with predictions and confidence intervals
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before forecasting")
        
        print(f"Generating {steps}-step forecast...")
        
        # Generate forecast
        forecast_result = self.fitted_model.get_forecast(steps=steps, exog=exog_future)
        
        # Extract predictions and confidence intervals
        forecast_mean = forecast_result.predicted_mean
        forecast_ci = forecast_result.conf_int(alpha=1-confidence_level)
        
        # Create forecast dates
        last_date = self.training_data.index[-1]
        forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=steps, freq='D')
        
        forecast_mean.index = forecast_dates
        forecast_ci.index = forecast_dates
        
        return {
            'forecast': forecast_mean,
            'lower_bound': forecast_ci.iloc[:, 0],
            'upper_bound': forecast_ci.iloc[:, 1],
            'confidence_level': confidence_level,
            'steps': steps
        }
    
    def predict_single_date(self, target_date: datetime, exog_values: pd.Series = None) -> float:
        """
        Predict AQI for a single future date.
        
        Args:
            target_date (datetime): Target date for prediction
            exog_values (pd.Series): Exogenous variable values for the target date
            
        Returns:
            float: Predicted AQI value
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        # Calculate steps from last training date
        last_date = self.training_data.index[-1]
        steps = (target_date - last_date).days
        
        if steps <= 0:
            raise ValueError("Target date must be in the future")
        
        # Prepare exogenous data for prediction
        if exog_values is not None and self.exogenous_data is not None:
            exog_future = pd.DataFrame([exog_values.values], 
                                     columns=self.exogenous_data.columns,
                                     index=[target_date])
        else:
            exog_future = None
        
        # Generate forecast
        forecast_result = self.forecast(steps=steps, exog_future=exog_future)
        
        # Return the prediction for the target date
        return float(forecast_result['forecast'].iloc[-1])
    
    def get_model_summary(self) -> str:
        """Get model summary statistics."""
        if not self.is_fitted:
            return "Model not fitted yet"
        
        return str(self.fitted_model.summary())
    
    def plot_diagnostics(self, figsize: Tuple[int, int] = (12, 8)) -> None:
        """Plot model diagnostics."""
        if not self.is_fitted:
            print("Model not fitted yet")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Residuals
        residuals = self.fitted_model.resid
        axes[0, 0].plot(residuals)
        axes[0, 0].set_title('Residuals')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Residuals')
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Q-Q Plot')
        
        # Histogram of residuals
        axes[1, 0].hist(residuals, bins=30, alpha=0.7)
        axes[1, 0].set_title('Histogram of Residuals')
        axes[1, 0].set_xlabel('Residuals')
        axes[1, 0].set_ylabel('Frequency')
        
        # ACF of residuals
        plot_acf(residuals, ax=axes[1, 1], lags=20)
        axes[1, 1].set_title('ACF of Residuals')
        
        plt.tight_layout()
        plt.show()
    
    def save_model(self, filepath: str) -> None:
        """Save the fitted model."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        model_data = {
            'fitted_model': self.fitted_model,
            'order': self.order,
            'seasonal_order': self.seasonal_order,
            'training_data': self.training_data,
            'exogenous_data': self.exogenous_data,
            'is_fitted': self.is_fitted
        }
        
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """Load a fitted model."""
        model_data = joblib.load(filepath)
        
        self.fitted_model = model_data['fitted_model']
        self.order = model_data['order']
        self.seasonal_order = model_data['seasonal_order']
        self.training_data = model_data['training_data']
        self.exogenous_data = model_data['exogenous_data']
        self.is_fitted = model_data['is_fitted']
        
        print(f"Model loaded from {filepath}")


def generate_future_exogenous_data(target_date: datetime, 
                                  historical_data: pd.DataFrame) -> pd.Series:
    """
    Generate exogenous variable values for future dates based on seasonal patterns.
    
    Args:
        target_date (datetime): Target date for prediction
        historical_data (pd.DataFrame): Historical data to extract patterns
        
    Returns:
        pd.Series: Exogenous variable values for the target date
    """
    # Extract seasonal patterns from historical data
    month = target_date.month
    day_of_year = target_date.timetuple().tm_yday
    is_weekend = 1 if target_date.weekday() >= 5 else 0
    
    # Calculate seasonal averages for pollutants
    seasonal_data = historical_data.groupby(historical_data.index.month).mean()
    
    # Get values for the target month
    co = seasonal_data.loc[month, 'co'] if 'co' in seasonal_data.columns else 3.0
    ozone = seasonal_data.loc[month, 'ozone'] if 'ozone' in seasonal_data.columns else 40.0
    pm10 = seasonal_data.loc[month, 'pm10'] if 'pm10' in seasonal_data.columns else 30.0
    pm25 = seasonal_data.loc[month, 'pm25'] if 'pm25' in seasonal_data.columns else 25.0
    no2 = seasonal_data.loc[month, 'no2'] if 'no2' in seasonal_data.columns else 20.0
    
    # Calculate derived features
    pm_ratio = pm25 / (pm10 + 1e-6)
    pollution_index = (pm25 + pm10 + no2) / 3
    
    # Create seasonal features
    sin_month = np.sin(2 * np.pi * month / 12)
    cos_month = np.cos(2 * np.pi * month / 12)
    sin_day = np.sin(2 * np.pi * day_of_year / 365)
    cos_day = np.cos(2 * np.pi * day_of_year / 365)
    
    # Create exogenous variables series
    exog_values = pd.Series({
        'co': co,
        'ozone': ozone,
        'pm10': pm10,
        'pm25': pm25,
        'no2': no2,
        'month': month,
        'day_of_year': day_of_year,
        'is_weekend': is_weekend,
        'sin_month': sin_month,
        'cos_month': cos_month,
        'sin_day': sin_day,
        'cos_day': cos_day,
        'pm_ratio': pm_ratio,
        'pollution_index': pollution_index
    })
    
    return exog_values


def main():
    """Test the SARIMAX forecaster."""
    from data_preprocessing import AQIDataPreprocessor
    
    # Load and preprocess data
    preprocessor = AQIDataPreprocessor('aqidaily_fiveyears.csv')
    processed_data = preprocessor.preprocess()
    
    # Get training data
    training_data = preprocessor.get_training_data()
    
    # Prepare time series and exogenous data
    ts_data = training_data['aqi']
    exog_data = preprocessor.get_exogenous_variables(training_data)
    
    # Initialize and fit SARIMAX model
    forecaster = AQISARIMAXForecaster()
    forecaster.fit(ts_data, exog_data, auto_parameters=True)
    
    # Test prediction for a future date
    future_date = datetime(2025, 4, 9)
    exog_future = generate_future_exogenous_data(future_date, training_data)
    prediction = forecaster.predict_single_date(future_date, exog_future)
    
    print(f"\nPrediction for {future_date.strftime('%Y-%m-%d')}: {prediction:.2f}")
    
    # Save model
    forecaster.save_model('aqi_sarimax_model.pkl')
    
    # Generate multi-step forecast
    forecast_result = forecaster.forecast(steps=30)
    print(f"\n30-day forecast mean: {forecast_result['forecast'].mean():.2f}")


if __name__ == "__main__":
    main()
