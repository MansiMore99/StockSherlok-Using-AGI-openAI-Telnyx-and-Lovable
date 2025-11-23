"""
StockSherlok - AI-Powered Research Agent
Main application file
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from research_agent import ResearchAgent
from voice_handler import VoiceHandler

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
research_agent = ResearchAgent(api_key=os.getenv('OPENAI_API_KEY'))
voice_handler = VoiceHandler(
    api_key=os.getenv('TELNYX_API_KEY'),
    phone_number=os.getenv('TELNYX_PHONE_NUMBER')
)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'StockSherlok Research Agent'
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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
