import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class StockAnalyzer:
    """Stock analysis class using Yahoo Finance API"""
    
    def __init__(self):
        pass
    
    def get_stock_data(self, symbol, period="1y"):
        """
        Fetch comprehensive stock data from Yahoo Finance
        
        Args:
            symbol (str): Stock ticker symbol
            period (str): Time period for historical data
            
        Returns:
            dict: Dictionary containing stock info and historical data
        """
        try:
            # Create ticker object
            ticker = yf.Ticker(symbol)
            
            # Get stock info
            info = ticker.info
            
            # Validate that we got valid data
            if not info or 'symbol' not in info:
                return None
            
            # Get historical data
            history = ticker.history(period=period)
            
            if history.empty:
                return None
            
            # Get additional financial data
            financials = self._get_financial_data(ticker)
            
            return {
                'info': info,
                'history': history,
                'financials': financials,
                'symbol': symbol.upper()
            }
            
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def _get_financial_data(self, ticker):
        """Get additional financial data"""
        
        financial_data = {}
        
        try:
            # Get quarterly financials
            quarterly_financials = ticker.quarterly_financials
            if not quarterly_financials.empty:
                financial_data['quarterly_financials'] = quarterly_financials
            
            # Get balance sheet
            balance_sheet = ticker.balance_sheet
            if not balance_sheet.empty:
                financial_data['balance_sheet'] = balance_sheet
            
            # Get cash flow
            cashflow = ticker.cashflow
            if not cashflow.empty:
                financial_data['cashflow'] = cashflow
                
        except Exception as e:
            # Financial data is optional, don't fail if unavailable
            pass
        
        return financial_data
    
    def get_real_time_price(self, symbol):
        """Get real-time price data"""
        
        try:
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            
            if not todays_data.empty:
                return {
                    'current_price': todays_data['Close'].iloc[-1],
                    'open_price': todays_data['Open'].iloc[-1],
                    'high_price': todays_data['High'].iloc[-1],
                    'low_price': todays_data['Low'].iloc[-1],
                    'volume': todays_data['Volume'].iloc[-1]
                }
            
        except Exception as e:
            st.error(f"Error fetching real-time data for {symbol}: {str(e)}")
            
        return None
    
    def calculate_technical_indicators(self, history):
        """Calculate basic technical indicators"""
        
        if history.empty:
            return {}
        
        indicators = {}
        
        try:
            # Simple Moving Averages
            indicators['SMA_20'] = history['Close'].rolling(window=20).mean()
            indicators['SMA_50'] = history['Close'].rolling(window=50).mean()
            indicators['SMA_200'] = history['Close'].rolling(window=200).mean()
            
            # Exponential Moving Average
            indicators['EMA_12'] = history['Close'].ewm(span=12).mean()
            indicators['EMA_26'] = history['Close'].ewm(span=26).mean()
            
            # MACD
            indicators['MACD'] = indicators['EMA_12'] - indicators['EMA_26']
            indicators['MACD_Signal'] = indicators['MACD'].ewm(span=9).mean()
            
            # RSI (Relative Strength Index)
            delta = history['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            indicators['RSI'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            sma_20 = indicators['SMA_20']
            std_20 = history['Close'].rolling(window=20).std()
            indicators['Bollinger_Upper'] = sma_20 + (std_20 * 2)
            indicators['Bollinger_Lower'] = sma_20 - (std_20 * 2)
            
        except Exception as e:
            st.warning(f"Error calculating technical indicators: {str(e)}")
        
        return indicators
    
    def get_company_news(self, symbol):
        """Get recent news for the company"""
        
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if news:
                return news[:5]  # Return top 5 news items
                
        except Exception as e:
            st.warning(f"Error fetching news for {symbol}: {str(e)}")
        
        return []
    
    def compare_stocks(self, symbols, period="1y"):
        """Compare multiple stocks"""
        
        comparison_data = {}
        
        for symbol in symbols:
            stock_data = self.get_stock_data(symbol, period)
            if stock_data:
                comparison_data[symbol] = stock_data
        
        return comparison_data
    
    def get_market_summary(self):
        """Get major market indices summary"""
        
        indices = {
            "S&P 500": "^GSPC",
            "Dow Jones": "^DJI", 
            "NASDAQ": "^IXIC",
            "Russell 2000": "^RUT"
        }
        
        market_data = {}
        
        for name, symbol in indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2] if len(hist) > 1 else current
                    change = current - previous
                    change_pct = (change / previous) * 100
                    
                    market_data[name] = {
                        'current': current,
                        'change': change,
                        'change_pct': change_pct
                    }
                    
            except Exception as e:
                continue
        
        return market_data
