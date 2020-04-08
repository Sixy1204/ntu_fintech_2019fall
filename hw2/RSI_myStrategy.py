def compute_rsi(windowedData):# calculate RSI
    sma_u = 0
    sma_d = 0

    windowSize = len(windowedData)
    for i in range(windowSize - 1):
        if windowedData[i] <= windowedData[i + 1]:
            sma_u += (windowedData[i + 1] - windowedData[i])
        else:
            sma_d += (windowedData[i] - windowedData[i + 1])
    return sma_u / (sma_d + sma_u)


def myStrategy(pastData, currPrice, stockType):
    import numpy as np
    # Explanation of my approach:
    #     # 1. Technical indicator used: RSI
    #     # 2. calculate data RSI
    #          if RSI > buy(0.8) and preshortRSI < prelongRSI and shortRSI > longRSI ==> buy    黃金交叉且RSI大於buy的閾值
    #     #    if RSI < sale(0.2) preshortRSI > prelongRSI and shortRSI < longRSI ==> sell       死亡交叉且RSI小於buy的閾值
    #     # 3. Modifiable parameters: buy, sale, windowSize, ShortwindowSize and LongwindowSize for RSI
    #     # 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
    # stockType='SPY', 'IAU', 'LQD', 'DSI'
    # Set parameters for different stocks
    #  Decision of the current day by the current price, with 5 modifiable parameters
    paramSetting = {'SPY': {'buy': 0.3, 'sale': 0.1, 'windowSize': 5, 'ShortwindowSize': 20, 'LongwindowSize': 49},
                    'IAU': {'buy': 0.0, 'sale': 0.4, 'windowSize': 5, 'ShortwindowSize': 8, 'LongwindowSize': 21},
                    'LQD': {'buy': 0.1, 'sale': 0.4, 'windowSize': 11, 'ShortwindowSize': 20, 'LongwindowSize': 24},
                    'DSI': {'buy': 0.0, 'sale': 0.1, 'windowSize': 4, 'ShortwindowSize': 20, 'LongwindowSize': 39}}
    windowSize = paramSetting[stockType]['windowSize']
    buy = paramSetting[stockType]['buy']
    sale = paramSetting[stockType]['sale']
    ShortwindowSize = paramSetting[stockType]['ShortwindowSize']
    LongwindowSize = paramSetting[stockType]['LongwindowSize']

    dataLen = len(pastData)

    if dataLen < max(LongwindowSize + 1, windowSize):#If given price vector is small than max windowsize, action = 0
        return 0

    windowedData = pastData[-windowSize:]
    RSI = compute_rsi(windowedData)

    PreShortwindowedData = pastData[-ShortwindowSize - 1:-1]
    ShortwindowedData = pastData[-ShortwindowSize:]
    PreLongwindowedData = pastData[-LongwindowSize - 1:-1]
    LongwindowedData = pastData[-LongwindowSize:]

    preshortRSI = compute_rsi(PreShortwindowedData)
    prelongRSI = compute_rsi(PreLongwindowedData)
    shortRSI = compute_rsi(ShortwindowedData)
    longRSI = compute_rsi(LongwindowedData)

    if preshortRSI < prelongRSI and shortRSI > longRSI and RSI > buy:
        return 1
    elif preshortRSI > prelongRSI and shortRSI < longRSI and RSI < sale:
        return -1
    else:
        return 0

