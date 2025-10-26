#!/usr/bin/env python3
"""
Financial Analysis Toolkit
A comprehensive set of tools for financial data analysis and visualization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import yfinance as yf

class FinancialAnalyzer:
    def __init__(self):
        self.data = None
        self.portfolio = {}
    
    def download_stock_data(self, ticker, period="1y"):
        """Download stock data from Yahoo Finance"""
        try:
            stock = yf.download(ticker, period=period)
            self.data = stock
            print(f"✅ Downloaded data for {ticker}")
            return stock
        except Exception as e:
            print(f"❌ Error downloading data: {e}")
            return None
    
    def calculate_returns(self):
        """Calculate daily and cumulative returns"""
        if self.data is None:
            print("❌ No data available. Download data first.")
            return None
        
        self.data['Daily Return'] = self.data['Adj Close'].pct_change()
        self.data['Cumulative Return'] = (1 + self.data['Daily Return']).cumprod()
        return self.data
    
    def plot_performance(self, ticker):
        """Plot stock performance"""
        if self.data is None:
            print("❌ No data available.")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Price chart
        ax1.plot(self.data.index, self.data['Adj Close'])
        ax1.set_title(f'{ticker} Stock Price')
        ax1.set_ylabel('Price ($)')
        ax1.grid(True)
        
        # Returns chart
        ax2.plot(self.data.index, self.data['Cumulative Return'])
        ax2.set_title(f'{ticker} Cumulative Returns')
        ax2.set_ylabel('Cumulative Return')
        ax2.set_xlabel('Date')
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(f'{ticker}_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def calculate_volatility(self, window=30):
        """Calculate rolling volatility"""
        if self.data is None:
            return None
        
        self.data['Volatility'] = self.data['Daily Return'].rolling(window=window).std() * np.sqrt(252)
        return self.data['Volatility'].iloc[-1]

# Example usage
if __name__ == "__main__":
    analyzer = FinancialAnalyzer()
    
    # Analyze Apple stock
    data = analyzer.download_stock_data("AAPL")
    
    if data is not None:
        analyzer.calculate_returns()
        volatility = analyzer.calculate_volatility()
        analyzer.plot_performance("AAPL")
        
        print(f"📊 Analysis Complete!")
        print(f"📈 Final Price: ${data['Adj Close'].iloc[-1]:.2f}")
        print(f"📉 Volatility: {volatility:.2%}")
