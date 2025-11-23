# StockSherlok API Examples

This directory contains example scripts demonstrating how to use the StockSherlok API.

## Available Examples

### api_usage.py
Demonstrates core API functionality:
- Company analysis
- Market signal scanning
- Actionable insights

## Running Examples

Make sure the backend server is running first:

```bash
cd backend
python app.py
```

Then run the examples:

```bash
cd examples
python3 api_usage.py
```

## Custom Usage

You can also use the examples as a reference to build your own integrations:

```python
import requests

# Analyze a company
response = requests.post('http://localhost:5000/api/analyze', json={
    'ticker': 'AAPL'
})
print(response.json())
```
