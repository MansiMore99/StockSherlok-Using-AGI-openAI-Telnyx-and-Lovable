# 🔍 StockSherlok - AI-Powered Research Agent

AI-powered stock detective built with AGI agents, Lovable UI, OpenAI intelligence, and Telnyx voice magic.

## Overview

Sherlok is an AI-powered research agent that helps retail investors quickly spot promising mid-cap and early-stage tech companies. Instead of digging through earnings reports, analyst notes, and market data manually, Sherlok does the detective work for you, scanning signals, summarizing insights, and giving clear, actionable breakdowns.

## Features

### 🎯 Core Capabilities
- **Company Analysis**: Comprehensive AI-powered analysis of any publicly traded company
- **Market Signal Scanning**: Automatically discovers promising mid-cap and early-stage tech companies
- **Earnings Report Summarization**: Concise summaries of earnings reports and analyst notes
- **Actionable Insights**: Clear entry points, exit strategies, and catalysts to watch
- **Voice Integration**: Interactive voice queries via Telnyx

### 🤖 AI-Powered Analysis
- Leverages OpenAI GPT-4 for intelligent analysis
- Real-time stock data integration via yfinance
- Multi-factor signal scoring system
- Sector-specific insights

### 📊 Key Metrics Analyzed
- Revenue Growth
- Profit Margins
- Market Capitalization
- P/E Ratios
- Price Momentum
- Industry Trends

## Technology Stack

### Backend
- **Python 3.x** - Core backend language
- **Flask** - REST API framework
- **OpenAI GPT-4** - AI analysis engine
- **yfinance** - Real-time stock data
- **Telnyx** - Voice and SMS integration

### Frontend
- **React 18** - Modern UI framework
- **Axios** - HTTP client
- **CSS3** - Responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- OpenAI API key
- Telnyx API key (optional, for voice features)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Add your API keys to `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
TELNYX_API_KEY=your_telnyx_api_key_here
TELNYX_PHONE_NUMBER=your_telnyx_phone_number_here
FLASK_ENV=development
PORT=5000
```

5. Run the backend server:
```bash
python app.py
```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Create a `.env` file (optional):
```bash
REACT_APP_API_URL=http://localhost:5000/api
```

4. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Health Check
```
GET /api/health
```

### Analyze Company
```
POST /api/analyze
Content-Type: application/json

{
  "ticker": "AAPL",
  "company_name": "Apple Inc."
}
```

### Scan Market Signals
```
POST /api/scan
Content-Type: application/json

{
  "sector": "technology",
  "market_cap": "mid"
}
```

### Summarize Report
```
POST /api/summarize
Content-Type: application/json

{
  "ticker": "AAPL",
  "report_type": "earnings"
}
```

### Get Actionable Insights
```
POST /api/insights
Content-Type: application/json

{
  "ticker": "AAPL"
}
```

### Voice Webhook
```
POST /api/voice/webhook
Content-Type: application/json
```

## Usage Examples

### Analyzing a Company
```python
import requests

response = requests.post('http://localhost:5000/api/analyze', json={
    'ticker': 'PLTR',
    'company_name': 'Palantir Technologies'
})

print(response.json())
```

### Scanning Market Signals
```python
import requests

response = requests.post('http://localhost:5000/api/scan', json={
    'sector': 'technology',
    'market_cap': 'mid'
})

print(response.json())
```

## Project Structure

```
StockSherlok/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── research_agent.py      # AI research agent core logic
│   ├── voice_handler.py       # Telnyx voice integration
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Styling
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Global styles
│   └── package.json          # Node.js dependencies
├── .gitignore
└── README.md
```

## Features in Detail

### 1. Company Analysis
The research agent performs comprehensive analysis including:
- Financial metrics evaluation
- Business model assessment
- Growth potential analysis
- Risk assessment
- Clear buy/hold/sell recommendations

### 2. Market Signal Scanning
Automatically identifies promising companies based on:
- Revenue growth trends
- Profit margin health
- Market capitalization sweet spot
- Price momentum
- Multi-factor scoring system

### 3. Report Summarization
Condenses complex financial reports into:
- Key financial highlights
- Management commentary insights
- Forward guidance implications
- Actionable takeaways

### 4. Actionable Insights
Provides practical investment guidance:
- Entry point recommendations
- Exit strategy suggestions
- Risk management tips
- Timeline considerations
- Key catalysts to monitor

## Customization

### Adding New Sectors
Edit `research_agent.py` and add sectors to the `sample_tickers` dictionary:

```python
sample_tickers = {
    'technology': ['PLTR', 'SNOW', 'CRWD'],
    'healthcare': ['TDOC', 'VEEV', 'HIMS'],
    'your_sector': ['TICK1', 'TICK2', 'TICK3']
}
```

### Adjusting AI Analysis
Modify the prompts in `research_agent.py` to customize the analysis style and focus areas.

## Security Considerations

⚠️ **Important Security Notes:**
- Never commit your `.env` file with real API keys
- Keep your OpenAI and Telnyx API keys secure
- This application is for educational purposes only
- Not intended as financial advice

## Limitations

- Stock data relies on yfinance availability
- OpenAI API usage incurs costs
- Real-time data may have slight delays
- Analysis is AI-generated and should not be the sole basis for investment decisions

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

⚠️ **IMPORTANT**: This application is for educational and informational purposes only. It is not intended to provide financial, investment, or trading advice. Always conduct your own research and consult with qualified financial advisors before making investment decisions. The creators of this application are not responsible for any financial losses incurred from using this tool.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

Built with ❤️ using OpenAI GPT-4, Telnyx, and modern web technologies.
