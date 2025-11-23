"""
Research Agent - Core AI-powered analysis engine
"""
import openai
import yfinance as yf
from typing import Dict, List, Optional
import json
from metrics_engine import compute_metrics


class ResearchAgent:
    """
    AI-powered research agent for analyzing stocks and companies
    """
    
    def __init__(self, api_key: str):
        """Initialize the research agent with OpenAI API key"""
        self.api_key = api_key
        openai.api_key = api_key
        
    def _get_stock_data(self, ticker: str, include_history: bool = False) -> Dict:
        """
        Fetch stock data using yfinance
        
        Args:
            ticker: Stock ticker symbol
            include_history: If True, include price history DataFrame
            
        Returns:
            Dict with stock data and optionally price_history
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            history = stock.history(period="6mo")  # Get 6 months for trend analysis
            
            data = {
                'current_price': info.get('currentPrice', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'revenue_growth': info.get('revenueGrowth', 'N/A'),
                'profit_margins': info.get('profitMargins', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'summary': info.get('longBusinessSummary', 'N/A'),
                'avg_volume': info.get('averageVolume', 'N/A'),
                'recent_trend': 'up' if len(history) > 0 and history['Close'].iloc[-1] > history['Close'].iloc[0] else 'down'
            }
            
            if include_history:
                data['price_history'] = history
            
            return data
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_company(self, ticker: str, company_name: Optional[str] = None) -> Dict:
        """
        Perform comprehensive company analysis
        """
        # Get stock data
        stock_data = self._get_stock_data(ticker)
        
        if 'error' in stock_data:
            return {
                'error': f"Failed to fetch data for {ticker}: {stock_data['error']}",
                'recommendation': 'Unable to analyze'
            }
        
        # Create prompt for OpenAI
        prompt = f"""
As an expert financial analyst specializing in mid-cap and early-stage tech companies, 
analyze the following company data and provide clear, actionable insights for retail investors.

Company: {company_name or ticker}
Ticker: {ticker}

Financial Data:
- Current Price: ${stock_data.get('current_price', 'N/A')}
- Market Cap: ${stock_data.get('market_cap', 'N/A'):,} 
- P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
- Revenue Growth: {stock_data.get('revenue_growth', 'N/A')}
- Profit Margins: {stock_data.get('profit_margins', 'N/A')}
- Sector: {stock_data.get('sector', 'N/A')}
- Industry: {stock_data.get('industry', 'N/A')}
- Recent Trend: {stock_data.get('recent_trend', 'N/A')}

Business Summary:
{stock_data.get('summary', 'N/A')}

Provide:
1. Key Strengths (2-3 points)
2. Key Risks (2-3 points)
3. Growth Potential Assessment
4. Clear Recommendation (Buy, Hold, Sell, or Monitor)
5. Price Target Range (if applicable)

Keep the analysis concise and actionable for retail investors.
"""
        
        try:
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Sherlok, an AI research agent specializing in analyzing mid-cap and early-stage tech companies for retail investors. Provide clear, actionable insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            analysis_text = response.choices[0].message.content
            
            return {
                'ticker': ticker,
                'company_name': company_name or ticker,
                'stock_data': stock_data,
                'analysis': analysis_text,
                'timestamp': response.created
            }
        except openai.RateLimitError:
            return {
                'error': "OpenAI API rate limit exceeded. Please try again in a moment.",
                'stock_data': stock_data
            }
        except openai.AuthenticationError:
            return {
                'error': "OpenAI API authentication failed. Please check your API key.",
                'stock_data': stock_data
            }
        except openai.APIError as e:
            return {
                'error': f"OpenAI API error: {str(e)}. Please try again.",
                'stock_data': stock_data
            }
        except Exception as e:
            return {
                'error': f"Analysis failed: {str(e)}",
                'stock_data': stock_data
            }
    
    def scan_market_signals(self, sector: str = 'technology', market_cap: str = 'mid') -> Dict:
        """
        Scan market for promising companies based on signals
        """
        # Define some sample mid-cap tech companies for demonstration
        # In production, this would query a database or API
        sample_tickers = {
            'technology': ['PLTR', 'SNOW', 'CRWD', 'NET', 'DDOG', 'ZS'],
            'healthcare': ['TDOC', 'VEEV', 'HIMS'],
            'finance': ['SOFI', 'UPST', 'AFRM']
        }
        
        tickers = sample_tickers.get(sector.lower(), sample_tickers['technology'])[:3]
        
        signals = []
        for ticker in tickers:
            stock_data = self._get_stock_data(ticker)
            if 'error' not in stock_data:
                # Calculate a simple signal score
                score = 0
                reasons = []
                
                # Revenue growth signal
                if isinstance(stock_data.get('revenue_growth'), (int, float)) and stock_data['revenue_growth'] > 0.2:
                    score += 30
                    reasons.append('Strong revenue growth')
                
                # Trend signal
                if stock_data.get('recent_trend') == 'up':
                    score += 20
                    reasons.append('Positive momentum')
                
                # Market cap signal
                market_cap_val = stock_data.get('market_cap', 0)
                if isinstance(market_cap_val, (int, float)) and 2e9 < market_cap_val < 50e9:
                    score += 25
                    reasons.append('Mid-cap sweet spot')
                
                # Profit margins signal
                if isinstance(stock_data.get('profit_margins'), (int, float)) and stock_data['profit_margins'] > 0.1:
                    score += 25
                    reasons.append('Healthy profit margins')
                
                signals.append({
                    'ticker': ticker,
                    'score': score,
                    'reasons': reasons,
                    'current_price': stock_data.get('current_price', 'N/A'),
                    'sector': stock_data.get('sector', 'N/A')
                })
        
        # Sort by score
        signals.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'sector': sector,
            'market_cap': market_cap,
            'signals': signals,
            'summary': f"Found {len(signals)} promising signals in {sector} sector"
        }
    
    def summarize_report(self, ticker: str, report_type: str = 'earnings') -> Dict:
        """
        Summarize earnings reports or analyst notes
        """
        # Get company data
        stock_data = self._get_stock_data(ticker)
        
        if 'error' in stock_data:
            return {'error': f"Failed to fetch data for {ticker}"}
        
        prompt = f"""
