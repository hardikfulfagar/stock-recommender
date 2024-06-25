# Stock Recommender Chrome Extension

A Chrome extension that computes RSI-based buy/sell recommendations for the top 50 S&P 500 companies based on the latest stock prices.

## Features

- Computes RSI values for the top 50 S&P 500 stocks.
- Provides buy/sell recommendations based on RSI.
- Displays company names, ticker symbols, current prices, and RSI values.
- Uses Bootstrap for a clean UI.

## Installation

### Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/stock-recommender.git
   cd stock-recommender
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies and run the server:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

### Chrome Extension Setup

1. Open Chrome and go to `chrome://extensions/`.
2. Enable "Developer mode".
3. Click "Load unpacked" and select the `chrome_extension` directory.

## Usage

1. Open the extension and click "Fetch".
2. View computed RSI values, stock prices, and recommendations.
