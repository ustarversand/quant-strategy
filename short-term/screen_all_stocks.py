#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杨永兴十步法 - 全A股筛选
扫描所有A股，找出符合十步法的股票
"""

import akshare as ak
import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import sys

def get_a_stock_list():
    """获取A股列表"""
    print("获取A股列表...")
    df = ak.stock_info_a_code_name()
    
    # 转换代码格式
    stocks = []
    for _, row in df.iterrows():
        code = row['code']
        name = row['name']
        
        # 沪市 .SS, 深市 .SZ
        if code.startswith('6'):
            ticker = f"{code}.SS"
        else:
            ticker = f"{code}.SZ"
        
        stocks.append({'code': code, 'name': name, 'ticker': ticker})
    
    return stocks

def check_stock(ticker, name):
    """检查单只股票"""
    try:
        df = yf.Ticker(ticker).history(period='3mo', timeout=10)
        if df is None or len(df) < 20:
            return None
        
        price = df['Close'].iloc[-1]
        ma5 = df['Close'].rolling(5).mean().iloc[-1]
        ma10 = df['Close'].rolling(10).mean().iloc[-1]
        ma20 = df['Close'].rolling(20).mean().iloc[-1]
        
        vol = df['Volume'].iloc[-1]
        vol_ma = df['Volume'].rolling(20).mean().iloc[-1]
        
        ret_20d = (price / df['Close'].iloc[-20] - 1) * 100
        vol_ratio = vol / vol_ma
        
        # 筛选条件
        score = 0
        checks = []
        
        # 涨幅3-5%
        if 3 <= ret_20d <= 5:
            score += 2
            checks.append("涨幅3-5%")
        
        # 强势股
        if ret_20d > 10:
            score += 1
            checks.append("强势")
        
        # 放量
        if vol_ratio > 1:
            score += 2
            checks.append("放量")
        
        # 多头
        if ma5 > ma10 > ma20:
            score += 3
            checks.append("多头")
        
        # MA5上方
        if price > ma5:
            score += 1
            checks.append("MA5上")
        
        # 20日新高
        high_20 = df['High'].rolling(20).max().iloc[-1]
        if price >= high_20:
            score += 2
            checks.append("新高")
        
        if score >= 3:
            return {
                'name': name,
                'code': code,
                'price': price,
                'ret_20d': ret_20d,
                'vol_ratio': vol_ratio,
                'score': score,
                'checks': checks
            }
        
        return None
    
    except Exception as e:
        return None

def main():
    print("="*70)
    print(f"杨永兴十步法 - 全A股筛选")
    print(f"开始时间: {datetime.now()}")
    print("="*70)
    
    # 获取股票列表
    stocks = get_a_stock_list()
    print(f"共计 {len(stocks)} 只A股\n")
    
    # 筛选结果
    results = []
    
    # 筛选 (演示用，先筛选100只)
    # 实际使用时可改为全部
    sample_size = min(100, len(stocks))
    print(f"演示模式: 筛选前 {sample_size} 只股票...")
    print("(如需全量筛选，修改代码中的 sample_size)")
    print()
    
    for i, stock in enumerate(stocks[:sample_size]):
        if i % 20 == 0:
            print(f"进度: {i}/{sample_size}")
        
        result = check_stock(stock['ticker'], stock['name'])
        if result:
            results.append(result)
            print(f"  ✓ {result['name']}: {result['score']}分 - {' '.join(result['checks'])}")
    
    # 排序
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n" + "="*70)
    print(f"筛选结果 (共 {len(results)} 只符合条件)")
    print("="*70)
    
    print(f"\n{'排名':<6}{'股票':<15}{'代码':<10}{'价格':>10}{'20日涨幅':>12}{'量比':>8}{'分数':>6}{'信号'}")
    print("-"*80)
    
    for i, r in enumerate(results[:20], 1):
        sig = '|'.join(r['checks'])
        print(f"{i:<6}{r['name']:<15}{r['code']:<10}{r['price']:>10.2f}{r['ret_20d']:>+11.1f}%{r['vol_ratio']:>7.1f}x{r['score']:>5}  {sig}")
    
    # 保存结果
    if results:
        df = pd.DataFrame(results)
        df.to_csv(f'~/quant-strategy/logs/yang_screening_{datetime.now().strftime("%Y%m%d")}.csv', index=False)
        print(f"\n结果已保存到 logs/")

if __name__ == "__main__":
    main()
