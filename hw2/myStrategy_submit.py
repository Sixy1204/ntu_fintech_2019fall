'''
1.SPY使用逆勢指標：
currentPrice<ma-beta===>buy
currentPrice>ma+alpha===>sell
 
2.IAU,LQD,DSI則使用順勢指標：
currentPrice>ma+alpha===>buy
currentPrice<ma-beta===>sell
 
3.對所有股票以500筆資料為區間搜尋最佳參數
'''
import numpy as np
 
def myStrategy(pastPriceVec, currentPrice, stockType):
    paramSetting={'SPY': {'alpha':[2,0,5,4,3,2,4], 'beta':[2,1,4,3,0,3,0], 'windowSize':[4,5,4,15,1,15,4]},
                    'IAU': {'alpha':[0,0,0,0,1,1,0], 'beta':[0,1,1,0,0,0], 'windowSize':[6,0,0,8,0,0,0]},
                    'LQD': {'alpha':[0,2,0,0,1,0,0], 'beta':[2,1,0,1,2,1,1], 'windowSize':[0,7,0,0,2,5,10]},
                    'DSI': {'alpha':[3,0,0,0,2,0,3], 'beta':[0,3,0,1,4,1,4], 'windowSize':[0,1,1,1,1,1,1]}}
    windowSize=paramSetting[stockType]['windowSize']
    alpha=paramSetting[stockType]['alpha']
    beta=paramSetting[stockType]['beta']
    idx = len(pastPriceVec)-1
    if idx <500:
        i=0
    elif idx<1000:
        i=1
    elif idx<1500:
        i=2
    elif idx<2000:
        i=3
    elif idx<2500:
        i=4
    elif idx<3000:
        i=5
    else:
        i=6
    if stockType =='IAU':
        windowSize=26
        alpha=0
        beta=2
    else:
        windowSize=windowSize[i]
        alpha=alpha[i]
        beta=beta[i]
    action=0        # action=1(buy), -1(sell), 0(hold), with 0 as the default action
    dataLen=len(pastPriceVec)        # Length of the data vector
    if dataLen==0:
        return action
    # Compute ma
    if dataLen<windowSize:
        ma=np.mean(pastPriceVec)    # If given price vector is small than windowSize, compute MA by taking the average
    else:
        windowedData=pastPriceVec[-windowSize:]        # Compute the normal MA using windowSize
        ma=np.mean(windowedData)
    # Determine action
    if stockType=='SPY':
        if (currentPrice-ma)>alpha:        # If price-ma > alpha ==> sell
            action=-1
        elif (currentPrice-ma)<-beta:    # If price-ma < -beta ==> buy
            action=1
    else:
        if (currentPrice-ma)>alpha:        # If price-ma > alpha ==> buy
            action=1
        elif (currentPrice-ma)<-beta:    # If price-ma < -beta ==> sell
            action=-1
    return action