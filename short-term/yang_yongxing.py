#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杨永兴战法 Demo
基于公开资料整理的选股策略逻辑：

核心要素:
1. 放量突破 - 成交量放大至2倍以上
2. 形态突破 - 股价突破关键均线/平台
3. 热点题材 - 所属板块处于热点
4. 强势股回调买入 - 龙头股首次回调企稳

注意: 这只是策略逻辑demo，实盘需谨慎
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# 观察名单
WATCH_LIST = {
    '比亚迪': '002594.SZ',
    '紫金矿业': '601899.SS',
    '铜陵有色': '000630.SZ',
    '英维克': '002837.SZ',
    '剑桥科技': '603083.SS',
}

def yang_yongxing_signals():
    """
    杨永兴战法信号检测
    
    信号类型:
    - 放量突破: 成交量 > 2倍均量 且 股价 > 20日高点
    - 回调企稳: 下跌后企稳在5日均线附近
    - 强势股: 20日涨幅 > 10%
    """
    print("="*60)
    print(f"杨永兴战法信号 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    results = []
    
    for name, ticker in WATCH_LIST.items():
        try:
            df = yf.Ticker(ticker).history(period='1mo')
            if len(df) < 20:
                continue
            
            # 计算指标
            ma5 = df['Close'].rolling(5).mean()
            ma20 = df['Close'].rolling(20).mean()
            vol_ma20 = df['Volume'].rolling(20).mean()
            
            # 今日数据
            today = df.iloc[-1]
            yesterday = df.iloc[-2]
            
            # 1. 放量信号
            vol_ratio = today['Volume'] / vol_ma20.iloc[-1]
            
            # 2. 20日涨幅
            ret_20d = (today['Close'] / df['Close'].iloc[-20] - 1) * 100
            
            # 3. 突破20日高点
            high_20d = df['High'].iloc[-20:].max()
            breakout = today['Close'] > high_20d
            
            # 4. 回调企稳 (收盘价在5日均线附近)
            near_ma5 = abs(today['Close'] - ma5.iloc[-1]) / ma5.iloc[-1] < 0.02
            
            # 信号判断
            signals = []
            if vol_ratio > 2 and breakout:
                signals.append("🔥 放量突破")
            if ret_20d > 10:
                signals.append("💪 强势股")
            if near_ma5 and ret_20d < 0:
                signals.append("📍 回调企稳")
            
            # 打印结果
            print(f"\n{name} ({ticker}):")
            print(f"  当前价: {today['Close']:.2f}")
            print(f"  20日涨幅: {ret_20d:+.1f}%")
            print(f"  量比: {vol_ratio:.1f}x")
            print(f"  20日高点: {high_20d:.2f} {'✓ 突破' if breakout else ''}")
            
            if signals:
                print(f"  信号: {' | '.join(signals)}")
                results.append((name, signals))
            else:
                print(f"  信号: 无")
        
        except Exception as e:
            print(f"{name}: 错误 - {e}")
    
    return results

def screen_candidates():
    """
    选股池筛选Demo
    演示如何在A股中筛选符合杨永兴战法的股票
    
    筛选条件:
    1. 20日涨幅前100
    2. 量比 > 1.5
    3. 流通市值 > 50亿
    """
    print("\n" + "="*60)
    print("选股池筛选 Demo")
    print("="*60)
    print("注意: 这只是Demo演示，实盘选股需要:")
    print("  1. 实时行情数据 (需付费)")
    print("  2. 完整的A股列表")
    print("  3. 更多维度的基本面筛选")
    print()
    print("Demo演示: 使用现有的5只股票进行信号检测")
    print("="*60)

if __name__ == "__main__":
    screen_candidates()
    signals = yang_yongxing_signals()
    
    print("\n" + "="*60)
    print("总结")
    print("="*60)
    if signals:
        for name, sig in signals:
            print(f"  {name}: {' '.join(sig)}")
    else:
        print("  今日无符合杨永兴战法的信号")
