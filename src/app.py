import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
from stock_analyzer import StockAnalyzer
from utils import format_currency, format_percentage, validate_symbol

# Configure page
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = ""

def main():
    st.title("📈 Stock Analysis Dashboard")
    st.markdown("### Professional Financial Data Analysis with Yahoo Finance")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Stock Selection")
        
        # Stock symbol input
        symbol = st.text_input(
            "Enter Stock Symbol",
            value=st.session_state.current_symbol,
            placeholder="e.g., AAPL, MSFT, GOOGL",
            help="Enter a valid stock ticker symbol"
        ).upper()
        
        # Timeframe selection
        timeframe_options = {
            "1 Month": "1mo",
            "3 Months": "3mo", 
            "6 Months": "6mo",
            "1 Year": "1y",
            "2 Years": "2y",
            "5 Years": "5y"
        }
        
        selected_timeframe = st.selectbox(
            "Select Timeframe",
            options=list(timeframe_options.keys()),
            index=3  # Default to 1 Year
        )
        
        # Chart type selection
        chart_type = st.selectbox(
            "Chart Type",
            options=["Line Chart", "Candlestick Chart"],
            index=0
        )
        
        # Analyze button
        analyze_button = st.button("🔍 Analyze Stock", type="primary")
        
        # Download section
        st.markdown("---")
        st.header("Data Export")
        
        if st.session_state.stock_data is not None:
            # CSV download button
            csv_data = prepare_csv_download()
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"{st.session_state.current_symbol}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    # Main content area
    if analyze_button and symbol:
        if validate_symbol(symbol):
            st.session_state.current_symbol = symbol
            analyze_stock(symbol, timeframe_options[selected_timeframe], chart_type)
        else:
            st.error("❌ Please enter a valid stock symbol (e.g., AAPL, MSFT, GOOGL)")
    
    elif st.session_state.stock_data is not None:
        display_analysis(st.session_state.stock_data, chart_type)
    
    else:
        # Welcome screen
        st.info("👆 Enter a stock symbol in the sidebar to begin analysis")
        
        # Popular stocks quick access
        st.markdown("### Popular Stocks")
        col1, col2, col3, col4 = st.columns(4)
        
        popular_stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "META", "NVDA", "NFLX"]
        
        for i, stock in enumerate(popular_stocks):
            col = [col1, col2, col3, col4][i % 4]
            if col.button(f"📊 {stock}", key=f"popular_{stock}"):
                st.session_state.current_symbol = stock
                analyze_stock(stock, "1y", "Line Chart")

def analyze_stock(symbol, period, chart_type):
    """Analyze stock data and update session state"""
    
    with st.spinner(f"🔄 Fetching data for {symbol}..."):
        try:
            analyzer = StockAnalyzer()
            stock_data = analyzer.get_stock_data(symbol, period)
            
            if stock_data is None:
                st.error(f"❌ Unable to fetch data for symbol '{symbol}'. Please verify the symbol is correct.")
                return
            
            st.session_state.stock_data = stock_data
            display_analysis(stock_data, chart_type)
            
        except Exception as e:
            st.error(f"❌ Error analyzing stock: {str(e)}")

