#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杨永兴 十步尾盘买入法 - 增强版
加入更多股票池和实时监控
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

# 扩大股票池
STOCKS = {
    # 有色金属 (你的持仓)
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
    '兴业银锡': '600737.SS',
    # 科技
    '英维克': '002837.SZ',
    '剑桥科技': '603083.SS',
    '中际旭创': '308308.SZ',
    '新易盛': '300502.SZ',
    # 新能源
    '比亚迪': '002594.SZ',
    '宁德时代': '300750.SZ',
    '隆基绿能': '601012.SS',
    # 消费
    '贵州茅台': '600519.SS',
    '五粮液': '000858.SZ',
}

def check_stock(name, ticker):
    """检查是否符合十步法"""
    try:
        df = yf.Ticker(ticker).history(period='3mo')
        if len(df) < 20:
            return None
        
        price = df['Close'].iloc[-1]
        ma5 = df['Close'].rolling(5).mean().iloc[-1]
        ma10 = df['Close'].rolling(10).mean().iloc[-1]
        ma20 = df['Close'].rolling(20).mean().iloc[-1]
        
        vol = df['Volume'].iloc[-1]
        vol_ma = df['Volume'].rolling(20).mean().iloc[-1]
        
        ret_20d = (price / df['Close'].iloc[-20] - 1) * 100
        vol_ratio = vol / vol_ma
        
        # 检查条件
        checks = []
        score = 0
        
        if 3 <= ret_20d <= 5:
            checks.append("涨幅3-5%")
            score += 2
        elif ret_20d > 10:
            checks.append("强势")
            score += 1
        
        if vol_ratio > 1:
            checks.append("放量")
            score += 2
        elif vol_ratio > 0.8:
            checks.append("量稳")
            score += 1
        
        if price > ma5 > ma10 > ma20:
            checks.append("多头")
            score += 3
        
        if price > ma5:
            checks.append("MA5上")
            score += 1
        
        # 20日新高
        high_20 = df['High'].rolling(20).max().iloc[-1]
        if price >= high_20:
            checks.append("新高")
            score += 2
        
        return {
            'name': name,
            'price': price,
            'ret_20d': ret_20d,
            'vol_ratio': vol_ratio,
            'checks': checks,
            'score': score
        }
    except:
        return None

def market_index():
    """检查大盘趋势"""
    print("\n【大盘趋势】")
    
    # 创业板
    cyb = yf.Ticker('159915.SZ').history(period='1mo')
    if len(cyb) > 0:
        cyb_ret = (cyb['Close'].iloc[-1] / cyb['Close'].iloc[0] - 1) * 100
        print(f"  创业板: {cyb_ret:+.1f}%")
    
    # 沪深300
    hs300 = yf.Ticker('510300.SS').history(period='1mo')
    if len(hs300) > 0:
        hs_ret = (hs300['Close'].iloc[-1] / hs300['Close'].iloc[0] - 1) * 100
        print(f"  沪深300: {hs_ret:+.1f}%")
    
    if hs_ret > 5:
        return "中期上升"
    elif hs_ret > 0:
        return "短期上升"
    else:
        return "下降"

def main():
    print("="*70)
    print(f"杨永兴十步法 增强版 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*70)
    
    # 大盘趋势
    trend = market_index()
    print(f"  → 大盘状态: {trend}")
    
    results = []
    for name, ticker in STOCKS.items():
        r = check_stock(name, ticker)
        if r:
            results.append(r)
    
    # 排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n{'股票':<10}{'价格':>8}{'20日':>8}{'量比':>8}{'分数':>6}{'信号'}")
    print("-"*70)
    
    for r in results:
        sig = ' | '.join(r['checks']) if r['checks'] else '-'
        print(f"{r['name']:<10}{r['price']:>8.2f}{r['ret_20d']:>+7.1f}%{r['vol_ratio']:>7.1f}x{r['score']:>5}  {sig}")
    
    # Top推荐
    print("\n" + "="*70)
    print("【重点关注】分数>=3")
    print("="*70)
    
    top = [r for r in results if r['score'] >= 3]
    if top:
        for r in top:
            print(f"  🏆 {r['name']}: {' '.join(r['checks'])}")
    else:
        print("  今日无强烈信号")

if __name__ == "__main__":
    main()
