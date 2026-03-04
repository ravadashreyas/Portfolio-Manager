import plotly.graph_objects as go
import yfinance as yf
import numpy as np


MAX_CACHE_SIZE = 5
cache = {}

def optionsData(ticker):
    if (ticker in cache):
        print("Options cache used")
        data = cache.pop(ticker)
        cache[ticker] = data
        callsDict, putsDict, callFig, putFig = cache[ticker]
        return callsDict, putsDict, callFig, putFig
    else:
        if (len(cache) >= MAX_CACHE_SIZE) and (ticker not in cache):
            oldest_ticker = next(iter(cache))
            del cache[oldest_ticker]
            print(f"Cache full. Evicted oldest Options: {oldest_ticker}")

        stockData = yf.Ticker(ticker)
        avaExp = stockData.options

        if not avaExp:
            print(f"No options data available for {ticker}.")
            return None, None, None, None
        first_expiry = avaExp[0]
        opt_chain = stockData.option_chain(first_expiry)
        calls = opt_chain.calls
        puts = opt_chain.puts

        if calls.empty and puts.empty:
                print(f"Option chain for {ticker} is empty.")
                return None, None
        if calls.empty:
                print(f"Calls data is empty for {ticker}.")
                return None, None
        if puts.empty:
                print(f"Puts data is empty for {ticker}.")
                return None, None
        
        calls = calls.replace({np.nan: None})
        puts = puts.replace({np.nan: None})
        callsDict = calls.to_dict(orient='records')
        putsDict = puts.to_dict(orient='records')
        callGraph = "callGraph"
        putGraph = "putGraph"
        callFig = plotBarGraph(callsDict, ticker, callGraph)
        putFig = plotBarGraph(putsDict, ticker, putGraph)

        cache[ticker] = callsDict, putsDict, callFig, putFig
        
        return callsDict, putsDict, callFig, putFig

def plotBarGraph(options, ticker, graphType):
    ticker = ticker
    current_price = yf.Ticker(ticker).info.get("currentPrice")
    min_strike = current_price * 0.8
    max_strike = current_price * 1.2
    stockOptions = options
    filteredOptions = []
    for i in options: 
        if i['strike'] >= min_strike and i['strike'] <= max_strike:
            filteredOptions.append(i)
    
    if not filteredOptions:
        print(f"No options data found in the strike range {min_strike}-{max_strike}")
        return
    
    color = ''
    if graphType == "putGraph":
       color = 'red'
    elif graphType == "callGraph":
        color = 'green'
       
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[i['volume'] for i in filteredOptions],
        y=[i['strike'] for i in filteredOptions],
        name='Options Data',
        marker_color=color,
        orientation='h'
    ))
    fig.update_layout(
        template='plotly_dark',
        xaxis_title='Volume',
        yaxis_title='Strike Price',
        width=700,
        height=400
    )
    return fig

def plotBarGraph(options, ticker, graphType):
    ticker = ticker
    current_price = yf.Ticker(ticker).info.get("currentPrice")
    min_strike = current_price * 0.8
    max_strike = current_price * 1.2
    stockOptions = options
    filteredOptions = []
    for i in options: 
        if i['strike'] >= min_strike and i['strike'] <= max_strike:
            filteredOptions.append(i)
    
    if not filteredOptions:
        print(f"No options data found in the strike range {min_strike}-{max_strike}")
        return
    
    color = ''
    if graphType == "putGraph":
       color = 'red'
    elif graphType == "callGraph":
        color = 'green'
       
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[i['volume'] for i in filteredOptions],
        y=[i['strike'] for i in filteredOptions],
        name='Options Data',
        marker_color=color,
        orientation='h'
    ))
    fig.update_layout(
        template='plotly_dark',
        xaxis_title='Volume',
        yaxis_title='Strike Price',
        width=700,
        height=400
    )
    return fig