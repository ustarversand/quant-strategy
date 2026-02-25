#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杨永兴 十步尾盘买入法 Demo
"""

import yfinance as yf

stocks = {
    '英维克': '002837.SZ',
    '铜陵有色': '000630.SZ',
    '紫金矿业': '601899.SS',
    '比亚迪': '002594.SZ',
}

print("="*60)
print("杨永兴 十步尾盘买入法")
print("="*60)

for name, ticker in stocks.items():
    df = yf.Ticker(ticker).history(period='3mo')
    if len(df) < 20:
        continue
    
    price = df['Close'].iloc[-1]
    ma5 = df['Close'].rolling(5).mean().iloc[-1]
    ma20 = df['Close'].rolling(20).mean().iloc[-1]
    vol = df['Volume'].iloc[-1]
    vol_ma = df['Volume'].rolling(20).mean().iloc[-1]
    
    ret_20d = (price / df['Close'].iloc[-20] - 1) * 100
    vol_ratio = vol / vol_ma
    
    checks = []
    if vol_ratio > 1:
        checks.append("量比>1")
    if 3 < ret_20d < 5:
        checks.append("涨幅3-5%")
    if price > ma5:
        checks.append("均价线上")
    if price > ma20:
        checks.append("20日线上")
    
    print(f"\n{name}:")
    print(f"  价格: {price:.2f}")
    print(f"  20日涨幅: {ret_20d:+.1f}%")
    print(f"  量比: {vol_ratio:.1f}x")
    print(f"  符合: {', '.join(checks) if checks else '无'}")

print("\n" + "="*60)
print("十步法要点:")
print("1. 选时: 大盘趋势")
print("2. 1点半看涨幅3-5%")
print("3. 量比>1")
print("4. 换手率5-10%")
print("5. 市值50-200亿")
print("6. 成交量温和放大")
print("7. K线无压力")
print("8. 分时均价线上")
print("9. 2点半创新高买入")
print("10. 第二天卖出")
