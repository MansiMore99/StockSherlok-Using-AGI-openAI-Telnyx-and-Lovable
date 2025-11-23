import OpenAI from 'openai';
import dotenv from 'dotenv';

dotenv.config();

// Placeholder constant for API key configuration
const PLACEHOLDER_API_KEY = 'your_openai_api_key_here';

/**
 * StockSherlokAgent - An intelligent multi-step agent using OpenAI's AGI capabilities
 * This agent can handle complex stock analysis queries through multi-step reasoning
 */
class StockSherlokAgent {
  constructor() {
    const apiKey = process.env.OPENAI_API_KEY;
    
    if (!apiKey || apiKey === PLACEHOLDER_API_KEY) {
      console.warn('⚠️  OpenAI API key not configured. Agent will run in limited mode.');
      this.client = null;
    } else {
      this.client = new OpenAI({
        apiKey: apiKey,
      });
    }
    
    this.systemPrompt = `You are Stock Sherlok, an AI-powered financial detective specializing in stock market analysis.
    
Your capabilities include:
1. Analyzing stock performance and trends
2. Providing insights on company fundamentals
3. Explaining market movements
4. Offering educational information about investing
5. Breaking down complex financial concepts

You communicate in a friendly, detective-like manner, using deductive reasoning to help users understand stock markets.
Always remind users that you provide information, not financial advice, and they should consult professionals for investment decisions.`;
    
    this.conversationHistory = [];
  }

  /**
   * Multi-step reasoning process for stock analysis
   * Breaks down complex queries into manageable steps
   */
  async analyzeQuery(userQuery, stockData = null) {
    // Step 1: Understand the query intent
    const intent = await this.identifyIntent(userQuery);
    
    // Step 2: Gather relevant context
    const context = await this.gatherContext(userQuery, stockData);
    
    // Step 3: Generate comprehensive response
    const response = await this.generateResponse(userQuery, intent, context);
    
    return {
      response,
      intent,
      steps: ['Intent Analysis', 'Context Gathering', 'Response Generation']
    };
  }

  /**
   * Identify the intent of user query (classification step)
   */
  async identifyIntent(query) {
    if (!this.client) {
      return 'general';
    }
    
    const intentPrompt = `Analyze this query and identify the primary intent. Categories: 
    - stock_price: User wants current or historical price
    - company_analysis: User wants company fundamentals
    - market_trend: User wants market or sector trends
    - education: User wants to learn about investing
    - general: General question
    
    Query: "${query}"
    
    Respond with just the category name.`;
    
    try {
      const completion = await this.client.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: intentPrompt }],
        temperature: 0.3,
        max_tokens: 50,
      });
      
      return completion.choices[0].message.content.trim().toLowerCase();
    } catch (error) {
      console.error('Intent identification error:', error.message);
      return 'general';
    }
  }

  /**
   * Gather context based on query (data aggregation step)
   */
  async gatherContext(query, stockData) {
    const context = {
      timestamp: new Date().toISOString(),
      query,
      stockData: stockData || {}
    };
    
    return context;
  }

  /**
   * Generate comprehensive response (synthesis step)
   */
  async generateResponse(query, intent, context) {
    if (!this.client) {
      return `I apologize, but I need an OpenAI API key to provide intelligent analysis. Please configure your OPENAI_API_KEY in the .env file. 

For now, here's what I can tell you: I'm Stock Sherlok, your AI financial detective. Once configured, I can help you with:
- Real-time stock analysis
- Company fundamentals
- Market trends explanation
- Investment education

Please add your OpenAI API key to get started!`;
    }
    
    const messages = [
      { role: "system", content: this.systemPrompt },
      ...this.conversationHistory,
      { role: "user", content: this.buildContextualQuery(query, context) }
    ];
    
    try {
      const completion = await this.client.chat.completions.create({
        model: "gpt-4",
        messages,
        temperature: 0.7,
        max_tokens: 500,
      });
      
      const response = completion.choices[0].message.content;
      
      // Update conversation history (keep last 6 messages)
      this.conversationHistory.push({ role: "user", content: query });
      this.conversationHistory.push({ role: "assistant", content: response });
      
      if (this.conversationHistory.length > 6) {
        this.conversationHistory = this.conversationHistory.slice(-6);
      }
      
      return response;
    } catch (error) {
      console.error('Response generation error:', error.message);
      return `I apologize, detective work requires proper credentials. Please ensure your OpenAI API key is configured. Error: ${error.message}`;
    }
  }

  /**
   * Build contextual query with stock data
   */
  buildContextualQuery(query, context) {
    let contextualQuery = query;
    
    if (context.stockData && Object.keys(context.stockData).length > 0) {
      contextualQuery += `\n\nRelevant stock data:\n${JSON.stringify(context.stockData, null, 2)}`;
    }
    
    return contextualQuery;
  }

  /**
   * Reset conversation history
   */
  resetConversation() {
    this.conversationHistory = [];
  }

  /**
   * Process voice input (integration with Telnyx)
   */
  async processVoiceQuery(transcribedText, stockData = null) {
    return await this.analyzeQuery(transcribedText, stockData);
  }
}

export default StockSherlokAgent;
