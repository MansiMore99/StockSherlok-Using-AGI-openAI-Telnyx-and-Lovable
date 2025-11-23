"""
StockSherlok - AI-Powered Research Agent
Main application file
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
from research_agent import ResearchAgent
from voice_handler import VoiceHandler

# Load environment variables
load_dotenv()

# Validate required environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY environment variable is required")
    print("Please set it in your .env file")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
research_agent = ResearchAgent(api_key=OPENAI_API_KEY)

# Voice handler is optional (only if Telnyx credentials are provided)
TELNYX_API_KEY = os.getenv('TELNYX_API_KEY')
TELNYX_PHONE_NUMBER = os.getenv('TELNYX_PHONE_NUMBER')

if TELNYX_API_KEY and TELNYX_PHONE_NUMBER:
    voice_handler = VoiceHandler(
        api_key=TELNYX_API_KEY,
        phone_number=TELNYX_PHONE_NUMBER
    )
    print("✓ Voice handler initialized")
else:
    voice_handler = None
    print("⚠ Voice handler not initialized (Telnyx credentials not provided)")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'StockSherlok Research Agent',
        'voice_enabled': voice_handler is not None
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_company():
    """
    Analyze a company and provide insights
    Expected payload: { "ticker": "AAPL", "company_name": "Apple Inc." }
    """
    try:
        data = request.get_json()
        ticker = data.get('ticker')
        company_name = data.get('company_name')
        
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400
        
        # Get analysis from research agent
        analysis = research_agent.analyze_company(ticker, company_name)
        
        return jsonify({
            'success': True,
            'ticker': ticker,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan', methods=['POST'])
def scan_signals():
    """
    Scan market signals for promising companies
    Expected payload: { "sector": "technology", "market_cap": "mid" }
    """
    try:
        data = request.get_json()
        sector = data.get('sector', 'technology')
        market_cap = data.get('market_cap', 'mid')
        
        # Scan for promising companies
        signals = research_agent.scan_market_signals(sector, market_cap)
        
        return jsonify({
            'success': True,
            'signals': signals
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/summarize', methods=['POST'])
def summarize_report():
    """
    Summarize earnings reports or analyst notes
    Expected payload: { "ticker": "AAPL", "report_type": "earnings" }
    """
    try:
        data = request.get_json()
        ticker = data.get('ticker')
        report_type = data.get('report_type', 'earnings')
        
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400
        
        # Get report summary
        summary = research_agent.summarize_report(ticker, report_type)
        
        return jsonify({
            'success': True,
            'ticker': ticker,
            'report_type': report_type,
            'summary': summary
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/voice/webhook', methods=['POST'])
def voice_webhook():
    """
    Handle Telnyx voice webhooks
    """
    if not voice_handler:
        return jsonify({'error': 'Voice features not enabled'}), 503
    
    try:
        data = request.get_json()
        response = voice_handler.handle_webhook(data)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/insights', methods=['POST'])
def get_insights():
    """
    Get actionable insights for a specific company
    Expected payload: { "ticker": "AAPL" }
    """
    try:
        data = request.get_json()
        ticker = data.get('ticker')
        
        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400
        
        # Get actionable insights
        insights = research_agent.get_actionable_insights(ticker)
        
        return jsonify({
            'success': True,
            'ticker': ticker,
            'insights': insights
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-multiple', methods=['POST'])
def analyze_multiple():
    """
    Analyze multiple companies or auto-discover mid-cap companies
    Expected payload: { 
        "query": "top mid cap companies this week",  // optional, for context
        "tickers": ["PLTR", "CRWD", "NET"]  // optional
    }
    
    If tickers are provided, analyze those specific companies.
    If tickers are NOT provided, auto-discover mid-cap companies and analyze them.
    """
    try:
        data = request.get_json() or {}
        tickers = data.get('tickers', [])
        query = data.get('query', '')
        
        # If no tickers provided, discover mid-cap companies
        if not tickers:
            tickers = research_agent.discover_midcap_companies(limit=15)
            
            if not tickers:
                return jsonify({
                    'error': 'No mid-cap companies found. Please try again later.'
                }), 404
        
        # Analyze each ticker and compute metrics
        results = []
        for ticker in tickers:
            analysis = research_agent.analyze_company(ticker)
            
            # Compute metrics for this ticker
            metrics = research_agent.get_ticker_metrics(ticker)
            
            # Add metrics to the result (if no error)
            if 'error' not in metrics:
                analysis['metrics'] = metrics
            
            results.append(analysis)
        
        # Use LLM to analyze and compare all companies
        llm_summary = research_agent.analyze_multiple_companies_llm(query, results)
        
        # Generate comparison charts
        charts = research_agent.create_comparison_charts(results)
        
        # Create UI-friendly response structure with convenience shortcuts
        return jsonify({
            'success': True,
            'analysis': {
                'query': query,
                'count': len(results),
                'companies_raw': results,
                'summary': llm_summary,
                'charts': charts,
                'top_3': llm_summary.get('top_3_companies', []),
                'spoken_summary': llm_summary.get('spoken_summary', '')
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Starting StockSherlok API on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
