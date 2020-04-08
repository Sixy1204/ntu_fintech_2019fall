import pandas as pd
import numpy as np
from talib import RSI, BBANDS
import matplotlib.pyplot as plt
import os  
os.chdir('C:/Users/12157/Desktop/hw-108/fintech/hw2')
df = pd.read_csv('SPY.csv')
close = df['Adj Close']
 

def myStrategy(pastPriceVec, currentPrice, stockType):
    # Explanation of my approach:
	# 1. Technical indicator used: MA
	# 2. if price-ma>alpha ==> buy
	#    if price-ma<-beta ==> sell
	# 3. Modifiable parameters: alpha, beta, and window size for MA
	# 4. Use exhaustive search to obtain these parameter values (as shown in bestParamByExhaustiveSearch.py)
	'''
	if len(pastPriceVec) == 0:
		prePrice = pastPriceVec
	else:
		prePrice = pastPriceVec[-1]
	'''
	
	import numpy as np
	# stockType='SPY', 'IAU', 'LQD', 'DSI'
	# Set parameters for different stocks
	paramSetting={'SPY': {'alpha':6, 'beta':9, 'windowSize':8},
					'IAU': {'alpha':0, 'beta':2, 'windowSize':26},
					'LQD': {'alpha':0, 'beta':1, 'windowSize':5},
					'DSI': {'alpha':2, 'beta':10, 'windowSize':17}}
	windowSize=paramSetting[stockType]['windowSize']
	alpha=paramSetting[stockType]['alpha']
	beta=paramSetting[stockType]['beta']
	action=0		# action=1(buy), -1(sell), 0(hold), with 0 as the default action
	dataLen=len(pastPriceVec)		# Length of the data vector
	if dataLen==0:
		return action

	# Compute ma
	if dataLen<windowSize:
		ma=np.mean(pastPriceVec)	# If given price vector is small than windowSize, compute MA by taking the average
		if stockType in ['SPY']:
			if (currentPrice-ma)<-beta:	# If price-ma < -beta ==> sell
				action=1
			if (currentPrice-ma)>alpha:		# If price-ma > alpha ==> buy
				action=-1

		elif stockType in ['IAU','LQD','DSI']:
			if (currentPrice-ma)>alpha:		# If price-ma > alpha ==> buy
				action=1
		
			if (currentPrice-ma)<-beta:	# If price-ma < -beta ==> sell
				action=-1
	else:
		window10=pastPriceVec[-20:]	# Compute the normal MA using windowSize  
		ma20=np.mean(window10)
		window20=pastPriceVec[-60:]
		ma60=np.mean(window20)
		if ma20>ma60:
			action = 1
		else:
			action = -1
	
		

	return action