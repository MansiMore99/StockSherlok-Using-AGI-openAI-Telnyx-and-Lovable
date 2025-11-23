import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import rateLimit from 'express-rate-limit';
import StockSherlokAgent from './agents/StockSherlokAgent.js';
import StockDataService from './services/StockDataService.js';
import TelnyxVoiceService from './services/TelnyxVoiceService.js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 3000;

// Initialize services
const agent = new StockSherlokAgent();
const stockService = new StockDataService();
const voiceService = new TelnyxVoiceService();

// Rate limiting middleware for API endpoints
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../public')));

// Apply rate limiting to API routes
app.use('/api/', apiLimiter);

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    voiceEnabled: voiceService.isEnabled()
  });
});

// Chat endpoint - Main interaction with Stock Sherlok
app.post('/api/chat', async (req, res) => {
  try {
    const { message, symbol } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Fetch stock data if symbol is provided
    let stockData = null;
    if (symbol) {
      const quote = await stockService.getStockQuote(symbol);
      const company = await stockService.getCompanyOverview(symbol);
      stockData = { quote, company };
    }

    // Process query with AGI agent
    const result = await agent.analyzeQuery(message, stockData);

    res.json({
      response: result.response,
      intent: result.intent,
      steps: result.steps,
      stockData: stockData,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ 
      error: 'Failed to process your request',
      details: error.message 
    });
  }
});

// Stock quote endpoint
app.get('/api/stock/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const quote = await stockService.getStockQuote(symbol);
    res.json(quote);
  } catch (error) {
    console.error('Stock quote error:', error);
    res.status(500).json({ error: 'Failed to fetch stock data' });
  }
});

// Company overview endpoint
app.get('/api/company/:symbol', async (req, res) => {
  try {
    const { symbol } = req.params;
    const company = await stockService.getCompanyOverview(symbol);
    res.json(company);
  } catch (error) {
    console.error('Company overview error:', error);
    res.status(500).json({ error: 'Failed to fetch company data' });
  }
});

// Voice webhook endpoint for Telnyx
app.post('/api/voice/webhook', async (req, res) => {
  try {
    const event = req.body;
    const webhookData = voiceService.processWebhook(event);

    // Handle different event types
    switch (webhookData.eventType) {
      case 'call.initiated':
        console.log('Call initiated:', webhookData.callControlId);
        break;
      
      case 'call.answered':
        await voiceService.handleIncomingCall(
          webhookData.callControlId,
          `${req.protocol}://${req.get('host')}/api/voice/webhook`
        );
        break;
      
      case 'call.speak.ended':
        // Could gather user input here
        console.log('Speak ended');
        break;
      
      case 'call.hangup':
        console.log('Call ended');
        break;
      
      default:
        console.log('Unhandled event type:', webhookData.eventType);
    }

    res.json({ received: true });
  } catch (error) {
    console.error('Voice webhook error:', error);
    res.status(500).json({ error: 'Webhook processing failed' });
  }
});

// Voice query endpoint (for web-based voice interaction)
app.post('/api/voice/query', async (req, res) => {
  try {
    const { transcribedText, symbol } = req.body;

    if (!transcribedText) {
      return res.status(400).json({ error: 'Transcribed text is required' });
    }

    // Fetch stock data if symbol is provided
    let stockData = null;
    if (symbol) {
      const quote = await stockService.getStockQuote(symbol);
      const company = await stockService.getCompanyOverview(symbol);
      stockData = { quote, company };
    }

    // Process voice query with agent
    const result = await agent.processVoiceQuery(transcribedText, stockData);

    res.json({
      response: result.response,
      intent: result.intent,
      voiceEnabled: voiceService.isEnabled(),
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Voice query error:', error);
    res.status(500).json({ error: 'Failed to process voice query' });
  }
});

// Reset conversation endpoint
app.post('/api/reset', (req, res) => {
  agent.resetConversation();
  res.json({ message: 'Conversation reset successfully' });
});

// Serve the UI
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

// Start server
app.listen(port, () => {
  console.log(`
  🔍 Stock Sherlok Server Running!
  ================================
  
  Server: http://localhost:${port}
  Health: http://localhost:${port}/api/health
  
  Voice Features: ${voiceService.isEnabled() ? '✓ Enabled' : '✗ Disabled (Configure TELNYX_API_KEY to enable)'}
  
  Ready to solve stock market mysteries! 🕵️
  `);
});

export default app;