Summarize the latest {report_type} report for {ticker} ({stock_data.get('sector', 'N/A')} sector).

Based on the following company information, provide a concise summary:
- Industry: {stock_data.get('industry', 'N/A')}
- Revenue Growth: {stock_data.get('revenue_growth', 'N/A')}
- Profit Margins: {stock_data.get('profit_margins', 'N/A')}
- Recent Trend: {stock_data.get('recent_trend', 'N/A')}

Provide:
1. Key Financial Highlights
2. Management Commentary (based on typical patterns)
3. Forward Guidance Implications
4. What Investors Should Watch

Keep it concise and focused on actionable takeaways.
"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Sherlok, an expert at summarizing financial reports for retail investors."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            summary_text = response.choices[0].message.content
            
            return {
                'ticker': ticker,
                'report_type': report_type,
                'summary': summary_text,
                'timestamp': response.created
            }
        except Exception as e:
            return {'error': f"Summarization failed: {str(e)}"}
    
    def get_actionable_insights(self, ticker: str) -> Dict:
        """
        Generate clear, actionable insights and recommendations
        """
        stock_data = self._get_stock_data(ticker)
        
        if 'error' in stock_data:
            return {'error': f"Failed to fetch data for {ticker}"}
        
        prompt = f"""
As Sherlok, provide actionable investment insights for {ticker}.

Company Data:
- Sector: {stock_data.get('sector', 'N/A')}
- Industry: {stock_data.get('industry', 'N/A')}
- Current Price: ${stock_data.get('current_price', 'N/A')}
- Market Cap: ${stock_data.get('market_cap', 'N/A'):,}
- P/E Ratio: {stock_data.get('pe_ratio', 'N/A')}
- Revenue Growth: {stock_data.get('revenue_growth', 'N/A')}

Provide actionable insights:
1. Entry Points: When to consider buying
2. Exit Strategy: Price targets and stop-loss recommendations
3. Risk Management: Position sizing suggestions
4. Timeline: Short-term vs. long-term outlook
5. Catalysts to Watch: Upcoming events or milestones

Be specific and practical for a retail investor.
"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Sherlok, providing actionable investment insights."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=900
            )
            
            insights_text = response.choices[0].message.content
            
            return {
                'ticker': ticker,
                'insights': insights_text,
                'stock_data': {
                    'price': stock_data.get('current_price'),
                    'market_cap': stock_data.get('market_cap'),
                    'sector': stock_data.get('sector')
                },
                'timestamp': response.created
            }
        except Exception as e:
            return {'error': f"Insights generation failed: {str(e)}"}
    
    def discover_midcap_companies(self, limit: int = 15) -> List[str]:
        """
        Discover mid-cap companies (market cap between 2B and 10B)
        
        Args:
            limit: Maximum number of companies to return (default: 15)
            
        Returns:
            List of ticker symbols for mid-cap companies
        """
        # Expanded list of potential mid-cap tech companies
        # In production, this would query a real-time market data API
        potential_tickers = [
            'PLTR', 'SNOW', 'CRWD', 'NET', 'DDOG', 'ZS', 'OKTA', 'FTNT',
            'PANW', 'MDB', 'TEAM', 'WDAY', 'DOCU', 'TWLO', 'SHOP',
            'SQ', 'UBER', 'LYFT', 'COIN', 'RBLX', 'U', 'PATH',
            'BILL', 'PCTY', 'HUBS', 'ZM', 'ESTC', 'CFLT', 'S', 'FROG'
        ]
        
        midcap_companies = []
        
        for ticker in potential_tickers:
            if len(midcap_companies) >= limit:
                break
                
            try:
                stock_data = self._get_stock_data(ticker)
                
                # Check if it's in the mid-cap range (2B - 10B)
                if 'error' not in stock_data:
                    market_cap = stock_data.get('market_cap', 0)
                    if isinstance(market_cap, (int, float)) and 2e9 <= market_cap <= 10e9:
                        midcap_companies.append(ticker)
            except Exception:
                # Skip tickers that fail
                continue
        
        return midcap_companies
    
    def get_ticker_metrics(self, ticker: str) -> Dict:
        """
        Get computed metrics for a ticker
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dict with computed metrics or error
        """
        try:
            # Get stock data with price history
            stock_data = self._get_stock_data(ticker, include_history=True)
            
            if 'error' in stock_data:
                return {'error': f"Failed to fetch data for {ticker}"}
            
            # Extract price history
            price_history = stock_data.pop('price_history', None)
            
            # Compute metrics
            metrics = compute_metrics(price_history, stock_data)
            
            return metrics
        except Exception as e:
            return {'error': f"Metrics computation failed: {str(e)}"}
    
    def analyze_multiple_companies_llm(self, query: str, results: List[Dict]) -> Dict:
        """
        Use LLM to compare multiple companies and produce ranked Top 3 picks
        
        Args:
            query: User's query/request
            results: List of company analysis results with metrics
            
        Returns:
            Dict with query_interpreted, top_3_companies, and spoken_summary
        """
        # Build a summary of all companies for the LLM
        companies_summary = []
        
        for result in results:
            if 'error' in result:
                continue
                
            ticker = result.get('ticker', 'N/A')
            company_name = result.get('company_name', ticker)
            stock_data = result.get('stock_data', {})
            metrics = result.get('metrics', {})
            
            # Extract key information
            company_info = {
                'ticker': ticker,
                'company_name': company_name,
                'sector': stock_data.get('sector', 'N/A'),
                'market_cap': stock_data.get('market_cap', 'N/A'),
                'current_price': stock_data.get('current_price', 'N/A'),
                'recent_trend': stock_data.get('recent_trend', 'N/A'),
                'metrics': {
                    'weekly_change': metrics.get('weekly_change', 0),
                    'monthly_change': metrics.get('monthly_change', 0),
                    'six_month_trend_slope': metrics.get('six_month_trend_slope', 0),
                    'volatility': metrics.get('volatility', 0),
                    'revenue_growth_yoy': metrics.get('revenue_growth_yoy', 0),
                    'growth_score': metrics.get('growth_score', 0)
                }
            }
            companies_summary.append(company_info)
        
        # Create the prompt for OpenAI
        prompt = f"""You are StockSherlok, an investment insight agent.
