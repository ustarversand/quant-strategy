#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动量因子策略 (Momentum Factor)

策略：
- 过去N个月涨幅最好的资产
- 持续持有直到反转
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

def momentum_signal(lookback=60):
    """动量信号"""
    signals = {}
    
    for name, ticker in STOCKS.items():
        df = yf.Ticker(ticker).history(period='2y')
        if len(df) < lookback:
            continue
        
        # 过去N天收益
        ret = (df['Close'].iloc[-1] / df['Close'].iloc[-lookback] - 1) * 100
        signals[name] = ret
    
    return signals

def relative_momentum():
    """相对动量 - 选最强的"""
    signals = momentum_signal(60)
    
    print("="*50)
    print("动量排名 (过去60天)")
    print("="*50)
    
    # 排序
    sorted_stocks = sorted(signals.items(), key=lambda x: x[1], reverse=True)
    
    for i, (name, ret) in enumerate(sorted_stocks, 1):
        print(f"{i}. {name}: {ret:+.1f}%")
    
    # 选最强
    winner = sorted_stocks[0]
    print(f"\n最强动量: {winner[0]} ({winner[1]:+.1f}%)")

if __name__ == "__main__":
    relative_momentum()
