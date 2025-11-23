# StockSherlok Backend

This is the backend API server for StockSherlok, providing AI-powered stock research capabilities.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the server:
```bash
python app.py
```

## API Documentation

See the main README.md for complete API documentation.

## Testing

You can test the API using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Analyze a company
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Scan market signals
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"sector": "technology", "market_cap": "mid"}'
```

## Architecture

- `app.py` - Main Flask application with API routes
- `research_agent.py` - Core AI research logic using OpenAI
- `voice_handler.py` - Telnyx voice integration

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `TELNYX_API_KEY` - Your Telnyx API key (optional)
- `TELNYX_PHONE_NUMBER` - Your Telnyx phone number (optional)
- `FLASK_ENV` - Development or production mode
- `PORT` - Server port (default: 5000)