You do NOT give financial advice. You only analyze and compare companies.

User Query: {query}

Companies to Analyze:
{json.dumps(companies_summary, indent=2)}

Your task:
1. Understand the user query
2. Compare all provided companies using their metrics:
   - weekly_change: % change over last 7 days
   - monthly_change: % change over last 30 days
   - six_month_trend_slope: trend direction (higher is better)
   - volatility: price stability (lower is better)
   - revenue_growth_yoy: year-over-year revenue growth
   - growth_score: composite score (0-10, higher is better)
3. Rank companies by growth potential
4. Select the TOP 3 companies
5. Explain WHY each one stands out
6. Keep explanations simple and friendly
7. Create a spoken_summary (1-2 sentences per company)

Return ONLY valid JSON in this exact format:
{{
  "query_interpreted": "brief interpretation of what user is looking for",
  "top_3_companies": [
    {{
      "ticker": "TICKER",
      "company_name": "Company Name",
      "growth_score": "X.X",
      "why_selected": "Clear explanation of why this company was selected",
      "risk_label": "Low/Medium/High"
    }}
  ],
  "spoken_summary": "Conversational summary of the top 3 picks in 2-3 sentences"
}}"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are StockSherlok, an AI that analyzes and compares companies. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse the response
            llm_response = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                parsed_result = json.loads(llm_response)
                return parsed_result
            except json.JSONDecodeError:
                # If parsing fails, return a structured error
                return {
                    'query_interpreted': query,
                    'top_3_companies': [],
                    'spoken_summary': 'Unable to generate comparison. Please try again.',
                    'error': 'Failed to parse LLM response as JSON'
                }
                
        except openai.RateLimitError:
            return {
                'query_interpreted': query,
                'top_3_companies': [],
                'spoken_summary': 'API rate limit exceeded. Please try again in a moment.',
                'error': 'Rate limit exceeded'
            }
        except openai.AuthenticationError:
            return {
                'query_interpreted': query,
                'top_3_companies': [],
                'spoken_summary': 'Authentication failed. Please check API key.',
                'error': 'Authentication failed'
            }
        except Exception as e:
            return {
                'query_interpreted': query,
                'top_3_companies': [],
                'spoken_summary': f'Analysis failed: {str(e)}',
                'error': str(e)
            }
