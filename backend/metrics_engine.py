"""
Metrics Engine - Advanced financial metrics computation
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional


def compute_metrics(price_history: pd.DataFrame, fundamentals: Dict) -> Dict:
    """
    Compute advanced metrics for a stock
    
    Args:
        price_history: pandas DataFrame with Date index and 'Close' column
        fundamentals: dict with revenue, market_cap, volume, etc.
        
    Returns:
        dict of computed metrics including price-based, fundamental, and composite scores
    """
    metrics = {}
    
    # Price-Based Metrics
    if price_history is not None and len(price_history) > 0:
        metrics.update(_compute_price_metrics(price_history))
    else:
        # Default values if no price history
        metrics.update({
            'weekly_change': 0.0,
            'monthly_change': 0.0,
            'six_month_trend_slope': 0.0,
            'volatility': 0.0
        })
    
    # Fundamental Metrics
    metrics.update(_compute_fundamental_metrics(fundamentals))
    
    # Composite Growth Score
    metrics['growth_score'] = _compute_growth_score(metrics)
    
    return metrics


def _compute_price_metrics(price_history: pd.DataFrame) -> Dict:
    """Compute price-based metrics from historical data"""
    metrics = {}
    
    try:
        prices = price_history['Close'].values
        
        # Weekly change (last 7 days)
        if len(prices) >= 7:
            weekly_change = ((prices[-1] - prices[-7]) / prices[-7]) * 100
            metrics['weekly_change'] = round(weekly_change, 2)
        else:
            metrics['weekly_change'] = 0.0
        
        # Monthly change (last 30 days)
        if len(prices) >= 30:
            monthly_change = ((prices[-1] - prices[-30]) / prices[-30]) * 100
            metrics['monthly_change'] = round(monthly_change, 2)
        else:
            metrics['monthly_change'] = 0.0
        
        # Six-month trend slope (linear regression)
        if len(prices) >= 120:  # ~6 months of trading days
            x = np.arange(len(prices[-120:]))
            y = prices[-120:]
            slope = np.polyfit(x, y, 1)[0]
            metrics['six_month_trend_slope'] = round(slope, 4)
        else:
            metrics['six_month_trend_slope'] = 0.0
        
        # Volatility (standard deviation of returns)
        if len(prices) >= 2:
            returns = np.diff(prices) / prices[:-1]
            volatility = np.std(returns)
            metrics['volatility'] = round(volatility, 4)
        else:
            metrics['volatility'] = 0.0
            
    except Exception as e:
        # If computation fails, return zeros
        metrics.update({
            'weekly_change': 0.0,
            'monthly_change': 0.0,
            'six_month_trend_slope': 0.0,
            'volatility': 0.0
        })
    
    return metrics


def _compute_fundamental_metrics(fundamentals: Dict) -> Dict:
    """Compute fundamental metrics"""
    metrics = {}
    
    # Revenue growth year-over-year
    revenue_growth = fundamentals.get('revenue_growth', 0.0)
    if isinstance(revenue_growth, (int, float)):
        metrics['revenue_growth_yoy'] = round(revenue_growth, 4)
    else:
        metrics['revenue_growth_yoy'] = 0.0
    
    # Market cap (already available)
    metrics['market_cap'] = fundamentals.get('market_cap', 0)
    
    # Average volume (if available)
    avg_volume = fundamentals.get('avg_volume', 0)
    metrics['avg_volume_30d'] = avg_volume
    
    return metrics


def _compute_growth_score(metrics: Dict) -> float:
    """
    Compute composite growth score
    
    Weighted average of normalized metrics:
    - 25% weekly change
    - 25% monthly change
    - 25% revenue growth
    - 15% trend slope
    - 10% inverse volatility
    
    Score is on a 0-10 scale
    """
    # Simple min-max normalization (not perfect but works for comparison)
    def normalize(value, min_val, max_val):
        """Normalize value to 0-1 range"""
        if max_val == min_val:
            return 0.5
        normalized = (value - min_val) / (max_val - min_val)
        return max(0, min(1, normalized))
    
    # Define reasonable ranges for normalization
    weekly_norm = normalize(metrics.get('weekly_change', 0), -20, 20)
    monthly_norm = normalize(metrics.get('monthly_change', 0), -50, 50)
    revenue_norm = normalize(metrics.get('revenue_growth_yoy', 0), -0.5, 1.0)
    trend_norm = normalize(metrics.get('six_month_trend_slope', 0), -1, 1)
    
    # Inverse volatility (lower volatility is better)
    volatility = metrics.get('volatility', 0)
    if volatility > 0:
        vol_norm = 1 - normalize(volatility, 0, 0.1)
    else:
        vol_norm = 0.5
    
    # Weighted composite score
    growth_score = (
        0.25 * weekly_norm +
        0.25 * monthly_norm +
        0.25 * revenue_norm +
        0.15 * trend_norm +
        0.10 * vol_norm
    )
    
    # Scale to 0-10
    return round(growth_score * 10, 2)
