#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杨永兴战法 - 增强版
加入更多选股条件和信号

策略逻辑:
1. 放量突破 - 量比 > 1.5，股价突破20日高点
2. 均线多头 - 5日 > 10日 > 20日
3. 强势股 - 20日涨幅 > 10%
4. 回调企稳 - 下跌后企稳在5日均线附近
5. 新高突破 - 创20日/60日新高
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# 扩大观察名单
WATCH_LIST = {
    # 有色金属
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
    '兴业银锡': '600737.SS',
    # 科技
    '剑桥科技': '603083.SS',
    '英维克': '002837.SZ',
    # 新能源
    '比亚迪': '002594.SZ',
    '宁德时代': '300750.SZ',
    # 消费
    '贵州茅台': '600519.SS',
    '五粮液': '000858.SZ',
}

def calculate_indicators(df):
    """计算技术指标"""
    # 均线
    df['MA5'] = df['Close'].rolling(5).mean()
    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA20'] = df['Close'].rolling(20).mean()
    df['MA60'] = df['Close'].rolling(60).mean()
    
    # 量比
    df['VOL_MA20'] = df['Volume'].rolling(20).mean()
    df['VOL_RATIO'] = df['Volume'] / df['VOL_MA20']
    
    #VOL_MA20 涨跌幅
    df['RET_5D'] = df['Close'].pct_change(5) * 100
    df['RET_20D'] = df['Close'].pct_change(20) * 100
    
    # 20日/60日新高
    df['HIGH_20D'] = df['High'].rolling(20).max()
    df['HIGH_60D'] = df['High'].rolling(60).max()
    
    return df

def check_signals(name, ticker):
    """检查信号"""
    try:
        df = yf.Ticker(ticker).history(period='3mo')
        if len(df) < 60:
            return None
        
        df = calculate_indicators(df)
        latest = df.iloc[-1]
        
        signals = []
        score = 0
        
        # 1. 放量突破
        if latest['VOL_RATIO'] > 1.5 and latest['Close'] > latest['HIGH_20D']:
            signals.append("🔥 放量突破")
            score += 2
        
        # 2. 均线多头排列
        if latest['MA5'] > latest['MA10'] > latest['MA20']:
            signals.append("📈 多头排列")
            score += 1
        
        # 3. 强势股
        if latest['RET_20D'] > 10:
            signals.append("💪 强势股")
            score += 2
        
        # 4. 回调企稳 (在MA5附近且之前有跌幅)
        if (abs(latest['Close'] - latest['MA5']) / latest['MA5'] < 0.02 
            and latest['RET_5D'] < 0 and latest['RET_5D'] > -5):
            signals.append("📍 回调企稳")
            score += 1
        
        # 5. 创60日新高
        if latest['Close'] >= latest['HIGH_60D']:
            signals.append("🎯 60日新高")
            score += 2
        
        # 6. 成交量持续放大
        vol_trend = df['VOL_RATIO'].tail(5).mean()
        if vol_trend > 1.2:
            signals.append("📊 量能活跃")
            score += 1
        
        return {
            'name': name,
            'ticker': ticker,
            'price': latest['Close'],
            'ret_20d': latest['RET_20D'],
            'vol_ratio': latest['VOL_RATIO'],
            'signals': signals,
            'score': score
        }
    
    except Exception as e:
        return None

def main():
    print("="*70)
    print(f"杨永兴战法 增强版 - {datetime.now().strftime('%Y-%m-%d')}")
    print("="*70)
    
    results = []
    
    for name, ticker in WATCH_LIST.items():
        result = check_signals(name, ticker)
        if result:
            results.append(result)
    
    # 按分数排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # 打印结果
    print(f"\n{'股票':<12}{'价格':>8}{'20日':>8}{'量比':>8}{'分数':>6}{'信号'}")
    print("-"*70)
    
    for r in results:
        signal_str = ' | '.join(r['signals']) if r['signals'] else '无'
        print(f"{r['name']:<12}{r['price']:>8.2f}{r['ret_20d']:>+7.1f}%{r['vol_ratio']:>7.1f}x{r['score']:>5}  {signal_str}")
    
    # Top推荐
    print("\n" + "="*70)
    print("重点关注 (分数 >= 3)")
    print("="*70)
    
    top_stocks = [r for r in results if r['score'] >= 3]
    if top_stocks:
        for r in top_stocks:
            print(f"  🏆 {r['name']} - {' '.join(r['signals'])}")
    else:
        print("  今日无符合条件的股票")

if __name__ == "__main__":
    main()
