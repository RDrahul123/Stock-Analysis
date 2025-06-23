# Stock Analysis Dashboard

A professional dark-themed Streamlit web application for comprehensive stock analysis using Yahoo Finance data.

![Stock Analysis Dashboard](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Yahoo Finance](https://img.shields.io/badge/Yahoo%20Finance-720E9E?style=for-the-badge&logo=yahoo&logoColor=white)

## Features

- **Real-time Stock Data**: Fetch live stock information from Yahoo Finance
- **Interactive Charts**: Line charts and candlestick charts with Plotly
- **Financial Metrics**: Key metrics including market cap, P/E ratio, dividend yield, and more
- **Multiple Timeframes**: Analyze data from 1 month to 5 years
- **Volume Analysis**: Trading volume visualization
- **CSV Export**: Download historical data and analysis reports
- **Dark Theme**: Professional dark interface with green accent colors
- **Popular Stocks**: Quick access buttons for major stocks

## Screenshots

The dashboard provides a clean, professional interface for stock analysis with:
- Sidebar controls for stock selection
- Interactive price charts
- Key financial metrics display
- Historical data table
- CSV export functionality

<img width="881" alt="Screen1" src="https://github.com/user-attachments/assets/82031e63-c956-4752-910e-ea0255f6a6d8" />


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-analysis-dashboard.git
cd stock-analysis-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Usage

1. **Enter Stock Symbol**: Type a stock ticker symbol (e.g., AAPL, MSFT, GOOGL) in the sidebar
2. **Select Timeframe**: Choose from 1 month to 5 years of historical data
3. **Choose Chart Type**: Select between line chart or candlestick chart
4. **Analyze**: Click the "Analyze Stock" button to fetch and display data
5. **Export Data**: Use the CSV download button to export analysis results

### Popular Stocks Quick Access

The dashboard includes quick access buttons for popular stocks:
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Google)
- TSLA (Tesla)
- AMZN (Amazon)
- META (Meta)
- NVDA (NVIDIA)
- NFLX (Netflix)

## Technical Details

### Architecture

- **Frontend**: Streamlit web framework
- **Data Source**: Yahoo Finance API via yfinance library
- **Visualization**: Plotly for interactive charts
- **Data Processing**: Pandas for data manipulation

### Key Components

- `app.py`: Main Streamlit application
- `stock_analyzer.py`: Stock data retrieval and analysis logic
- `utils.py`: Utility functions for data formatting and validation
- `.streamlit/config.toml`: Streamlit configuration with dark theme

### Dependencies

- streamlit: Web application framework
- yfinance: Yahoo Finance API client
- pandas: Data manipulation and analysis
- plotly: Interactive visualization library
- numpy: Numerical computing support

## Configuration

The application uses a dark theme configuration in `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "dark"
primaryColor = "#00ff88"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

## Data Export

The application provides comprehensive CSV export functionality including:
- Company information and metadata
- Historical price data (OHLCV)
- Generated timestamps
- All key financial metrics

## Error Handling

The application includes robust error handling for:
- Invalid stock symbols
- Network connectivity issues
- Missing or incomplete data
- API rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is for educational and informational purposes only. It should not be used as the sole basis for investment decisions. Always consult with a qualified financial advisor before making investment decisions.

## Acknowledgments

- Yahoo Finance for providing free financial data
- Streamlit for the excellent web framework
- Plotly for interactive visualization capabilities
- The open-source Python community

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
