from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
import plotly.graph_objects as go
from methods.plot_main import plotGraphW

@pytest.fixture
def mock_stock_data():
    # Create a sample DataFrame that mimics yfinance output
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    data = {
        "Open": [100 + i for i in range(100)],
        "High": [105 + i for i in range(100)],
        "Low": [95 + i for i in range(100)],
        "Close": [102 + i for i in range(100)],
        "Volume": [1000 for _ in range(100)],
    }
    df = pd.DataFrame(data, index=dates)
    return df

@patch("methods.plot_main.yf.download")
def test_plot_graph_w_all(mock_download, mock_stock_data):
    # Test "ALL" timeframe
    mock_download.return_value = mock_stock_data
    
    fig = plotGraphW("AAPL", "ALL")
    
    assert fig is not None
    assert isinstance(fig, go.Figure)
    # Check if traces are added (Candlestick or Scatter based on implementation, here it seems to be Scatter)
    assert len(fig.data) > 0
    assert fig.data[0].name == "Close Price"

@patch("methods.plot_main.yf.download")
def test_plot_graph_w_5y(mock_download, mock_stock_data):
    # Test "5Y" timeframe
    mock_download.return_value = mock_stock_data
    
    fig = plotGraphW("AAPL", "5Y")
    
    assert fig is not None
    assert isinstance(fig, go.Figure)

@patch("methods.plot_main.yf.download")
def test_plot_graph_w_no_data(mock_download):
    # Test case where no data is returned
    mock_download.return_value = pd.DataFrame()
    
    fig = plotGraphW("INVALID", "1D")
    
    assert fig is None

@patch("methods.plot_main.yf.download")
def test_plot_graph_w_indicators(mock_download, mock_stock_data):
    # Test if indicators (SMA, VWAP) are calculated and added to the plot
    mock_download.return_value = mock_stock_data.copy()
    
    fig = plotGraphW("AAPL", "1Y")
    
    # We expect traces for Close, SMA 20, SMA 50, SMA 200, VWAP if data allows
    # With 100 points, SMA 20 and 50 should be there. SMA 200 might not be fully populated if not enough data, 
    # but the code handles na.
    
    trace_names = [trace.name for trace in fig.data]
    assert "Close Price" in trace_names
    assert "SMA 20" in trace_names
    assert "SMA 50" in trace_names
    # SMA 200 needs 200 points, our mock has 100, so it might not be there or be empty/handled safely.
    assert "VWAP" in trace_names