def display_analysis(stock_data, chart_type):
    """Display the complete stock analysis"""
    
    symbol = stock_data['info']['symbol']
    info = stock_data['info']
    history = stock_data['history']
    
    # Header with company info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## {info.get('longName', symbol)} ({symbol})")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')} | **Industry:** {info.get('industry', 'N/A')}")
    
    with col2:
        current_price = info.get('currentPrice', history['Close'].iloc[-1] if not history.empty else 0)
        st.metric("Current Price", format_currency(current_price))
    
    with col3:
        change_percent = info.get('regularMarketChangePercent', 0)
        st.metric("Change %", format_percentage(change_percent))
    
    # Key metrics row
    st.markdown("### Key Financial Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        market_cap = info.get('marketCap', 0)
        st.metric("Market Cap", f"${market_cap/1e9:.2f}B" if market_cap > 0 else "N/A")
    
    with col2:
        pe_ratio = info.get('trailingPE', 0)
        st.metric("P/E Ratio", f"{pe_ratio:.2f}" if pe_ratio and pe_ratio > 0 else "N/A")
    
    with col3:
        dividend_yield = info.get('dividendYield', 0)
        st.metric("Dividend Yield", format_percentage(dividend_yield * 100) if dividend_yield else "N/A")
    
    with col4:
        volume = info.get('volume', history['Volume'].iloc[-1] if not history.empty else 0)
        st.metric("Volume", f"{volume/1e6:.2f}M" if volume > 0 else "N/A")
    
    with col5:
        beta = info.get('beta', 0)
        st.metric("Beta", f"{beta:.2f}" if beta else "N/A")
    
    # Charts section
    if not history.empty:
        st.markdown("### Price Analysis")
        
        if chart_type == "Line Chart":
            display_line_chart(history, symbol)
        else:
            display_candlestick_chart(history, symbol)
        
        # Volume chart
        display_volume_chart(history, symbol)
        
        # Data table
        st.markdown("### Historical Data")
        display_data_table(history)
    
    else:
        st.warning("⚠️ No historical data available for this symbol")

def display_line_chart(history, symbol):
    """Display interactive line chart"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=history.index,
        y=history['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#00ff88', width=2),
        hovertemplate='<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{symbol} - Stock Price Trend",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_candlestick_chart(history, symbol):
    """Display interactive candlestick chart"""
    
    fig = go.Figure(data=go.Candlestick(
        x=history.index,
        open=history['Open'],
        high=history['High'],
        low=history['Low'],
        close=history['Close'],
        name=symbol,
        increasing_line_color='#00ff88',
        decreasing_line_color='#ff6b6b'
    ))
    
    fig.update_layout(
        title=f"{symbol} - Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        height=500,
        xaxis_rangeslider_visible=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_volume_chart(history, symbol):
    """Display volume chart"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=history.index,
        y=history['Volume'],
        name='Volume',
        marker_color='rgba(0, 255, 136, 0.6)',
        hovertemplate='<b>Date:</b> %{x}<br><b>Volume:</b> %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{symbol} - Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_dark",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_data_table(history):
    """Display historical data table"""
    
    # Prepare data for display
    display_data = history.copy()
    
    # Format columns
    price_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    for col in price_columns:
        if col in display_data.columns:
            display_data[col] = display_data[col].apply(lambda x: f"${x:.2f}")
    
    if 'Volume' in display_data.columns:
        display_data['Volume'] = display_data['Volume'].apply(lambda x: f"{x:,.0f}")
    
    # Reset index to show dates
    display_data = display_data.reset_index()
    display_data['Date'] = display_data['Date'].dt.strftime('%Y-%m-%d')
    
    # Show recent data first
    display_data = display_data.iloc[::-1].reset_index(drop=True)
    
    st.dataframe(
        display_data,
        use_container_width=True,
        height=400
    )

def prepare_csv_download():
    """Prepare CSV data for download"""
    
    if st.session_state.stock_data is None:
        return ""
    
    history = st.session_state.stock_data['history'].copy()
    info = st.session_state.stock_data['info']
    
    # Add metadata
    metadata_df = pd.DataFrame({
        'Metric': ['Symbol', 'Company Name', 'Sector', 'Industry', 'Market Cap', 'P/E Ratio', 'Beta'],
        'Value': [
            info.get('symbol', ''),
            info.get('longName', ''),
            info.get('sector', ''),
            info.get('industry', ''),
            info.get('marketCap', ''),
            info.get('trailingPE', ''),
            info.get('beta', '')
        ]
    })
    
    # Reset index for historical data
    history_df = history.reset_index()
    
    # Combine data
    output = io.StringIO()
    
    # Write metadata
    output.write("# Stock Analysis Report\n")
    output.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("\n# Company Information\n")
    metadata_df.to_csv(output, index=False)
    
    output.write("\n# Historical Price Data\n")
    history_df.to_csv(output, index=False)
    
    return output.getvalue()

if __name__ == "__main__":
    main()
