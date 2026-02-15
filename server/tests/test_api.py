from unittest.mock import MagicMock, patch
import json
import pytest

@patch("routes.api.plotGraphW")
def test_get_plot(mock_plot, client):
    # Mock return value of plotGraphW
    # It returns a plotly figure, then to_json() is called on it.
    mock_fig = MagicMock()
    mock_fig.to_json.return_value = json.dumps({"data": [], "layout": {}})
    mock_plot.return_value = mock_fig
    
    response = client.post("/api/plot", json={
        "ticker": "AAPL",
        "timeFrame": "1D"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data
    assert "layout" in data

@patch("routes.api.plotGraphW")
def test_get_plot_error(mock_plot, client):
    # Test error case (None returned)
    mock_plot.return_value = None
    
    response = client.post("/api/plot", json={
        "ticker": "INVALID",
        "timeFrame": "1D"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No data found for ticker"

@patch("routes.api.tecAnalysis")
def test_get_analysis(mock_analysis, client):
    # Mock return value of tecAnalysis
    mock_analysis.return_value = {
        "rating": "Buy",
        "remark": "Good stuff",
        "weekHigh": 150
    }
    
    response = client.post("/api/analysis", json={
        "ticker": "AAPL"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert "analysis" in data
    assert data["analysis"]["rating"] == "Buy"

@patch("routes.api.tecAnalysis")
def test_get_analysis_error(mock_analysis, client):
    # Test error case
    mock_analysis.return_value = None
    
    response = client.post("/api/analysis", json={
        "ticker": "INVALID"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert "error" in data
