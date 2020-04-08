# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import talib
import os

def EMA_diff(daily_open):
    EMA_short = talib.MA(daily_open,12,matype=1).reset_index(drop=True)
    EMA_long = talib.MA(daily_open,30,matype=1).reset_index(drop=True)
    diff = EMA_short - EMA_long
    if diff[len(diff)-1] > 0:
        return 1
    elif diff[len(diff)-1] < 0:
        return -1
    else:
        return 0

def EMA(daily_open): # exponential
    EMA = talib.MA(daily_open,12,matype=1).reset_index(drop=True)
    if daily_open[len(daily_open)-1] - EMA[len(EMA)-1] > 5:
        action = 1
    elif daily_open[len(daily_open)-1] - EMA[len(EMA)-1] < 10:
        action = -1
    else:
        action = 0
    return action

def RSI_cross(daily_open):
    RSI_short = talib.RSI(daily_open,20).reset_index(drop=True)
    RSI_long = talib.RSI(daily_open,120).reset_index(drop=True)
    pre_short = RSI_short[len(RSI_short)-2]
    pre_long = RSI_long[len(RSI_long)-2]
 
    curr_short = RSI_short[len(RSI_short)-1]
    curr_long = RSI_long[len(RSI_long)-1]
 
    if(pre_short < pre_long and curr_short > curr_long ):
        return 1
    elif (pre_short > pre_long and curr_short < curr_long ):
        return -1
    else:
        return 0

def RSI(daily_open):
    RSI_short = talib.RSI(daily_open,120).reset_index(drop=True)
    curr_short = RSI_short[len(RSI_short)-1]
    if curr_short > 65:
        return 1
    elif curr_short < 35:
        return -1
    else:
        return 0
'''
def KD(df):
    slowk, slowd = talib.STOCH(df.high, df.low, df.close,9,3,3)
    slowk.reset_index(drop=True)
    slowd.reset_index(drop=True)
    value = len(slowk)-1
    if slowk[value]>slowd[value]:
        return 1
    elif slowk[value]<slowd[value]:
        return -1
    else:
        return 0
'''
# action = myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice)
def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice):
    daily_open = dailyOhlcvFile['open']
    return RSI(daily_open)



os.chdir('C:/Users/12157/Desktop/hw-108/fintech/fintech_final')
dailyOhlcv = pd.read_csv('TX_daily.csv')
minutelyOhlcv = pd.read_csv('TX_minutely.csv')
capital = 500000.0
capitalOrig=capital
transFee = 100
evalDays = 14
action = np.zeros((evalDays,1))
realAction = np.zeros((evalDays,1))
total = np.zeros((evalDays,1))
total[0] = capital
Holding = 0.0
openPricev = dailyOhlcv["open"].tail(evalDays).values
clearPrice = dailyOhlcv.iloc[-3]["close"]
for ic in range(evalDays,0,-1):
    dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
    dateStr = dailyOhlcvFile.iloc[-1,0]
    minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
    action[evalDays-ic] = myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic])
    currPrice = openPricev[evalDays-ic]
    if action[evalDays-ic] == 1:
        if Holding == 0 and capital > transFee:
            Holding = (capital-transFee)/currPrice
            capital = 0
            realAction[evalDays-ic] = 1
    elif action[evalDays-ic] == -1:
        if Holding > 0 and Holding*currPrice > transFee:
            capital = Holding*currPrice - transFee
            Holding = 0
            realAction[evalDays-ic] = -1
    elif action[evalDays-ic] == 0:
        realAction[evalDays-ic] = 0
    else:
        assert False
    if ic == 3 and Holding > 0: #遇到每個月的第三個禮拜三要平倉，請根據data的日期自行修改
        capital = Holding*clearPrice - transFee
        Holding = 0

    total[evalDays-ic] = capital + float(Holding>0) * (Holding*currPrice-transFee)

returnRate = (total[-1] - capitalOrig)/capitalOrig * 10000
print(returnRate)



