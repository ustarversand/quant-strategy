#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能均线策略 - 双均线 + 成交量 + 止损
"""

import yfinance as yf

STOCKS = {
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
    '兴业银锡': '600737.SS',
    '英维克': '002837.SZ',
    '剑桥科技': '603083.SS',
}

def backtest(ticker):
    """双均线策略"""
    df = yf.download(ticker, start='2023-01-01', progress=False)
    if len(df) < 60:
        return None
    
    # 计算指标
    ma5 = df['Close'].rolling(5).mean()
    ma20 = df['Close'].rolling(20).mean()
    vol_ma = df['Volume'].rolling(20).mean()
    
    # 信号
    sig = [0] * len(df)
    for i in range(1, len(df)):
        if ma5.iloc[i-1] <= ma20.iloc[i-1] and ma5.iloc[i] > ma20.iloc[i]:
            if df['Volume'].iloc[i] > vol_ma.iloc[i] * 1.5:
                sig[i] = 1  # 买入
        elif ma5.iloc[i-1] >= ma20.iloc[i-1] and ma5.iloc[i] < ma20.iloc[i]:
            sig[i] = -1  # 卖出
    
    # 回测
    cash = 100000
    pos = 0
    shares = 0
    
    for i in range(60, len(df)):
        if sig[i] == 1 and pos == 0:
            shares = cash / df['Close'].iloc[i]
            pos = 1
        elif sig[i] == -1 and pos == 1:
            cash = shares * df['Close'].iloc[i]
            pos = 0
        
        # 止损5%
        if pos == 1:
            cost = cash / shares
            if (df['Close'].iloc[i] - cost) / cost < -0.05:
                cash = shares * df['Close'].iloc[i]
                pos = 0
    
    if pos == 1:
        cash = shares * df['Close'].iloc[-1]
    
    return (cash - 100000) / 100000 * 100

print("="*60)
print("智能均线策略 (MA5/MA20 + 量能 + 5%止损)")
print("="*60)

for name, ticker in STOCKS.items():
    ret = backtest(ticker)
    if ret:
        print(f"{name}: {ret:+.1f}%")

# 买入持有对比
print("\n买入持有对比:")
for name, ticker in STOCKS.items():
    df = yf.download(ticker, start='2023-01-01', progress=False)
    if len(df) > 60:
        bh = (df['Close'].iloc[-1] / df['Close'].iloc[60] - 1) * 100
        print(f"{name}: {bh:+.1f}%")
