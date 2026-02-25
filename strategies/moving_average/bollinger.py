#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
布林带策略 (Bollinger Bands)

策略：
- 价格突破上轨 -> 卖出
- 价格突破下轨 -> 买入
- 价格回归中轨 -> 平仓
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

def bollinger_bands(df, window=20, num_std=2):
    df = df.copy()
    df['MA'] = df['Close'].rolling(window).mean()
    df['STD'] = df['Close'].rolling(window).std()
    df['Upper'] = df['MA'] + num_std * df['STD']
    df['Lower'] = df['MA'] - num_std * df['STD']
    return df

def backtest_bollinger(ticker, window=20, num_std=2):
    df = yf.Ticker(ticker).history(period='3y')
    df = bollinger_bands(df, window, num_std)
    
    # 信号
    df['Signal'] = 0
    df.loc[df['Close'] < df['Lower'], 'Signal'] = 1  # 超卖买入
    df.loc[df['Close'] > df['Upper'], 'Signal'] = -1  # 超买卖出
    df.loc[(df['Close'] > df['MA']) & (df['Close'].shift(1) < df['MA'].shift(1)), 'Signal'] = 0  # 回归平仓
    
    df['Position'] = df['Signal'].shift(1)
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Returns']
    
    market_ret = (1 + df['Returns'].dropna()).cumprod().iloc[-1] - 1
    strategy_ret = (1 + df['Strategy_Returns'].dropna()).cumprod().iloc[-1] - 1
    
    return market_ret, strategy_ret

print("="*50)
print("布林带策略回测")
print("="*50)

for name, ticker in STOCKS.items():
    market, strategy = backtest_bollinger(ticker)
    print(f"{name}: 市场 {market*100:.1f}% vs 策略 {strategy*100:.1f}% ({strategy-market:+.1f}%)")
