import axios from 'axios';

/**
 * StockDataService - Handles fetching stock data from various sources
 */
class StockDataService {
  constructor() {
    this.alphaVantageKey = process.env.ALPHA_VANTAGE_API_KEY;
  }

  /**
   * Get stock quote data
   */
  async getStockQuote(symbol) {
    // For demo purposes, using mock data
    // In production, you would use Alpha Vantage or similar APIs
    try {
      if (this.alphaVantageKey && this.alphaVantageKey !== 'your_alpha_vantage_api_key_here') {
        const url = `https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${this.alphaVantageKey}`;
        const response = await axios.get(url);
        
        if (response.data['Global Quote']) {
          const quote = response.data['Global Quote'];
          return {
            symbol: quote['01. symbol'],
            price: quote['05. price'],
            change: quote['09. change'],
            changePercent: quote['10. change percent'],
            volume: quote['06. volume'],
            lastUpdated: quote['07. latest trading day']
          };
        }
      }
      
      // Fallback to mock data for demo
      return this.getMockStockData(symbol);
    } catch (error) {
      console.error('Error fetching stock quote:', error.message);
      return this.getMockStockData(symbol);
    }
  }

  /**
   * Get company overview
   */
  async getCompanyOverview(symbol) {
    try {
      if (this.alphaVantageKey && this.alphaVantageKey !== 'your_alpha_vantage_api_key_here') {
        const url = `https://www.alphavantage.co/query?function=OVERVIEW&symbol=${symbol}&apikey=${this.alphaVantageKey}`;
        const response = await axios.get(url);
        
        if (response.data.Symbol) {
          return {
            name: response.data.Name,
            symbol: response.data.Symbol,
            description: response.data.Description,
            sector: response.data.Sector,
            industry: response.data.Industry,
            marketCap: response.data.MarketCapitalization,
            peRatio: response.data.PERatio
          };
        }
      }
      
      return this.getMockCompanyData(symbol);
    } catch (error) {
      console.error('Error fetching company overview:', error.message);
      return this.getMockCompanyData(symbol);
    }
  }

  /**
   * Mock stock data for demo purposes
   */
  getMockStockData(symbol) {
    const mockData = {
      'AAPL': {
        symbol: 'AAPL',
        price: '178.50',
        change: '+2.50',
        changePercent: '+1.42%',
        volume: '52000000',
        lastUpdated: new Date().toISOString().split('T')[0]
      },
      'GOOGL': {
        symbol: 'GOOGL',
        price: '142.30',
        change: '-1.20',
        changePercent: '-0.84%',
        volume: '28000000',
        lastUpdated: new Date().toISOString().split('T')[0]
      },
      'MSFT': {
        symbol: 'MSFT',
        price: '378.85',
        change: '+5.15',
        changePercent: '+1.38%',
        volume: '23000000',
        lastUpdated: new Date().toISOString().split('T')[0]
      }
    };
    
    return mockData[symbol.toUpperCase()] || {
      symbol: symbol.toUpperCase(),
      price: '100.00',
      change: '+0.00',
      changePercent: '+0.00%',
      volume: '1000000',
      lastUpdated: new Date().toISOString().split('T')[0]
    };
  }

  /**
   * Mock company data for demo purposes
   */
  getMockCompanyData(symbol) {
    const mockData = {
      'AAPL': {
        name: 'Apple Inc.',
        symbol: 'AAPL',
        description: 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.',
        sector: 'Technology',
        industry: 'Consumer Electronics',
        marketCap: '2800000000000',
        peRatio: '29.5'
      },
      'GOOGL': {
        name: 'Alphabet Inc.',
        symbol: 'GOOGL',
        description: 'Alphabet Inc. offers various products and platforms in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America.',
        sector: 'Communication Services',
        industry: 'Internet Content & Information',
        marketCap: '1750000000000',
        peRatio: '26.8'
      },
      'MSFT': {
        name: 'Microsoft Corporation',
        symbol: 'MSFT',
        description: 'Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide.',
        sector: 'Technology',
        industry: 'Software—Infrastructure',
        marketCap: '2820000000000',
        peRatio: '35.2'
      }
    };
    
    return mockData[symbol.toUpperCase()] || {
      name: `${symbol.toUpperCase()} Company`,
      symbol: symbol.toUpperCase(),
      description: 'Company information not available in demo mode.',
      sector: 'Unknown',
      industry: 'Unknown',
      marketCap: 'N/A',
      peRatio: 'N/A'
    };
  }
}

export default StockDataService;
