#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宏观策略"""

import yfinance as yf

gld = yf.Ticker('GLD').history(period='1y')['Close']
dbc = yf.Ticker('DBC').history(period='1y')['Close']

gc = (gld / dbc).dropna()
print(f'金铜比: {gc.iloc[-1]:.4f}')
print(f'20日均线: {gc.rolling(20).mean().iloc[-1]:.4f}')
signal = 'risk_off' if gc.iloc[-1] > gc.rolling(20).mean().iloc[-1] else 'risk_on'
print(f'信号: {signal}')
