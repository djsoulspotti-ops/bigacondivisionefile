{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import numpy as np\
import talib  # Per RSI e EMA (installa TA-Lib)\
\
# Calcola EMA\
def calc_ema(prices, period):\
    return talib.EMA(prices, timeperiod=period)\
\
# Calcola RSI\
def calc_rsi(prices, period):\
    return talib.RSI(prices, timeperiod=period)\
\
# Calcola livelli Fibonacci da swing high/low\
def calc_fibonacci(high, low, swing_idx):\
    swing_high = high[swing_idx]\
    swing_low = low[swing_idx]\
    fib_range = swing_high - swing_low\
    return [swing_high - (fib_range * level) for level in FIB_LEVELS]\
\
# Trova ultimo swing high/low\
def find_last_swing(high, low, lookback=5):\
    n = len(high)\
    for i in range(n - lookback * 2, n):\
        if all(high[i] >= high[max(0, i-lookback):i+lookback+1]):\
            return i  # Swing high\
        if all(low[i] <= low[max(0, i-lookback):i+lookback+1]):\
            return i  # Swing low\
    return None}