#!/usr/bin/env python3
"""
Example script demonstrating how to use the StockSherlok API
"""
import requests
import json
import sys

# Configuration
API_BASE_URL = "http://localhost:5000/api"


def check_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is healthy and running")
            return True
        else:
            print("❌ API returned error:", response.status_code)
            return False
    except Exception as e:
        print("❌ Cannot connect to API:", str(e))
        return False


def analyze_company(ticker):
    """Analyze a company by ticker symbol"""
    print(f"\n🔍 Analyzing {ticker}...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={"ticker": ticker}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Analysis for {ticker}:")
            print("=" * 60)
            
            if 'analysis' in data:
                analysis = data['analysis']
                if isinstance(analysis, dict):
                    # Print structured analysis
                    print(f"\nTicker: {analysis.get('ticker', ticker)}")
                    print(f"Company: {analysis.get('company_name', 'N/A')}")
                    print(f"\nAnalysis Text:")
                    print(analysis.get('analysis', 'No analysis available'))
                else:
                    # Print raw analysis
                    print(json.dumps(analysis, indent=2))
            else:
                print(json.dumps(data, indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Error analyzing company: {str(e)}")


def scan_market(sector="technology"):
    """Scan market for promising signals"""
    print(f"\n🎯 Scanning {sector} sector...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/scan",
            json={"sector": sector, "market_cap": "mid"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n🔍 Market Signals - {sector.title()} Sector:")
            print("=" * 60)
            
            if 'signals' in data:
                signals_data = data['signals']
                if isinstance(signals_data, dict) and 'signals' in signals_data:
                    signals = signals_data['signals']
                else:
                    signals = signals_data
                
                for signal in signals:
                    print(f"\n📈 {signal['ticker']}")
                    print(f"   Score: {signal['score']}/100")
                    print(f"   Price: ${signal['current_price']}")
                    print(f"   Sector: {signal.get('sector', 'N/A')}")
                    print(f"   Reasons:")
                    for reason in signal.get('reasons', []):
                        print(f"      ✓ {reason}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Error scanning market: {str(e)}")


def get_insights(ticker):
    """Get actionable insights for a ticker"""
    print(f"\n💡 Getting insights for {ticker}...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/insights",
            json={"ticker": ticker}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n💡 Insights for {ticker}:")
            print("=" * 60)
            
            if 'insights' in data:
                insights = data['insights']
                if isinstance(insights, dict):
                    print(f"\nInsights Text:")
                    print(insights.get('insights', 'No insights available'))
                else:
                    print(insights)
            else:
                print(json.dumps(data, indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"❌ Error getting insights: {str(e)}")


def main():
    """Main function to run examples"""
    print("=" * 60)
    print("🔍 StockSherlok API - Example Usage")
    print("=" * 60)
    
    # Check API health
    if not check_health():
        print("\n⚠️  Make sure the backend server is running!")
        print("Run: cd backend && python app.py")
        sys.exit(1)
    
    # Example 1: Analyze a company
    analyze_company("PLTR")
    
    # Example 2: Scan market signals
    scan_market("technology")
    
    # Example 3: Get actionable insights
    get_insights("PLTR")
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
