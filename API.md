# API Documentation

Complete API reference for StockSherlok Research Agent.

## Base URL

```
http://localhost:5000/api
```

For production: `https://your-domain.com/api`

## Authentication

Currently, the API does not require authentication. Future versions will support API keys.

## Endpoints

### Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "StockSherlok Research Agent"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### Analyze Company

Get comprehensive AI-powered analysis of a company.

**Endpoint:** `POST /api/analyze`

**Request Body:**
```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc." // optional
}
```

**Parameters:**
- `ticker` (string, required): Stock ticker symbol
- `company_name` (string, optional): Company name for context

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "analysis": {
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "stock_data": {
      "current_price": 150.25,
      "market_cap": 2400000000000,
      "pe_ratio": 25.5,
      "revenue_growth": 0.15,
      "profit_margins": 0.25,
      "sector": "Technology",
      "industry": "Consumer Electronics"
    },
    "analysis": "AI-generated analysis text...",
    "timestamp": 1637000000
  }
}
```

**Error Response:**
```json
{
  "error": "Ticker symbol is required"
}
```

**Status Codes:**
- `200 OK` - Analysis successful
- `400 Bad Request` - Missing or invalid parameters
- `500 Internal Server Error` - Analysis failed

**Example:**
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "PLTR", "company_name": "Palantir Technologies"}'
```

---

### Scan Market Signals

Scan the market for promising companies based on sector and market cap.

**Endpoint:** `POST /api/scan`

**Request Body:**
```json
{
  "sector": "technology",
  "market_cap": "mid"
}
```

**Parameters:**
- `sector` (string, optional): Sector to scan. Options: `technology`, `healthcare`, `finance`. Default: `technology`
- `market_cap` (string, optional): Market cap range. Default: `mid`

**Response:**
```json
{
  "success": true,
  "signals": {
    "sector": "technology",
    "market_cap": "mid",
    "signals": [
      {
        "ticker": "PLTR",
        "score": 75,
        "reasons": [
          "Strong revenue growth",
          "Positive momentum",
          "Mid-cap sweet spot"
        ],
        "current_price": 18.50,
        "sector": "Technology"
      }
    ],
    "summary": "Found 3 promising signals in technology sector"
  }
}
```

**Status Codes:**
- `200 OK` - Scan successful
- `500 Internal Server Error` - Scan failed

**Example:**
```bash
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"sector": "technology", "market_cap": "mid"}'
```

---

### Summarize Report

Get a concise summary of earnings reports or analyst notes.

**Endpoint:** `POST /api/summarize`

**Request Body:**
```json
{
  "ticker": "AAPL",
  "report_type": "earnings"
}
```

**Parameters:**
- `ticker` (string, required): Stock ticker symbol
- `report_type` (string, optional): Type of report. Default: `earnings`

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "report_type": "earnings",
  "summary": {
    "ticker": "AAPL",
    "report_type": "earnings",
    "summary": "AI-generated summary text...",
    "timestamp": 1637000000
  }
}
```

**Status Codes:**
- `200 OK` - Summarization successful
- `400 Bad Request` - Missing ticker
- `500 Internal Server Error` - Summarization failed

**Example:**
```bash
curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "report_type": "earnings"}'
```

---

### Get Actionable Insights

Get specific, actionable investment insights for a company.

**Endpoint:** `POST /api/insights`

**Request Body:**
```json
{
  "ticker": "AAPL"
}
```

**Parameters:**
- `ticker` (string, required): Stock ticker symbol

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "insights": {
    "ticker": "AAPL",
    "insights": "AI-generated insights text including entry points, exit strategies, etc...",
    "stock_data": {
      "price": 150.25,
      "market_cap": 2400000000000,
      "sector": "Technology"
    },
    "timestamp": 1637000000
  }
}
```

**Status Codes:**
- `200 OK` - Insights generated successfully
- `400 Bad Request` - Missing ticker
- `500 Internal Server Error` - Insights generation failed

**Example:**
```bash
curl -X POST http://localhost:5000/api/insights \
  -H "Content-Type: application/json" \
  -d '{"ticker": "PLTR"}'
```

---

### Voice Webhook

Handle incoming Telnyx voice webhooks.

**Endpoint:** `POST /api/voice/webhook`

**Request Body:**
Telnyx webhook payload (varies by event type)

**Response:**
```json
{
  "status": "processed",
  "event_type": "call.answered"
}
```

**Status Codes:**
- `200 OK` - Webhook processed
- `500 Internal Server Error` - Webhook processing failed

**Note:** This endpoint is designed to be called by Telnyx, not directly by users.

---

## Error Handling

All endpoints follow a consistent error response format:

```json
{
  "error": "Description of what went wrong"
}
```

Common HTTP status codes:
- `200 OK` - Request successful
- `400 Bad Request` - Invalid or missing parameters
- `500 Internal Server Error` - Server-side error

## Rate Limiting

Currently, there is no rate limiting. This will be added in future versions.

## Data Sources

- **Stock Data**: yfinance
- **AI Analysis**: OpenAI GPT-4
- **Voice/SMS**: Telnyx

## Response Times

Typical response times:
- Health check: < 50ms
- Analysis: 2-5 seconds (depends on OpenAI API)
- Market scan: 3-8 seconds
- Insights: 2-5 seconds

## Best Practices

1. **Cache Results**: Analysis results can be cached for a few minutes to reduce API calls
2. **Error Handling**: Always check for `error` field in responses
3. **Timeouts**: Set reasonable timeouts (10-15 seconds) for API calls
4. **Retry Logic**: Implement exponential backoff for retries

## Code Examples

### Python

```python
import requests

# Analyze a company
response = requests.post('http://localhost:5000/api/analyze', json={
    'ticker': 'AAPL'
})
data = response.json()

if 'error' in data:
    print(f"Error: {data['error']}")
else:
    print(f"Analysis: {data['analysis']}")
```

### JavaScript

```javascript
// Analyze a company
fetch('http://localhost:5000/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    ticker: 'AAPL'
  })
})
.then(response => response.json())
.then(data => {
  if (data.error) {
    console.error('Error:', data.error);
  } else {
    console.log('Analysis:', data.analysis);
  }
});
```

### cURL

```bash
# Analyze a company
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}'

# Scan market
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"sector": "technology"}'

# Get insights
curl -X POST http://localhost:5000/api/insights \
  -H "Content-Type: application/json" \
  -d '{"ticker": "PLTR"}'
```

## Changelog

### v1.0.0 (Initial Release)
- Basic analysis endpoint
- Market scanning
- Report summarization
- Actionable insights
- Voice webhook handler

## Support

For issues or questions:
- GitHub Issues: [Submit an issue](https://github.com/MansiMore99/StockSherlok-Using-AGI-openAI-Telnyx-and-Lovable/issues)
- Documentation: See README.md

## Legal

⚠️ **Disclaimer**: This API is for educational and informational purposes only. It is not intended to provide financial, investment, or trading advice. Always consult with qualified financial advisors before making investment decisions.
