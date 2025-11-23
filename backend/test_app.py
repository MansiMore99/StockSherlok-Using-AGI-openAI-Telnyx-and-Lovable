"""
Basic tests for the StockSherlok API
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import pandas as pd
import numpy as np

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from metrics_engine import compute_metrics, _compute_price_metrics, _compute_fundamental_metrics, _compute_growth_score


class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('service', data)
    
    @patch('research_agent.ResearchAgent.analyze_company')
    def test_analyze_endpoint(self, mock_analyze):
        """Test analyze endpoint"""
        mock_analyze.return_value = {
            'ticker': 'TEST',
            'analysis': 'Test analysis'
        }
        
        response = self.client.post('/api/analyze', json={
            'ticker': 'TEST'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['ticker'], 'TEST')
    
    def test_analyze_missing_ticker(self):
        """Test analyze endpoint with missing ticker"""
        response = self.client.post('/api/analyze', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    @patch('research_agent.ResearchAgent.scan_market_signals')
    def test_scan_endpoint(self, mock_scan):
        """Test scan endpoint"""
        mock_scan.return_value = {
            'sector': 'technology',
            'signals': []
        }
        
        response = self.client.post('/api/scan', json={
            'sector': 'technology'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
    
    @patch('research_agent.ResearchAgent.get_actionable_insights')
    def test_insights_endpoint(self, mock_insights):
        """Test insights endpoint"""
        mock_insights.return_value = {
            'ticker': 'TEST',
            'insights': 'Test insights'
        }
        
        response = self.client.post('/api/insights', json={
            'ticker': 'TEST'
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])


class TestResearchAgent(unittest.TestCase):
    """Test Research Agent functionality"""
    
    @patch('yfinance.Ticker')
    def test_get_stock_data(self, mock_ticker):
        """Test stock data fetching"""
        from research_agent import ResearchAgent
        
        # Mock yfinance response
        mock_stock = MagicMock()
        mock_stock.info = {
            'currentPrice': 100.0,
            'marketCap': 1000000000,
            'sector': 'Technology'
        }
        mock_stock.history.return_value = MagicMock()
        mock_ticker.return_value = mock_stock
        
        agent = ResearchAgent('fake-api-key')
        data = agent._get_stock_data('TEST')
        
        self.assertIn('current_price', data)
        self.assertIn('sector', data)


class TestMetricsEngine(unittest.TestCase):
    """Test metrics computation"""
    
    def test_compute_price_metrics_with_data(self):
        """Test price metrics computation with valid data"""
        # Create mock price history
        dates = pd.date_range(start='2023-01-01', periods=150, freq='D')
        prices = np.linspace(100, 120, 150) + np.random.randn(150) * 2
        price_history = pd.DataFrame({'Close': prices}, index=dates)
        
        metrics = _compute_price_metrics(price_history)
        
        # Check that metrics exist
        self.assertIn('weekly_change', metrics)
        self.assertIn('monthly_change', metrics)
        self.assertIn('six_month_trend_slope', metrics)
        self.assertIn('volatility', metrics)
        
        # Check that values are numeric
        self.assertIsInstance(metrics['weekly_change'], (int, float))
        self.assertIsInstance(metrics['volatility'], (int, float))
    
    def test_compute_price_metrics_insufficient_data(self):
        """Test price metrics with insufficient data"""
        # Create very short price history
        dates = pd.date_range(start='2023-01-01', periods=3, freq='D')
        prices = [100, 101, 102]
        price_history = pd.DataFrame({'Close': prices}, index=dates)
        
        metrics = _compute_price_metrics(price_history)
        
        # Should return zeros for metrics that need more data
        self.assertEqual(metrics['weekly_change'], 0.0)
        self.assertEqual(metrics['monthly_change'], 0.0)
    
    def test_compute_fundamental_metrics(self):
        """Test fundamental metrics computation"""
        fundamentals = {
            'revenue_growth': 0.25,
            'market_cap': 5000000000,
            'avg_volume': 1000000
        }
        
        metrics = _compute_fundamental_metrics(fundamentals)
        
        self.assertIn('revenue_growth_yoy', metrics)
        self.assertIn('market_cap', metrics)
        self.assertIn('avg_volume_30d', metrics)
        self.assertEqual(metrics['revenue_growth_yoy'], 0.25)
        self.assertEqual(metrics['market_cap'], 5000000000)
    
    def test_compute_growth_score(self):
        """Test growth score computation"""
        metrics = {
            'weekly_change': 5.0,
            'monthly_change': 15.0,
            'revenue_growth_yoy': 0.3,
            'six_month_trend_slope': 0.5,
            'volatility': 0.02
        }
        
        score = _compute_growth_score(metrics)
        
        # Score should be between 0 and 10
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 10)
        self.assertIsInstance(score, float)
    
    def test_compute_metrics_full(self):
        """Test complete metrics computation"""
        # Create mock price history
        dates = pd.date_range(start='2023-01-01', periods=150, freq='D')
        prices = np.linspace(100, 120, 150)
        price_history = pd.DataFrame({'Close': prices}, index=dates)
        
        fundamentals = {
            'revenue_growth': 0.25,
            'market_cap': 5000000000,
            'avg_volume': 1000000
        }
        
        metrics = compute_metrics(price_history, fundamentals)
        
        # Check all expected metrics are present
        expected_keys = [
            'weekly_change', 'monthly_change', 'six_month_trend_slope',
            'volatility', 'revenue_growth_yoy', 'market_cap',
            'avg_volume_30d', 'growth_score'
        ]
        
        for key in expected_keys:
            self.assertIn(key, metrics)
    
    def test_compute_metrics_with_none_price_history(self):
        """Test metrics computation with no price history"""
        fundamentals = {
            'revenue_growth': 0.25,
            'market_cap': 5000000000
        }
        
        metrics = compute_metrics(None, fundamentals)
        
        # Should have default values for price metrics
        self.assertEqual(metrics['weekly_change'], 0.0)
        self.assertEqual(metrics['monthly_change'], 0.0)
        self.assertIn('growth_score', metrics)


if __name__ == '__main__':
    unittest.main()
