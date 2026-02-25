#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宏观数据分析
- 利率 (Federal Funds Rate)
- PMI (采购经理指数)
- M2 货币供应量
- CPI/PPI 通胀
"""

import yfinance as yf
import pandas as pd
import numpy as np

def get_macro_data():
    """获取宏观数据"""
    print("="*60)
    print("宏观数据分析")
    print("="*60)
    
    # 美国利率预期 (TLT = 20年国债)
    tlt = yf.Ticker('TLT').history(period='1y')['Close']
    
    # 标普500 (市场)
    spy = yf.Ticker('SPY').history(period='1y')['Close']
    
    # 黄金 (避险)
    gld = yf.Ticker('GLD').history(period='1y')['Close']
    
    # 铜 (经济周期)
    copper = yf.Ticker('CPER').history(period='1y')['Close']
    
    # 恐慌指数 (VIX)
    vix = yf.Ticker('^VIX').history(period='1y')['Close']
    
    # 美元指数
    dxy = yf.Ticker('DXY').history(period='1y')['Close']
    
    return {
        'TLT (国债)': tlt,
        'SPY (股市)': spy,
        'GLD (黄金)': gld,
        '铜': copper,
        'VIX (恐慌)': vix,
        '美元': dxy,
    }

def analyze_macro():
    """分析宏观状态"""
    data = get_macro_data()
    
    print("\n📊 各类资产近期表现")
    print("-"*50)
    
    for name, series in data.items():
        if len(series) > 0:
            # 近1个月
            m1 = (series.iloc[-1] / series.iloc[-22] - 1) * 100 if len(series) > 22 else 0
            # 近3个月
            m3 = (series.iloc[-1] / series.iloc[-66] - 1) * 100 if len(series) > 66 else 0
            # 近6个月
            m6 = (series.iloc[-1] / series.iloc[-132] - 1) * 100 if len(series) > 132 else 0
            
            print(f"{name:<15} 1月: {m1:+6.1f}%  3月: {m3:+6.1f}%  6月: {m6:+6.1f}%")

def market_correlation():
    """市场相关性分析"""
    print("\n🔗 资产相关性 (与A股持仓)")
    print("-"*50)
    
    # 持仓
    stocks = {
        '紫金矿业': '601899.SS',
        '铜陵有色': '000630.SZ',
    }
    
    # 宏观
    spy = yf.Ticker('SPY').history(period='1y')['Close']
    gld = yf.Ticker('GLD').history(period='1y')['Close']
    tlt = yf.Ticker('TLT').history(period='1y')['Close']
    
    for name, ticker in stocks.items():
        stock = yf.Ticker(ticker).history(period='1y')['Close']
        
        # 对齐数据
        combined = pd.DataFrame({'stock': stock, 'spy': spy, 'gld': gld, 'tlt': tlt}).dropna()
        
        if len(combined) > 30:
            corr_spy = combined['stock'].corr(combined['spy'])
            corr_gld = combined['stock'].corr(combined['gld'])
            corr_tlt = combined['stock'].corr(combined['tlt'])
            
            print(f"{name}:")
            print(f"  与美股相关性: {corr_spy:+.2f}")
            print(f"  与黄金相关性: {corr_gld:+.2f}")
            print(f"  与国债相关性: {corr_tlt:+.2f}")

def sector_rotation():
    """行业轮动"""
    print("\n🔄 行业轮动 (ETF)")
    print("-"*50)
    
    sectors = {
        'XLE (能源)': 'XLE',
        'XLK (科技)': 'XLK',
        'XLF (金融)': 'XLF',
        'XLV (医疗)': 'XLV',
        'XLY (消费)': 'XLY',
        'XLP (必需消费)': 'XLP',
    }
    
    for name, ticker in sectors.items():
        df = yf.Ticker(ticker).history(period='6mo')
        if len(df) > 0:
            ret = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
            print(f"{name:<20}: {ret:+.1f}%")

if __name__ == "__main__":
    analyze_macro()
    market_correlation()
    sector_rotation()
