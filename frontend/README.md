# StockSherlok Frontend

React-based frontend for the StockSherlok AI research agent.

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The app will open at http://localhost:3000

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Configuration

Create a `.env` file to configure the API URL:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

## Features

- **Company Analysis**: Search and analyze any stock ticker
- **Market Scanning**: Discover promising companies by sector
- **Actionable Insights**: Get entry/exit strategies and catalysts
- **Responsive Design**: Works on desktop and mobile devices

## Components

- `App.js` - Main application component
- `App.css` - Component styles
- `index.js` - React entry point
- `index.css` - Global styles
