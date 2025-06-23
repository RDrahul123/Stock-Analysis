import re
import pandas as pd
import numpy as np
from datetime import datetime

def validate_symbol(symbol):
    """
    Validate stock symbol format
    
    Args:
        symbol (str): Stock ticker symbol
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not symbol or not isinstance(symbol, str):
        return False
    
    # Remove whitespace and convert to uppercase
    symbol = symbol.strip().upper()
    
    # Basic validation - alphanumeric characters, dots, and hyphens allowed
    # Length between 1-5 characters typically
    pattern = r'^[A-Z]{1,5}(\.[A-Z]{1,2})?$'
    
    return bool(re.match(pattern, symbol)) and len(symbol) >= 1

def format_currency(value, currency="USD"):
    """
    Format numeric value as currency
    
    Args:
        value (float): Numeric value
        currency (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    if value is None or pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
        if abs(value) >= 1e9:
            return f"${value/1e9:.2f}B"
        elif abs(value) >= 1e6:
            return f"${value/1e6:.2f}M"
        elif abs(value) >= 1e3:
            return f"${value/1e3:.2f}K"
        else:
            return f"${value:.2f}"
    except (ValueError, TypeError):
        return "N/A"

def format_percentage(value, decimal_places=2):
    """
    Format numeric value as percentage
    
    Args:
        value (float): Numeric value
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted percentage string
    """
    if value is None or pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
        formatted = f"{value:.{decimal_places}f}%"
        return formatted
    except (ValueError, TypeError):
        return "N/A"

def format_large_number(value):
    """
    Format large numbers with appropriate suffixes
    
    Args:
        value (float): Numeric value
        
    Returns:
        str: Formatted number string
    """
    if value is None or pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
        if abs(value) >= 1e12:
            return f"{value/1e12:.2f}T"
        elif abs(value) >= 1e9:
            return f"{value/1e9:.2f}B"
        elif abs(value) >= 1e6:
            return f"{value/1e6:.2f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.2f}K"
        else:
            return f"{value:.0f}"
    except (ValueError, TypeError):
        return "N/A"

def calculate_returns(prices):
    """
    Calculate returns from price series
    
    Args:
        prices (pd.Series): Price series
        
    Returns:
        pd.Series: Returns series
    """
    if prices.empty:
        return pd.Series()
    
    return prices.pct_change().dropna()

def calculate_volatility(returns, periods=252):
    """
    Calculate annualized volatility from returns
    
    Args:
        returns (pd.Series): Returns series
        periods (int): Number of periods in a year (252 for daily)
        
    Returns:
        float: Annualized volatility
    """
    if returns.empty:
        return np.nan
    
    return returns.std() * np.sqrt(periods)

def calculate_sharpe_ratio(returns, risk_free_rate=0.02, periods=252):
    """
    Calculate Sharpe ratio
    
    Args:
        returns (pd.Series): Returns series
        risk_free_rate (float): Risk-free rate (annual)
        periods (int): Number of periods in a year
        
    Returns:
        float: Sharpe ratio
    """
    if returns.empty:
        return np.nan
    
    excess_returns = returns - (risk_free_rate / periods)
    return excess_returns.mean() / returns.std() * np.sqrt(periods)

def calculate_max_drawdown(prices):
    """
    Calculate maximum drawdown
    
    Args:
        prices (pd.Series): Price series
        
    Returns:
        float: Maximum drawdown as percentage
    """
    if prices.empty:
        return np.nan
    
    # Calculate running maximum
    running_max = prices.expanding().max()
    
    # Calculate drawdown
    drawdown = (prices - running_max) / running_max
    
    return drawdown.min()

def get_trading_days_in_period(start_date, end_date):
    """
    Get number of trading days between two dates
    
    Args:
        start_date (datetime): Start date
        end_date (datetime): End date
        
    Returns:
        int: Number of trading days
    """
    # Simple approximation - can be enhanced with actual trading calendar
    total_days = (end_date - start_date).days
    weekdays = total_days * (5/7)  # Approximate weekdays
    return int(weekdays * 0.95)  # Account for holidays

def clean_financial_data(data):
    """
    Clean and format financial data
    
    Args:
        data (dict): Raw financial data
        
    Returns:
        dict: Cleaned financial data
    """
    cleaned = {}
    
    for key, value in data.items():
        if isinstance(value, (int, float)):
            if pd.isna(value) or np.isinf(value):
                cleaned[key] = None
            else:
                cleaned[key] = value
        else:
            cleaned[key] = value
    
    return cleaned

def determine_trend(prices, window=20):
    """
    Determine price trend based on moving average
    
    Args:
        prices (pd.Series): Price series
        window (int): Moving average window
        
    Returns:
        str: Trend direction ('Upward', 'Downward', 'Sideways')
    """
    if len(prices) < window:
        return "Insufficient Data"
    
    ma = prices.rolling(window=window).mean()
    current_ma = ma.iloc[-1]
    previous_ma = ma.iloc[-window//2]
    
    if pd.isna(current_ma) or pd.isna(previous_ma):
        return "Insufficient Data"
    
    change_pct = (current_ma - previous_ma) / previous_ma * 100
    
    if change_pct > 2:
        return "Upward"
    elif change_pct < -2:
        return "Downward"
    else:
        return "Sideways"

def format_date_range(start_date, end_date):
    """
    Format date range for display
    
    Args:
        start_date (datetime): Start date
        end_date (datetime): End date
        
    Returns:
        str: Formatted date range
    """
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    return f"{start_str} to {end_str}"

def validate_date_range(start_date, end_date):
    """
    Validate date range
    
    Args:
        start_date (datetime): Start date
        end_date (datetime): End date
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
        return False
    
    return start_date < end_date and end_date <= datetime.now()
