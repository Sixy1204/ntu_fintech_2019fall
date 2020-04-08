import sys
import os
import numpy as np
import pandas as pd
import talib

def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice):
    daily_open = dailyOhlcvFile['open']
    vol = dailyOhlcvFile['volume']
    data_len = len(daily_open)
    if(daily_open[data_len-3] < daily_open[data_len-2] and daily_open[data_len-2] < daily_open[data_len-1] ):
        return -1
    elif (daily_open[data_len-3] > daily_open[data_len-2] and daily_open[data_len-2] > daily_open[data_len-1]  ):
        return 1
    else:
        return 0

def computeReturnRate(short,long):
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
        action[evalDays-ic] = myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic],short,long)
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
        if ic == 3 and Holding > 0: 
            capital = Holding*clearPrice - transFee
            Holding = 0
    
        total[evalDays-ic] = capital + float(Holding>0) * (Holding*currPrice-transFee)
    returnRate = (total[-1] - capitalOrig)/capitalOrig
    return returnRate

if __name__=='__main__':
    returnRateBest=-1.00     # Initial best return rate
    dailyOhlcv = pd.read_csv(sys.argv[1])
    minutelyOhlcv = pd.read_csv(sys.argv[2])

    #os.chdir('C:/Users/12157/Desktop/hw-108/fintech/fintech_final')
    #dailyOhlcv = pd.read_csv('TX_daily.csv')
    #minutelyOhlcv = pd.read_csv('TX_minutely.csv')

    # search rsi_win, long_win, short_win, sell, buy
    short_win_min = 5; short_win_max=30;
    long_win_min = 90; long_win_max=120
    # Start exhaustive search
    for short in range(short_win_min, short_win_max+1,1):            # For-loop for alpha
        print("\tshort_win=%d" %(short))
        for long in range(long_win_min, long_win_max+1,1):        # For-loop for beta
            print("\tlong_win=%d" %(long))    # No newline
            returnRate = computeReturnRate( short,long)        # Start the whole run with the given parameters
            print("\t\t ==> returnRate=%f" %(returnRate))
            if returnRate > returnRateBest:        # Keep the best parameters
                shortBest=short
                longBest=long
                returnRateBest=returnRate
    print("Best settings: short=%d, long=%d ==> returnRate=%f" 
          %(shortBest, longBest,returnRateBest))        # Print the best result

