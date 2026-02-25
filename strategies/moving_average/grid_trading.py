#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网格交易策略 (Grid Trading)

在震荡行情中，价格在区间内波动
低买高卖，不断赚取差价
"""

import yfinance as yf
import pandas as pd
import numpy as np

STOCKS = {
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
}

def grid_trading(ticker, grid_pct=0.03, holdings=5):
    """
    网格交易
    - grid_pct: 网格间距百分比
    - holdings: 持仓手数
    """
    df = yf.Ticker(ticker).history(period='1y')
    
    # 计算网格区间
    price = df['Close']
    high = price.max()
    low = price.min()
    
    # 创建网格
    levels = np.linspace(low, high, holdings * 2 + 1)
    
    print(f"\n{'='*50}")
    print(f"网格交易: {ticker}")
    print(f"价格区间: {low:.2f} - {high:.2f}")
    print(f"网格间距: {grid_pct*100}%")
    print(f"{'='*50}")
    
    # 简单回测：假设在区间内做网格
    # 实际收益 = 价格波动 / 网格数
    range_pct = (high - low) / low
    grid_profit = range_pct / (holdings * 2) * holdings
    
    # 买入持有收益
    buy_hold = (price.iloc[-1] / price.iloc[0] - 1)
    
    print(f"买入持有: {buy_hold*100:.1f}%")
    print(f"网格收益: ~{grid_profit*100:.1f}% (理论值)")
    
    return buy_hold, grid_profit

if __name__ == "__main__":
    for name, ticker in STOCKS.items():
        grid_trading(ticker)
