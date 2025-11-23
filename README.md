# 🔍 Stock Sherlok - AI-Powered Financial Detective

AI-powered stock detective built with AGI agents, Lovable UI, OpenAI intelligence, and Telnyx voice magic.

## 🌟 Features

### 🤖 AGI Multi-Step Agents
- **Intelligent Query Analysis**: Uses OpenAI's advanced models to break down complex stock queries into manageable steps
- **Intent Recognition**: Automatically identifies whether you're asking about prices, company analysis, market trends, or general education
- **Context Gathering**: Fetches relevant stock data and company information to provide informed responses
- **Multi-Turn Conversations**: Maintains conversation history for contextual follow-up questions

### 💬 Lovable Interactive UI
- **Beautiful, Modern Design**: Gradient-based responsive interface that works on all devices
- **Real-Time Chat**: Instant responses from Stock Sherlok
- **Stock Data Visualization**: Displays live stock quotes, company info, and market data
- **Voice Input Support**: Built-in browser speech recognition for hands-free queries

### 🎤 Telnyx Voice Integration
- **Phone-Based Queries**: Call Stock Sherlok and ask questions via voice (when configured)
- **Natural Voice Interaction**: Talk to Sherlok like a real financial assistant
- **Webhook Support**: Handles incoming calls and processes voice commands
- **Text-to-Speech Responses**: Sherlok speaks back the analysis results

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- OpenAI API key
- (Optional) Telnyx API key for voice features
- (Optional) Alpha Vantage API key for real stock data

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MansiMore99/StockSherlok-Using-AGI-openAI-Telnyx-and-Lovable.git
cd StockSherlok-Using-AGI-openAI-Telnyx-and-Lovable
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
TELNYX_API_KEY=your_telnyx_api_key_here  # Optional
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here  # Optional
```

### Running the Application

Start the server:
```bash
npm start
```

Or use development mode with auto-reload:
```bash
npm run dev
```

Visit `http://localhost:3000` in your browser to start chatting with Stock Sherlok!

## 📚 API Documentation

### Chat Endpoint
**POST** `/api/chat`

Request body:
```json
{
  "message": "What's the outlook for Apple stock?",
  "symbol": "AAPL"  // Optional
}
```

Response:
```json
{
  "response": "Based on the current data...",
  "intent": "stock_price",
  "steps": ["Intent Analysis", "Context Gathering", "Response Generation"],
  "stockData": {
    "quote": { "symbol": "AAPL", "price": "178.50", ... },
    "company": { "name": "Apple Inc.", ... }
  },
  "timestamp": "2025-11-23T00:00:00.000Z"
}
```

### Stock Quote
**GET** `/api/stock/:symbol`

Example: `/api/stock/AAPL`

### Company Overview
**GET** `/api/company/:symbol`

Example: `/api/company/GOOGL`

### Voice Webhook
**POST** `/api/voice/webhook`

Handles Telnyx voice webhooks for phone-based interactions.

### Reset Conversation
**POST** `/api/reset`

Clears conversation history.

## 🏗️ Architecture

### AGI Agent Flow
1. **Intent Identification**: Classifies user query into categories (stock_price, company_analysis, market_trend, education, general)
2. **Context Gathering**: Fetches relevant stock data and company information
3. **Response Generation**: Uses GPT-4 to synthesize information and generate comprehensive, conversational responses

### Project Structure
```
StockSherlok/
├── src/
│   ├── agents/
│   │   └── StockSherlokAgent.js      # AGI multi-step agent
│   ├── services/
│   │   ├── StockDataService.js       # Stock data fetching
│   │   └── TelnyxVoiceService.js     # Voice integration
│   └── index.js                      # Express server
├── public/
│   └── index.html                    # Lovable UI
├── package.json
├── .env.example
└── README.md
```

## 🔧 Configuration

### OpenAI (Required)
Get your API key from [OpenAI Platform](https://platform.openai.com/)

### Telnyx (Optional - for voice features)
1. Sign up at [Telnyx](https://telnyx.com/)
2. Get your API key and configure a phone number
3. Set up webhook URL: `https://your-domain.com/api/voice/webhook`

### Alpha Vantage (Optional - for real stock data)
Get a free API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key)

**Note**: Without Alpha Vantage API key, the app uses mock data for demonstration.

## 🎯 Use Cases

1. **Stock Price Queries**: "What's the current price of Tesla?"
2. **Company Analysis**: "Tell me about Microsoft's business"
3. **Market Trends**: "What's happening in the tech sector?"
4. **Education**: "Explain what P/E ratio means"
5. **Investment Insights**: "Should I be concerned about recent market volatility?"
6. **Voice Queries**: Call Sherlok or use voice input in the UI

## 🔒 Security

- API keys are stored in environment variables
- CORS enabled for controlled access
- Input validation on all endpoints
- Secure dependency versions (no known vulnerabilities)

## 🛠️ Technologies Used

- **Backend**: Node.js, Express
- **AI/AGI**: OpenAI GPT-4, GPT-3.5-turbo
- **Voice**: Telnyx Voice API
- **Stock Data**: Alpha Vantage API (with mock data fallback)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Deployment Ready**: Docker-compatible, Heroku-ready

## 📝 License

ISC

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

Stock Sherlok provides information for educational purposes only and is not financial advice. Always consult with qualified financial advisors before making investment decisions.

---

Built with ❤️ using AGI, OpenAI, Telnyx, and Lovable UI principles
