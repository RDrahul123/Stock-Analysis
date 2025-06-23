# Stock Analysis Dashboard - Deployment Guide

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

3. **Access the App**:
   Open your browser to `http://localhost:8501`

## Streamlit Cloud Deployment

1. Upload this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file: `app.py`
5. Deploy

## Features

- Dark theme with professional styling
- Real-time stock data from Yahoo Finance
- Interactive charts (line and candlestick)
- Key financial metrics display
- CSV export functionality
- Popular stocks quick access

## File Structure

```
├── app.py                    # Main Streamlit application
├── stock_analyzer.py         # Stock data analysis logic
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README.md                # Project documentation
├── LICENSE                  # MIT License
└── .gitignore              # Git ignore rules
```