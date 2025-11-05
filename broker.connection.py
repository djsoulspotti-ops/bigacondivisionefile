{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from ib_insync import *\
from config import SYMBOL\
\
# Classe per gestire broker (Interactive Brokers)\
class Broker:\
    def __init__(self):\
        self.ib = IB()\
        self.ib.connect('127.0.0.1', 7497, clientId=1)  # Porta TWS/IB Gateway\
        self.contract = Forex(SYMBOL)  # O Contract per futures\
\
    def get_historical_data(self, duration, bar_size):\
        bars = self.ib.reqHistoricalData(self.contract, endDateTime='', durationStr=duration, \
                                         barSizeSetting=bar_size, whatToShow='MIDPOINT', useRTH=True)\
        return util.df(bars)\
\
    def place_trade(self, action, quantity, price, tp_level, sl_level):\
        # Crea bracket order con SL/TP\
        bracket = util.bracketOrder(action, quantity, price, tp_level, sl_level)\
        for o in bracket:\
            self.ib.placeOrder(self.contract, o)\
        return bracket\
\
    def disconnect(self):\
        self.ib.disconnect()\
\
# Nota: Per MT5 (prop firm), sostituisci con:\
# import MetaTrader5 as mt5\
# mt5.initialize()\
# Poi usa mt5.copy_rates_range per dati e mt5.order_send per ordini.}