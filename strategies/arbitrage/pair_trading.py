#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
套利策略 (Arbitrage Strategy)

策略类型:
1. 配对交易 - 两只相关股票做价差
2. 跨市场套利 - A股vs港股
3. 统计套利 - 均值回归
"""

import yfinance as yf
import pandas as pd
import numpy as np

# 尝试找配对 - 有色金属相关
# 紫金矿业 vs 铜陵有色 (都是有色金属)
# 兴业银锡 vs 铜陵有色 (都产铜/锡)

PAIRS = [
    ('紫金矿业', '601899.SS', '铜陵有色', '000630.SZ'),
]

def download_data(ticker1, ticker2, period='3y'):
    """下载两只股票数据"""
    s1 = yf.Ticker(ticker1).history(period=period)
    s2 = yf.Ticker(ticker2).history(period=period)
    return s1, s2

def pair_trading(s1, s2, window=60):
    """配对交易策略"""
    # 计算价差
    df = pd.DataFrame({
        's1': s1['Close'],
        's2': s2['Close']
    }).dropna()
    
    # 价格比率
    df['ratio'] = df['s1'] / df['s2']
    
    # 移动平均和标准差
    df['ma'] = df['ratio'].rolling(window).mean()
    df['std'] = df['ratio'].rolling(window).std()
    
    # z-score
    df['zscore'] = (df['ratio'] - df['ma']) / df['std']
    
    # 信号
    # z-score < -1: s1太便宜，买s1卖s2
    # z-score > 1: s1太贵，卖s1买s2
    df['Signal'] = 0
    df.loc[df['zscore'] < -1, 'Signal'] = 1   # 买入比率低
    df.loc[df['zscore'] > 1, 'Signal'] = -1  # 卖出比率高
    df.loc[(df['zscore'] > -0.5) & (df['zscore'] < 0.5), 'Signal'] = 0  # 回归平仓
    
    # 计算收益
    df['s1_ret'] = df['s1'].pct_change()
    df['s2_ret'] = df['s2'].pct_change()
    
    # 做多s1做空s2的收益
    df['Pair_Returns'] = df['Signal'].shift(1) * (df['s1_ret'] - df['s2_ret'])
    
    return df

def backtest_pair(name1, ticker1, name2, ticker2):
    print(f"\n{'='*60}")
    print(f"配对交易: {name1} vs {name2}")
    print(f"{'='*60}")
    
    s1, s2 = download_data(ticker1, ticker2)
    if s1 is None or s2 is None or len(s1) < 100:
        print("数据不足")
        return
    
    df = pair_trading(s1, s2)
    
    # 基准：各买一半
    market_ret = (s1['Close'].iloc[-1] / s1['Close'].iloc[0]) * (s2['Close'].iloc[-1] / s2['Close'].iloc[0])
    market_ret = market_ret ** 0.5 - 1
    
    # 策略收益
    strategy_ret = (1 + df['Pair_Returns'].dropna()).cumprod().iloc[-1] - 1
    
    print(f"持有基准: {market_ret*100:.2f}%")
    print(f"配对策略: {strategy_ret*100:.2f}% ({strategy_ret - market_ret:+.2f}%)")
    
    return df

def main():
    print("="*60)
    print("配对交易策略回测")
    print("="*60)
    
    for name1, ticker1, name2, ticker2 in PAIRS:
        backtest_pair(name1, ticker1, name2, ticker2)

if __name__ == "__main__":
    main()
