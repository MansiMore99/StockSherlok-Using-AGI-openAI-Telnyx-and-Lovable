"""
Basic tests for the StockSherlok API
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app


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


if __name__ == '__main__':
    unittest.main()
