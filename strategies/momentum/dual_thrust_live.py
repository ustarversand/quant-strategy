#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual Thrust 实盘信号
每日运行，获取今日交易信号
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

STOCKS = {
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
    '兴业银锡': '600737.SS',
    '英维克': '002837.SZ',
    '剑桥科技': '603083.SS',
}

def dual_thrust_signal(ticker, k1=0.5, k2=0.5):
    """获取Dual Thrust信号"""
    # 获取最近22天数据
    df = yf.Ticker(ticker).history(period='1mo')
    
    if len(df) < 20:
        return None, None, None
    
    # 昨天数据
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    
    HH = df['High'].iloc[-22:-1].max()   # 20日最高
    LC = df['Low'].iloc[-22:-1].min()    # 20日最低
    HC = df['Close'].iloc[-22:-1].max()  # 20日收盘最高
    
    # Range
    Range = max(HH - yesterday['Close'], yesterday['Close'] - LC)
    
    # 上下轨
    Upper = yesterday['Open'] + k1 * Range
    Lower = yesterday['Open'] - k2 * Range
    
    # 今日价格
    current = today['Close']
    high = today['High']
    low = today['Low']
    
    # 信号
    signal = 'hold'
    if high > Upper:
        signal = 'BUY (突破上轨)'
    elif low < Lower:
        signal = 'SELL (跌破下轨)'
    
    return signal, Upper, Lower

def main():
    print("="*60)
    print(f"Dual Thrust 信号 - {datetime.now().strftime('%Y-%m-%d')}")
    print("="*60)
    
    for name, ticker in STOCKS.items():
        signal, upper, lower = dual_thrust_signal(ticker)
        
        if signal:
            print(f"\n{name} ({ticker}):")
            print(f"  上轨: {upper:.2f}")
            print(f"  下轨: {lower:.2f}")
            print(f"  信号: {signal}")
        else:
            print(f"{name}: 数据不足")

if __name__ == "__main__":
    main()
