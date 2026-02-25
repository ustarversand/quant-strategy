#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动量策略 (Momentum Strategy)

策略类型:
1. RSI - 相对强弱指数
2. MACD - 移动平均收敛/发散
3. 动量反转
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

def download_data(ticker, period='3y'):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def rsi_strategy(df, period=14, oversold=30, overbought=70):
    """RSI 策略"""
    df = df.copy()
    
    # 计算 RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # 信号
    df['Signal'] = 0
    df.loc[df['RSI'] < oversold, 'Signal'] = 1   # 超卖 -> 买入
    df.loc[df['RSI'] > overbought, 'Signal'] = -1  # 超买 -> 卖出
    
    df['Position'] = df['Signal'].shift(1)
    df.fillna(0, inplace=True)
    
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Returns']
    
    return df

def macd_strategy(df, fast=12, slow=26, signal=9):
    """MACD 策略"""
    df = df.copy()
    
    ema_fast = df['Close'].ewm(span=fast).mean()
    ema_slow = df['Close'].ewm(span=slow).mean()
    
    df['MACD'] = ema_fast - ema_slow
    df['Signal_Line'] = df['MACD'].ewm(span=signal).mean()
    
    df['Signal'] = 0
    df.loc[df['MACD'] > df['Signal_Line'], 'Signal'] = 1
    df.loc[df['MACD'] < df['Signal_Line'], 'Signal'] = -1
    
    df['Position'] = df['Signal'].shift(1)
    df.fillna(0, inplace=True)
    
    df['Returns'] = df['Close'].pct_change()
    df['Strategy_Returns'] = df['Position'] * df['Returns']
    
    return df

def backtest(stock_name, ticker):
    print(f"\n{'='*50}")
    print(f"动量策略回测: {stock_name} ({ticker})")
    print(f"{'='*50}")
    
    df = download_data(ticker)
    if df is None or len(df) < 50:
        print("数据不足")
        return
    
    # RSI 策略
    df_rsi = rsi_strategy(df.copy())
    rsi_return = (1 + df_rsi['Strategy_Returns'].dropna()).cumprod().iloc[-1] - 1
    
    # MACD 策略
    df_macd = macd_strategy(df.copy())
    macd_return = (1 + df_macd['Strategy_Returns'].dropna()).cumprod().iloc[-1] - 1
    
    # 市场基准
    market_return = (1 + df['Close'].pct_change().dropna()).cumprod().iloc[-1] - 1
    
    print(f"市场基准: {market_return*100:.2f}%")
    print(f"RSI策略:   {rsi_return*100:.2f}% ({rsi_return - market_return:+.2f}%)")
    print(f"MACD策略:  {macd_return*100:.2f}% ({macd_return - market_return:+.2f}%)")

def main():
    print("="*60)
    print("动量策略回测 (RSI + MACD)")
    print("="*60)
    
    for name, ticker in STOCKS.items():
        backtest(name, ticker)

if __name__ == "__main__":
    main()
