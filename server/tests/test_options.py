import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
from methods.Options.options import optionsData, plotBarGraph, cache

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()

@patch('methods.Options.options.yf.Ticker')
def test_optionsData_success(mock_ticker):
    # Setup mock data
    ticker_val = "AAPL"
    mock_stock = MagicMock()
    mock_ticker.return_value = mock_stock
    
    mock_stock.options = ['2024-01-01']
    
    calls_df = pd.DataFrame({
        'strike': [150.0, 160.0],
        'volume': [100, 200]
    })
    puts_df = pd.DataFrame({
        'strike': [140.0, 130.0],
        'volume': [50, 60]
    })
    
    mock_chain = MagicMock()
    mock_chain.calls = calls_df
    mock_chain.puts = puts_df
    mock_stock.option_chain.return_value = mock_chain
    
    # Mock Ticker info for plotBarGraph
    mock_stock.info = {'currentPrice': 150}

    # Run function
    callsDict, putsDict, callFig, putFig = optionsData(ticker_val)

    # Verification
    assert len(callsDict) == 2
    assert len(putsDict) == 2
    assert ticker_val in cache
    assert callFig is not None
    assert putFig is not None

@patch('methods.Options.options.yf.Ticker')
def test_optionsData_no_options(mock_ticker):
    mock_stock = MagicMock()
    mock_ticker.return_value = mock_stock
    mock_stock.options = []

    callsDict, putsDict, callFig, putFig = optionsData("INVALID")
    
    assert callsDict is None
    assert putsDict is None
    assert callFig is None
    assert putFig is None

@patch('methods.Options.options.yf.Ticker')
def test_optionsData_cache_logic(mock_ticker):
    ticker_val = "MSFT"
    mock_stock = MagicMock()
    mock_ticker.return_value = mock_stock
    mock_stock.options = ['2024-01-01']
    mock_stock.info = {'currentPrice': 200}
    
    mock_chain = MagicMock()
    mock_chain.calls = pd.DataFrame({'strike': [200], 'volume': [10]})
    mock_chain.puts = pd.DataFrame({'strike': [190], 'volume': [20]})
    mock_stock.option_chain.return_value = mock_chain

    # First call - populates cache
    optionsData(ticker_val)
    assert mock_ticker.call_count == 3
    
    # Second call - should use cache
    optionsData(ticker_val)
    # yf.Ticker is not called again because it returns from cache early
    assert mock_ticker.call_count == 3

@patch('methods.Options.options.yf.Ticker')
def test_plotBarGraph_filtering(mock_ticker):
    mock_stock = MagicMock()
    mock_ticker.return_value = mock_stock
    mock_stock.info = {'currentPrice': 100} # Range: 80 to 120
    
    options = [
        {'strike': 70, 'volume': 10},  # Filtered out
        {'strike': 90, 'volume': 20},  # Kept
        {'strike': 110, 'volume': 30}, # Kept
        {'strike': 130, 'volume': 40}  # Filtered out
    ]
    
    fig = plotBarGraph(options, "AAPL", "callGraph")
    
    assert fig is not None
    # Check data in figure
    assert list(fig.data[0].y) == [90, 110]
    assert list(fig.data[0].x) == [20, 30]
    assert fig.data[0].marker.color == 'green'

@patch('methods.Options.options.yf.Ticker')
def test_plotBarGraph_no_data_in_range(mock_ticker):
    mock_stock = MagicMock()
    mock_ticker.return_value = mock_stock
    mock_stock.info = {'currentPrice': 100}
    
    options = [{'strike': 50, 'volume': 10}]
    fig = plotBarGraph(options, "AAPL", "callGraph")
    
    assert fig is None
