import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [ticker, setTicker] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [signals, setSignals] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('analyze');
  const [sector, setSector] = useState('technology');

  const analyzeCompany = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setAnalysis(null);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, {
        ticker: ticker.toUpperCase(),
      });

      setAnalysis(response.data.analysis);
    } catch (err) {
      console.error('Error analyzing company:', err);
      setError(err.response?.data?.error || 'Failed to analyze company. Please check the ticker symbol and try again.');
    } finally {
      setLoading(false);
    }
  };

  const scanMarket = async () => {
    setLoading(true);
    setSignals(null);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/scan`, {
        sector: sector,
        market_cap: 'mid',
      });

      setSignals(response.data.signals);
    } catch (err) {
      console.error('Error scanning market:', err);
      setError(err.response?.data?.error || 'Failed to scan market signals.');
    } finally {
      setLoading(false);
    }
  };

  const getInsights = async () => {
    if (!ticker.trim()) {
      setError('Please enter a ticker symbol');
      return;
    }

    setLoading(true);
    setAnalysis(null);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/insights`, {
        ticker: ticker.toUpperCase(),
      });

      setAnalysis(response.data.insights);
    } catch (err) {
      console.error('Error getting insights:', err);
      setError(err.response?.data?.error || 'Failed to get insights. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="logo-container">
          <h1>🔍 StockSherlok</h1>
          <p className="tagline">AI-Powered Research Agent for Retail Investors</p>
        </div>
      </header>

      <main className="App-main">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'analyze' ? 'active' : ''}`}
            onClick={() => setActiveTab('analyze')}
          >
            Analyze Company
          </button>
          <button
            className={`tab ${activeTab === 'scan' ? 'active' : ''}`}
            onClick={() => setActiveTab('scan')}
          >
            Market Signals
          </button>
          <button
            className={`tab ${activeTab === 'insights' ? 'active' : ''}`}
            onClick={() => setActiveTab('insights')}
          >
            Get Insights
          </button>
        </div>

        {activeTab === 'analyze' && (
          <div className="tab-content">
            <div className="search-section">
              <h2>Analyze a Company</h2>
              <p className="description">
                Enter a ticker symbol to get comprehensive AI-powered analysis
              </p>
              <div className="input-group">
                <input
                  type="text"
                  placeholder="Enter ticker (e.g., AAPL, PLTR)"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && analyzeCompany()}
                  className="ticker-input"
                />
                <button onClick={analyzeCompany} disabled={loading} className="analyze-btn">
                  {loading ? 'Analyzing...' : 'Analyze'}
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'scan' && (
          <div className="tab-content">
            <div className="search-section">
              <h2>Scan Market Signals</h2>
              <p className="description">
                Discover promising mid-cap and early-stage tech companies
              </p>
              <div className="input-group">
                <select
                  value={sector}
                  onChange={(e) => setSector(e.target.value)}
                  className="sector-select"
                >
                  <option value="technology">Technology</option>
                  <option value="healthcare">Healthcare</option>
                  <option value="finance">Finance</option>
                </select>
                <button onClick={scanMarket} disabled={loading} className="analyze-btn">
                  {loading ? 'Scanning...' : 'Scan Market'}
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="tab-content">
            <div className="search-section">
              <h2>Get Actionable Insights</h2>
              <p className="description">
                Get clear entry points, exit strategies, and catalysts to watch
              </p>
              <div className="input-group">
                <input
                  type="text"
                  placeholder="Enter ticker (e.g., AAPL, PLTR)"
                  value={ticker}
                  onChange={(e) => setTicker(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && getInsights()}
                  className="ticker-input"
                />
                <button onClick={getInsights} disabled={loading} className="analyze-btn">
                  {loading ? 'Loading...' : 'Get Insights'}
                </button>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <div className="error-content">
              <span className="error-icon">⚠️</span>
              <span>{error}</span>
              <button className="error-close" onClick={() => setError(null)}>×</button>
            </div>
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Sherlok is investigating...</p>
          </div>
        )}

        {analysis && (
          <div className="results-card">
            <h3>Analysis Results</h3>
            <div className="analysis-content">
              <pre>{JSON.stringify(analysis, null, 2)}</pre>
            </div>
          </div>
        )}

        {signals && (
          <div className="results-card">
            <h3>Market Signals</h3>
            <div className="signals-grid">
              {signals.signals && signals.signals.map((signal, index) => (
                <div key={index} className="signal-card">
                  <h4>{signal.ticker}</h4>
                  <div className="signal-score">
                    Score: <span className="score-value">{signal.score}</span>
                  </div>
                  <div className="signal-reasons">
                    {signal.reasons.map((reason, i) => (
                      <div key={i} className="reason">✓ {reason}</div>
                    ))}
                  </div>
                  <div className="signal-price">
                    Current Price: ${signal.current_price}
                  </div>
                  <div className="signal-sector">{signal.sector}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by OpenAI GPT-4, Telnyx Voice, and Lovable</p>
        <p className="disclaimer">
          ⚠️ This is for educational purposes only. Not financial advice.
        </p>
      </footer>
    </div>
  );
}

export default App;
