{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import datetime\
import logging\
import numpy as np\
from indicators import calc_ema, calc_rsi, calc_fibonacci, find_last_swing\
from config import RSI_PERIOD, EMA_PERIOD, PRICE_TOLERANCE\
\
# Configura logging\
logging.basicConfig(filename='gold_trades_log.log', level=logging.INFO, \
                    format='%(asctime)s - %(message)s')\
\
def check_signals(broker):\
    now = datetime.datetime.now()\
    if now.weekday() >= 5:  # Skip weekend\
        return\
    \
    # Dati H4\
    df_h4 = broker.get_historical_data('30 D', '4 hours')\
    h4_close = df_h4['close'].values\
    h4_high = df_h4['high'].values\
    h4_low = df_h4['low'].values\
    h4_ema = calc_ema(h4_close, EMA_PERIOD)\
    h4_trend = 'UP' if h4_close[-1] > h4_ema[-1] else 'DOWN'\
    \
    # Ultimo swing per Fib\
    last_swing_idx = find_last_swing(h4_high, h4_low)\
    if last_swing_idx is None:\
        return\
    fib_levels = calc_fibonacci(h4_high, h4_low, last_swing_idx)\
    \
    # Dati M15\
    df_m15 = broker.get_historical_data('4 H', '15 mins')\
    m15_close = df_m15['close'].values\
    m15_rsi = calc_rsi(m15_close, RSI_PERIOD)\
    current_price = m15_close[-1]\
    \
    # Logica segnali (3 conferme)\
    signal = 0\
    fib_hit = any(abs(current_price - level) < PRICE_TOLERANCE for level in fib_levels)\
    if h4_trend == 'UP' and fib_hit and m15_rsi[-1] < 70:\
        signal = 1  # Buy\
    elif h4_trend == 'DOWN' and fib_hit and m15_rsi[-1] > 30:\
        signal = -1  # Sell\
    \
    if signal != 0:\
        # SL/TP basati su Fib\
        fib_idx = np.argmin(np.abs(np.array(fib_levels) - current_price))\
        sl_level = fib_levels[max(fib_idx - 1, 0)] if signal == 1 else fib_levels[min(fib_idx + 1, len(fib_levels)-1)]\
        tp_level = fib_levels[min(fib_idx + 1, len(fib_levels)-1)] if signal == 1 else fib_levels[max(fib_idx - 1, 0)]\
        \
        # Piazza trade\
        action = 'BUY' if signal == 1 else 'SELL'\
        trade = broker.place_trade(action, LOT_SIZE, current_price, tp_level, sl_level)\
        \
        # Log\
        log_msg = f"Trade: \{action\}, Price: \{current_price\}, SL: \{sl_level\}, TP: \{tp_level\}"\
        logging.info(log_msg)\
        print(log_msg)}