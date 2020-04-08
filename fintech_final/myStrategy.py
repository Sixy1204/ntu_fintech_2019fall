# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import sys
import os


def compute_rsi(windowedData):
    up = 0
    down = 0
    windowSize = len(windowedData)
    for i in range(windowSize - 1):
        if windowedData[i] <= windowedData[i + 1]:
            up += (windowedData[i + 1] - windowedData[i])
        else:
            down += (windowedData[i] - windowedData[i + 1])
    return (up / (down + up))*100
    
# action = myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice)
def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPrice, windowSize, alpha, beta, short_win, long_win):
    data = dailyOhlcvFile['open']
    windowedData = data[-windowSize:].reset_index(drop=True)
    ma = np.mean(windowedData)
    pre_short_windowed_data = data[-short_win - 1:-1].reset_index(drop=True)
    pre_long_windowed_data = data[-long_win - 1:-1].reset_index(drop=True)
    
    short_windowed_data = data[-short_win:].reset_index(drop=True)
    long_windowed_data = data[-long_win:].reset_index(drop=True)

    pre_short_rsi = compute_rsi(pre_short_windowed_data)
    pre_long_rsi = compute_rsi(pre_long_windowed_data)
    
    short_rsi = compute_rsi(short_windowed_data)
    long_rsi = compute_rsi(long_windowed_data)
    
    #buy
    if pre_short_rsi < pre_long_rsi and short_rsi > long_rsi and (openPrice-ma)>alpha:
        return 1
    #sell
    elif pre_short_rsi > pre_long_rsi and short_rsi < long_rsi and (openPrice-ma)<-beta:
        return -1
    #hold
    else:
        return 0

def computeReturnRate( windowSize, alpha, beta, short_win,long_win):
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
        action[evalDays-ic] = myStrategy(dailyOhlcvFile,minutelyOhlcvFile,openPricev[evalDays-ic], windowSize, alpha, beta, short_win, long_win)
        
        #data = dailyOhlcvFile['open']
        #windowedData = data[-win:].reset_index(drop=True)
        #rsi = compute_rsi(windowedData)
        #print("day_%d_rsi=%d action_%d=%d"%(evalDays-ic,rsi,evalDays-ic,action[evalDays-ic]))
        
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
    returnRate = (total[-1] - capitalOrig)/capitalOrig
    return returnRate

if __name__=='__main__':
    os.chdir('C:/Users/12157/Desktop/hw-108/fintech/fintech_final')
    returnRateBest=-1.00     # Initial best return rate
    dailyOhlcv = pd.read_csv('TX_daily.csv')
    minutelyOhlcv = pd.read_csv('TX_minutely.csv')
#    dailyOhlcv = pd.read_csv(sys.argv[1])
#    minutelyOhlcv = pd.read_csv(sys.argv[2])
    # search rsi_win, long_win, short_win, sell, buy
    win_min = 0; win_max= 10;    # Range of windowSize to explore
    a_min = 0; a_max =8;
    b_min = 0; b_max = 8;
    short_win_min = 5; short_win_max=10;
    long_win_min = 12; long_win_max=20
    # Start exhaustive search
    for win in range(win_min,win_max+1):
        print("window=%d  "% win)
        for alpha in range(a_min,a_max+1):
            print("alpha=%d  "%alpha)
            for beta in range(b_min,b_max+1):
                print("beta=%d\t"%beta)
                for short in range(short_win_min, short_win_max+1):            # For-loop for alpha
                        print("short_win=%d  " %(short))
                        for long in range(long_win_min, long_win_max+1):        # For-loop for beta
                            print("long_win=%d" %(long))    # No newline
                            returnRate = computeReturnRate( win, alpha, beta, short,long)        # Start the whole run with the given parameters
                            print("\t ==> returnRate=%f" %(returnRate))
                            if returnRate > returnRateBest:        # Keep the best parameters
                                winBest = win
                                alphaBest = alpha
                                betaBest = beta
                                shortBest=short
                                longBest=long
                                returnRateBest=returnRate
        print("Best settings: win=%d, alpha=%d, beta=%d, short=%d, long=%d ==> returnRate=%f" 
              %(winBest,alphaBest,betaBest, shortBest, longBest,returnRateBest))        # Print the best result

'''
    for windowSize in range(rsi_win_min, rsi_win_max+1):        # For-loop for windowSize
        print("windowSize=%d" %(windowSize))
        for long in range(long_win_min, long_win_max+1):            # For-loop for alpha
            print("\tlong_win=%d" %(long))
            for short in range(short_win_min, short_win_max+1):        # For-loop for beta
                print("\t\tshort_win=%d" %(short))    # No newline
                for sell in range(sell_min, sell_max+1):
                    print("\t\t\tsell=%d" %(sell))
                    for buy in range(buy_min,buy_max+1):
                        print("\t\t\t\tbuy=%d" %(buy), end="")
                        returnRate = computeReturnRate(windowSize, long, short, sell, buy)        # Start the whole run with the given parameters
                        print(" ==> returnRate=%f " %(returnRate))
                        
                        if returnRate > returnRateBest:        # Keep the best parameters
                            windowSizeBest=windowSize
                            longBest=long
                            shortBest=short
                            sellBest=sell
                            buyBest=buy
                            returnRateBest=returnRate
    print("Best settings: windowSize=%d, long=%d, short=%d, sell=%d, buy=%d ==> returnRate=%f" 
          %(windowSizeBest,longBest,shortBest,sellBest,buyBest,returnRateBest))        # Print the best result
'''

    
