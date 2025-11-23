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


class TestChartGenerator(unittest.TestCase):
    """Test chart generation functionality"""
    
    def test_generate_bar_chart(self):
        """Test basic bar chart generation"""
        from chart_generator import generate_bar_chart
        
        labels = ['PLTR', 'CRWD', 'NET']
        values = [5.2, 8.1, 6.5]
        
        result = generate_bar_chart(
            title="Test Chart",
            labels=labels,
            values=values,
            ylabel="Test Metric"
        )
        
        # Check structure
        self.assertIn('chart_type', result)
        self.assertIn('title', result)
        self.assertIn('image_base64', result)
        
        # Check values
        self.assertEqual(result['chart_type'], 'bar')
        self.assertEqual(result['title'], 'Test Chart')
        
        # Check that base64 image was generated (should be non-empty string)
        if 'error' not in result:
            self.assertIsInstance(result['image_base64'], str)
            self.assertGreater(len(result['image_base64']), 0)
    
    def test_generate_bar_chart_empty_data(self):
        """Test bar chart generation with empty data"""
        from chart_generator import generate_bar_chart
        
        result = generate_bar_chart(
            title="Empty Chart",
            labels=[],
            values=[],
            ylabel="Test"
        )
        
        # Should return error structure
        self.assertIn('error', result)
        self.assertEqual(result['image_base64'], '')
    
    def test_create_comparison_charts(self):
        """Test creating comparison charts for multiple companies"""
        from research_agent import ResearchAgent
        
        # Create fake results
        fake_results = [
            {
                'ticker': 'PLTR',
                'stock_data': {'market_cap': 5000000000},
                'metrics': {
                    'monthly_change': 4.2,
                    'revenue_growth_yoy': 0.30
                }
            },
            {
                'ticker': 'CRWD',
                'stock_data': {'market_cap': 8000000000},
                'metrics': {
                    'monthly_change': 12.1,
                    'revenue_growth_yoy': 0.45
                }
            },
            {
                'ticker': 'NET',
                'stock_data': {'market_cap': 6000000000},
                'metrics': {
                    'monthly_change': 8.5,
                    'revenue_growth_yoy': 0.35
                }
            }
        ]
        
        agent = ResearchAgent('fake-api-key')
        charts = agent.create_comparison_charts(fake_results)
        
        # Should return exactly 3 charts
        self.assertIsInstance(charts, list)
        self.assertGreaterEqual(len(charts), 3)
        
        # Each chart should have required fields
        for chart in charts:
            self.assertIn('chart_type', chart)
            self.assertIn('metric', chart)
            self.assertIn('image_base64', chart)
            
            # If no error, should have base64 string
            if 'error' not in chart:
                self.assertIsInstance(chart['image_base64'], str)


if __name__ == '__main__':
    unittest.main()
