#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual Thrust 策略

日内突破策略：
- 计算枢轴区间
- 突破上轨买入
- 跌破下轨卖出
"""

import yfinance as yf
import pandas as pd
import numpy as np

STOCKS = {
    '紫金矿业': '601899.SS',
    '英维克': '002837.SZ',
}

def dual_thrust(df, k1=0.5, k2=0.5):
    """Dual Thrust"""
    df = df.copy()
    
    # 过去N天最高/最低价
    n = 20
    df['HH'] = df['High'].rolling(n).max()  # 最高价
    df['LC'] = df['Low'].rolling(n).min()   # 最低价
    df['HC'] = df['Close'].rolling(n).max() # 收盘价
    
    # 枢轴区间
    df['Range'] = np.maximum(df['HH'] - df['Close'], df['Close'] - df['LC'])
    
    # 上下轨
    df['Upper'] = df['Open'] + k1 * df['Range']
    df['Lower'] = df['Open'] - k2 * df['Range']
    
    # 信号
    df['Signal'] = 0
    df.loc[df['High'] > df['Upper'], 'Signal'] = 1   # 突破买入
    df.loc[df['Low'] < df['Lower'], 'Signal'] = -1   # 跌破卖出
    
    return df

def backtest_dual_thrust(ticker):
    df = yf.Ticker(ticker).history(period='2y')
    df = dual_thrust(df)
    
    # 简化：突破买入持有到跌破
    position = 0
    returns = []
    
    for i in range(1, len(df)):
        signal = df['Signal'].iloc[i-1]
        ret = df['Close'].iloc[i] / df['Close'].iloc[i-1] - 1
        
        if signal == 1:
            position = 1
        elif signal == -1:
            position = 0
        
        if position:
            returns.append(ret)
        else:
            returns.append(0)
    
    strategy_ret = np.prod(1 + np.array(returns)) - 1
    market_ret = df['Close'].iloc[-1] / df['Close'].iloc[0] - 1
    
    return market_ret, strategy_ret

print("="*50)
print("Dual Thrust 策略")
print("="*50)

for name, ticker in STOCKS.items():
    market, strategy = backtest_dual_thrust(ticker)
    print(f"{name}: 市场 {market*100:.1f}% vs 策略 {strategy*100:.1f}%")
