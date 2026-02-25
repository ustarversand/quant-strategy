#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
均线策略参数优化 - 50日/200日
"""

import yfinance as yf
import pandas as pd
import numpy as np

STOCKS = {
    '紫金矿业': '601899.SS',
    '剑桥科技': '603083.SS', 
    '兴业银锡': '600737.SS',
    '铜陵有色': '000630.SZ',
    '英维克': '002837.SZ'
}

# 测试不同参数组合
PARAM_SETS = [
    (20, 50),
    (50, 100),
    (50, 200),
    (10, 30),
]

def download_data(ticker, period='3y'):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def backtest_ma(df, short, long):
    df = df.copy()
    df['SMA_short'] = df['Close'].rolling(window=short).mean()
    df['SMA_long'] = df['Close'].rolling(window=long).mean()
    df['Signal'] = np.where(df['SMA_short'] > df['SMA_long'], 1, -1)
    df['Position'] = df['Signal'].shift(1)
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Returns']
    
    strategy_return = (1 + df['Strategy_Returns'].dropna()).cumprod().iloc[-1] - 1
    return strategy_return

print("="*60)
print("均线参数优化结果")
print("="*60)

for name, ticker in STOCKS.items():
    print(f"\n{name} ({ticker}):")
    df = download_data(ticker)
    if df is None or len(df) < 200:
        print("  数据不足")
        continue
    
    market_return = (1 + df['Close'].pct_change().dropna()).cumprod().iloc[-1] - 1
    print(f"  市场基准: {market_return*100:.2f}%")
    
    for short, long in PARAM_SETS:
        if len(df) < long + 10:
            continue
        ret = backtest_ma(df, short, long)
        diff = ret - market_return
        mark = "✓" if diff > 0 else "✗"
        print(f"  {short}/{long}: {ret*100:.2f}% ({diff:+.2f}%) {mark}")
