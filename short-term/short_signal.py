#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短线信号监控
- 涨跌幅监控
- 成交量异动
- 板块轮动
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

# 观察名单
WATCH_LIST = {
    '比亚迪': '002594.SZ',
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
    '英维克': '002837.SZ',
    '剑桥科技': '603083.SS',
}

def check_short_term_signals():
    """检查短线信号"""
    print("="*60)
    print(f"短线信号监控 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    signals = []
    
    for name, ticker in WATCH_LIST.items():
        try:
            # 获取近期数据
            df = yf.Ticker(ticker).history(period='5d')
            if len(df) < 2:
                continue
            
            # 今日数据
            today = df.iloc[-1]
            yesterday = df.iloc[-2] if len(df) > 1 else df.iloc[0]
            
            # 涨跌幅
            change = (today['Close'] / yesterday['Close'] - 1) * 100
            
            # 成交量放大
            vol_ratio = today['Volume'] / df['Volume'].mean() if df['Volume'].mean() > 0 else 0
            
            # 信号判断
            signal = ""
            if change > 5:
                signal = "🔥 涨幅 > 5%"
            elif change < -3:
                signal = "📉 跌幅 > 3%"
            elif vol_ratio > 2:
                signal = "📊 量能放大"
            
            if signal:
                print(f"{name}: {change:+.1f}% 成交量 {vol_ratio:.1f}x {signal}")
                signals.append(f"{name}: {change:+.1f}%")
            else:
                print(f"{name}: {change:+.1f}% (正常)")
        
        except Exception as e:
            print(f"{name}: 错误 - {e}")
    
    if not signals:
        print("\n今日无明显信号")
    else:
        print(f"\n发现 {len(signals)} 个信号: {', '.join(signals)}")
    
    return signals

if __name__ == "__main__":
    check_short_term_signals()
