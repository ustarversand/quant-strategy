#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dual Thrust 实盘信号 - 每日运行版
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import sys

STOCKS = {
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
    '兴业银锡': '600737.SS',
    '英维克': '002837.SZ',
    '剑桥科技': '603083.SS',
}

def get_signal(name, ticker):
    try:
        # 使用3个月数据确保足够
        df = yf.Ticker(ticker).history(period='3mo')
        
        if len(df) < 25:
            return f"{name}: 数据不足 ({len(df)}天)"
        
        # 取最近22个交易日
        recent = df.iloc[:-1].tail(22)
        yesterday = df.iloc[-2]
        
        HH = recent['High'].max()
        LC = recent['Low'].min()
        Range = max(HH - yesterday['Close'], yesterday['Close'] - LC)
        
        Upper = yesterday['Open'] + 0.5 * Range
        Lower = yesterday['Open'] - 0.5 * Range
        
        # 今日
        today_close = df.iloc[-1]['Close']
        
        signal = "持有"
        if today_close > Upper:
            signal = "BUY"
        elif today_close < Lower:
            signal = "SELL"
        
        return f"{name}: {signal} (当前:{today_close:.2f} 区间:{Lower:.2f}-{Upper:.2f})"
    
    except Exception as e:
        return f"{name}: 错误 - {e}"

def main():
    print("="*60)
    print(f"Dual Thrust 信号 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    signals = []
    for name, ticker in STOCKS.items():
        signal = get_signal(name, ticker)
        print(signal)
        signals.append(signal)
    
    # 保存到文件
    with open('/Users/ustar/quant-strategy/logs/latest_signal.txt', 'w') as f:
        f.write('\n'.join(signals))

if __name__ == "__main__":
    main()
