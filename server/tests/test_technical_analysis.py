import pytest
import pandas as pd
import numpy as np
from methods.technical_analysis import getHigh, getLow, analyzeGammaProxy, generateTradingSignal

def test_get_high():
    data = {
        "High": [100, 105, 102],
        "Low": [95, 98, 99],
        "Close": [98, 100, 101]
    }
    df = pd.DataFrame(data)
    # The function expects 'High' column. 
    # The function in technical_analysis.py does some column manipulation:
    # stock.columns = stock.columns.get_level_values(0)
    # This implies it typically receives a MultiIndex columns df from yfinance.
    # However, if we pass a single index df, get_level_values(0) might fail or just return the same.
    # Let's mock a MultiIndex to be safe or adjust the test df.
    
    # Actually, pandas Series/Index get_level_values works on single index too if level is 0.
    # But dataframe columns might need to be MultiIndex if that line is strictly executed.
    
    # Let's create a MultiIndex df to match the expected input format from yfinance
    columns = pd.MultiIndex.from_tuples([("High", ""), ("Low", ""), ("Close", "")])
    df = pd.DataFrame(
        [[100, 95, 98], [105, 98, 100], [102, 99, 101]],
        columns=columns
    )
    
    max_high = getHigh(df)
    assert max_high == 105

def test_get_low():
    columns = pd.MultiIndex.from_tuples([("High", ""), ("Low", ""), ("Close", "")])
    df = pd.DataFrame(
        [[100, 95, 98], [105, 90, 100], [102, 99, 101]],
        columns=columns
    )
    # Note: getLow implementation sorts by High(?!) but returns min of Low.
    # checking the code:
    # sortedDf = stock.sort_values(by="High", ascending=False)
    # minClose = sortedDf["Low"].min()
    # It returns the minimum low. Sorting by High doesn't affect min() result unless it takes the top/bottom element.
    # It takes .min(), so logic holds.
    
    min_low = getLow(df)
    assert min_low == 90

def test_analyze_gamma_proxy_balanced():
    current_price = 100
    calls = pd.DataFrame({
        'strike': [95, 100, 105],
        'openInterest': [100, 100, 100]
    })
    puts = pd.DataFrame({
        'strike': [95, 100, 105],
        'openInterest': [100, 100, 100]
    })
    
    remark = analyzeGammaProxy(current_price, calls, puts)
    assert "Options open interest is relatively balanced" in remark

def test_analyze_gamma_proxy_call_heavy():
    current_price = 100
    calls = pd.DataFrame({
        'strike': [95, 100, 105],
        'openInterest': [500, 500, 500]
    })
    puts = pd.DataFrame({
        'strike': [95, 100, 105],
        'openInterest': [100, 100, 100]
    })
    
    remark = analyzeGammaProxy(current_price, calls, puts)
    assert "Large call open interest" in remark

def test_generate_trading_signal_simple():
    current_price = 100
    rsi = 50
    moving_averages = {'SMA50': 90, 'SMA200': 80}
    support_levels = [90]
    resistance_levels = [110]
    fundamentals = {'trailingPE': 15, 'profitMargins': 0.15, 'debtToEquity': 50, 'returnOnEquity': 0.20}
    put_call_ratio = 0.5
    quarterly_fundamentals = [
        {'totalRevenue': 200, 'netIncome': 20},
        {'totalRevenue': 100, 'netIncome': 10}
    ]
    gamma_remark = "Neutral"
    
    # Just running to ensure no errors and getting a result
    rating, remark = generateTradingSignal(
        current_price, rsi, moving_averages, support_levels, resistance_levels,
        fundamentals, put_call_ratio, quarterly_fundamentals, gamma_remark
    )
    
    assert rating in ["Buy", "Sell", "Neutral"]
    assert isinstance(remark, str)
    assert len(remark) > 0
    # Expected: 
    # RSI 50 -> +1 (Healthy)
    # Price > SMA50 > SMA200 -> +6 (Bullish Trend)
    # (Price - SMA50)/SMA50 = 10/90 = 0.11 > 0.10 -> -2 (Overextended)
    # PE < 20 -> +3
    # Profit Margin > 0.10 -> +4
    # D/E < 100 -> +3
    # ROE > 0.15 -> +2
    # PCR < 0.7 -> +3
    # Revenue Growth -> +4
    # Income Growth -> +5
    # Total Score approx: 1+6-2+3+4+3+2+3+4+5 = 29 -> Buy
    assert rating == "Buy"

