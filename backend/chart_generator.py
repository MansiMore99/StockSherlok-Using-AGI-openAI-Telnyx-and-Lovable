"""
Chart Generator - Creates comparison charts as base64 PNG images
"""
import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from typing import List, Dict, Optional


def generate_bar_chart(title: str, labels: List[str], values: List[float], ylabel: str) -> Dict:
    """
    Generate a bar chart and return as base64-encoded PNG
    
    Args:
        title: Chart title
        labels: X-axis labels (company tickers)
        values: Y-axis values (metric values)
        ylabel: Y-axis label
        
    Returns:
        Dict with chart_type, title, and image_base64
    """
    try:
        # Validate inputs
        if not labels or not values:
            return {
                "chart_type": "bar",
                "title": title,
                "image_base64": "",
                "error": "No data provided for chart"
            }
        
        if len(labels) != len(values):
            return {
                "chart_type": "bar",
                "title": title,
                "image_base64": "",
                "error": "Labels and values length mismatch"
            }
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Create bar chart
        bars = ax.bar(labels, values)
        
        # Customize chart
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_xlabel('Company', fontsize=12)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            if height != 0:  # Only show label if value is not zero
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', fontsize=9)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        
        # Encode to base64
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        # Close the plot to free memory
        plt.close(fig)
        
        return {
            "chart_type": "bar",
            "title": title,
            "image_base64": image_base64
        }
        
    except Exception as e:
        # Return error structure if chart generation fails
        plt.close('all')  # Clean up any open figures
        return {
            "chart_type": "bar",
            "title": title,
            "image_base64": "",
            "error": f"Chart generation failed: {str(e)}"
        }


def generate_comparison_charts(companies_data: List[Dict]) -> List[Dict]:
    """
    Generate multiple comparison charts for a list of companies
    
    Args:
        companies_data: List of dicts with ticker, metrics, and stock_data
        
    Returns:
        List of chart dictionaries
    """
    charts = []
    
    # Extract data for charts
    tickers = []
    market_caps = []
    monthly_changes = []
    revenue_growths = []
    
    for company in companies_data:
        if 'error' in company:
            continue
            
        ticker = company.get('ticker', 'N/A')
        metrics = company.get('metrics', {})
        stock_data = company.get('stock_data', {})
        
        tickers.append(ticker)
        
        # Market cap (convert to billions for readability)
        market_cap = stock_data.get('market_cap', 0)
        if isinstance(market_cap, (int, float)) and market_cap > 0:
            market_caps.append(market_cap / 1e9)  # Convert to billions
        else:
            market_caps.append(0)
        
        # Monthly change
        monthly_change = metrics.get('monthly_change', 0)
        monthly_changes.append(monthly_change if isinstance(monthly_change, (int, float)) else 0)
        
        # Revenue growth (convert to percentage)
        revenue_growth = metrics.get('revenue_growth_yoy', 0)
        if isinstance(revenue_growth, (int, float)):
            revenue_growths.append(revenue_growth * 100)  # Convert to percentage
        else:
            revenue_growths.append(0)
    
    # Generate charts only if we have data
    if tickers:
        # Chart 1: Market Cap Comparison
        if any(cap > 0 for cap in market_caps):
            market_cap_chart = generate_bar_chart(
                title="Market Cap Comparison",
                labels=tickers,
                values=market_caps,
                ylabel="Market Cap (Billions USD)"
            )
            charts.append({
                **market_cap_chart,
                "metric": "market_cap"
            })
        
        # Chart 2: Monthly % Change
        monthly_change_chart = generate_bar_chart(
            title="Monthly Price Change (%)",
            labels=tickers,
            values=monthly_changes,
            ylabel="Change (%)"
        )
        charts.append({
            **monthly_change_chart,
            "metric": "monthly_change"
        })
        
        # Chart 3: Revenue Growth YoY
        revenue_growth_chart = generate_bar_chart(
            title="Revenue Growth Year-over-Year",
            labels=tickers,
            values=revenue_growths,
            ylabel="Growth (%)"
        )
        charts.append({
            **revenue_growth_chart,
            "metric": "revenue_growth_yoy"
        })
    
    return charts
