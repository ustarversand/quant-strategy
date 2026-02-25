#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
均线交叉策略回测
- 短期均线: 20日
- 长期均线: 50日
- 标的: 用户持仓股票
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# 持仓股票 (A股用 .SS 或 .SZ 后缀)
STOCKS = {
    '紫金矿业': '601899.SS',
    '剑桥科技': '603083.SS', 
    '兴业银锡': '600737.SS',
    '铜陵有色': '000630.SZ',
    '英维克': '002837.SZ'
}

# 策略参数
SHORT_WINDOW = 20   # 短期均线
LONG_WINDOW = 50     # 长期均线

def download_data(ticker, period='3y'):
    """下载历史数据"""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        return df
    except Exception as e:
        print(f"下载 {ticker} 失败: {e}")
        return None

def moving_average_crossover(df, short=20, long=50):
    """均线交叉策略"""
    df = df.copy()
    
    # 计算均线
    df['SMA_short'] = df['Close'].rolling(window=short).mean()
    df['SMA_long'] = df['Close'].rolling(window=long).mean()
    
    # 生成信号
    df['Signal'] = 0
    df.loc[df['SMA_short'] > df['SMA_long'], 'Signal'] = 1   # 金叉持有
    df.loc[df['SMA_short'] < df['SMA_long'], 'Signal'] = -1  # 死叉空仓
    
    # 计算持仓
    df['Position'] = df['Signal'].shift(1)  # 信号次日执行
    df.fillna(0, inplace=True)
    
    # 计算收益
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Returns']
    
    # 累计收益
    df['Cumulative_Market'] = (1 + df['Returns']).cumprod()
    df['Cumulative_Strategy'] = (1 + df['Strategy_Returns']).cumprod()
    
    return df

def backtest(stock_name, ticker):
    """回测单只股票"""
    print(f"\n{'='*50}")
    print(f"回测: {stock_name} ({ticker})")
    print(f"{'='*50}")
    
    df = download_data(ticker)
    if df is None or len(df) < LONG_WINDOW + 10:
        print(f"数据不足，跳过")
        return None
    
    df = moving_average_crossover(df, SHORT_WINDOW, LONG_WINDOW)
    
    # 统计结果
    market_return = df['Cumulative_Market'].iloc[-1] - 1
    strategy_return = df['Cumulative_Strategy'].iloc[-1] - 1
    
    # 年化收益
    years = len(df) / 252
    market_annual = (1 + market_return) ** (1/years) - 1
    strategy_annual = (1 + strategy_return) ** (1/years) - 1
    
    # 夏普比率 (简化)
    strategy_returns = df['Strategy_Returns'].dropna()
    sharpe = strategy_returns.mean() / strategy_returns.std() * np.sqrt(252) if strategy_returns.std() > 0 else 0
    
    # 交易次数
    trades = (df['Signal'].diff() != 0).sum()
    
    print(f"回测周期: {df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"交易次数: {trades}")
    print(f"市场收益: {market_return*100:.2f}%")
    print(f"策略收益: {strategy_return*100:.2f}%")
    print(f"年化市场: {market_annual*100:.2f}%")
    print(f"年化策略: {strategy_annual*100:.2f}%")
    print(f"夏普比率: {sharpe:.2f}")
    
    return df

def main():
    print("="*60)
    print("均线交叉策略回测")
    print(f"短期均线: {SHORT_WINDOW}日, 长期均线: {LONG_WINDOW}日")
    print("="*60)
    
    results = {}
    for name, ticker in STOCKS.items():
        df = backtest(name, ticker)
        if df is not None:
            results[name] = df
    
    # 汇总
    print("\n" + "="*60)
    print("汇总")
    print("="*60)
    print(f"{'股票':<12}{'市场收益':>12}{'策略收益':>12}{'夏普比率':>10}")
    print("-"*50)
    
    for name, df in results.items():
        market = df['Cumulative_Market'].iloc[-1] - 1
        strategy = df['Cumulative_Strategy'].iloc[-1] - 1
        sharpe = df['Strategy_Returns'].mean() / df['Strategy_Returns'].std() * np.sqrt(252) if df['Strategy_Returns'].std() > 0 else 0
        print(f"{name:<12}{market*100:>11.2f}%{strategy*100:>11.2f}%{sharpe:>10.2f}")

if __name__ == "__main__":
    main()
