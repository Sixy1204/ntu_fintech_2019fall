import numpy as np
import pandas as pd
import os
import copy
os.chdir('C:/Users/12157/Desktop/hw-108/fintech\hw3')
df = pd.read_csv('priceMat.txt', delimiter=' ')

def myOptimAction(priceMat, transFeeRate):
	# Explanation of my approach:
	# 1. Technical I used: Dynamic programming
	# 2. Record the way that we get
	# 	 the best stocks holding and cash holding every day.
	#	 Thus we can maximize final cash holding and then trace back.
	# 3. You should sell before buy to get cash each day
	# default
	capital = 1000
	dataLen, stockCount = priceMat.shape  # day size & stock count   
	actionMat = []  # An k-by-4 action matrix which holds k transaction records.
	dp = np.zeros(5)
	#DP initial
	for i in range(stockCount):
		dp[i] = capital*(1-transFeeRate)/priceMat[0][i]
	dp[4] = capital
	trace = np.zeros((dataLen,5))
	record_dp = np.zeros((dataLen,5))
	record_dp[0] = dp
	#recursion
	for day in range( 1, dataLen) :
		old_dp = copy.deepcopy(dp)
		#sell stock to gain money
		sell = old_dp[:-1]*priceMat[day]*(1-transFeeRate)
		max_money = max(sell)
		max_stock_id = np.argmax(sell)
		
		if max_money > old_dp[-1]:
			dp[-1] = max_money
			trace[day][-1] = max_stock_id
		else:
			trace[day][-1] = -1
			max_stock_id = -1
			max_money = dp[-1]
		trace_save = pd.DataFrame(trace)
		trace_save.to_csv("trace.csv",header=False,index=False)
		#buy stocks
		for s in range(stockCount):
			buy = max_money/priceMat[day][s]*(1-transFeeRate)
			if buy > old_dp[s]:
				dp[s] = buy
				trace[day][s] = max_stock_id
			else:
				trace[day][s] = s
		
		record_dp[day] = dp

	#tracing back
	record_from = [] #tracing back from
	diff = []
	from_ = trace[-1,-1]
	for t in reversed(range(0,dataLen)):
		record_from.append(from_)
		from_ = trace[int(t),int(from_)]
		prev = trace[int(t-1),int(from_)]
		if from_!=prev and t>1:
			from_=prev
			diff.append(t-1)
	record_from.reverse()
		
	#action[day,buy,sell,money]
	back = -1
	for i in diff:
		action = [0,0,0,0]
		action[0] = i
		action[1] = int(record_from[i])
		action[2] = back
		if int(record_from[i])==-1:
			action[3] = record_dp[i-1,-1]
		else:
			action[3] = priceMat[i,int(record_from[i])]*record_dp[i-1,int(record_from[i])]
		back = int(record_from[i])
		actionMat.append(action)
	actionMat.reverse()
	return actionMat
	
# Compute return rate over a given price Matrix & action Matrix
def computeReturnRate(priceMat, transFeeRate, actionMat):
	capital = 1000	  # Initial available capital
	capitalOrig = capital	  # original capital
	stockCount = len(priceMat[0])	# stack size
	suggestedAction = actionMat	   # Mat of suggested actions
	actionCount = len(suggestedAction)
	
	stockHolding = np.zeros((actionCount,stockCount))	# Mat of stock holdings
	realAction = np.zeros((actionCount,1))	  # Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	preDay = 0	# previous action day
	
	# Run through each action, should order by day
	for i in range(actionCount):
		actionVec = actionMat[ i ]
		day = actionVec[0] # The index of day
		a = actionVec[1] # The index of "from" stock
		b = actionVec[2] # The index of "to" stock
		z = actionVec[3] # The equivalent cash for such transaction.
		currentPriceVec = priceMat[day]	 # current priceVec
		
		# check action day
		if day >= preDay and day >= 0 and z > 0 :
			# get real action by suggested action
			if i > 0:
				stockHolding[i] = stockHolding[i-1]	 # The stock holding from the previous action day
				preDay = day  # previous action day
			
			if a == -1 and b >= 0 and capital > 0 :	 # Suggested action is "buy"
				currentPrice = currentPriceVec[b]  # The current price of stock
				if capital < z :  # "buy" allonly if you don't have enough capital
					z = capital
				stockHolding[i][b] += z*(1-transFeeRate) / currentPrice # Buy stock using cash
				capital = capital - z  # Cash
				realAction[i] = 1
			elif b == -1 and a >= 0 and stockHolding[i][a] > 0 :  # Suggested action is "sell"
				currentPrice = currentPriceVec[a]  # The current price of stock
				sellStock = z / currentPrice
				if stockHolding[i][a] < sellStock :  # "sell" all only if you don't have enough stock holding
					sellStock = stockHolding[i][a]
				getCash = sellStock * currentPrice*(1-transFeeRate)	 # Sell stock to have cash
				capital = capital + getCash	 # get cash from sell stock
				stockHolding[i][a] -= sellStock	 # Stocking holding
				realAction[i] = -1
			elif a >= 0 and b >= 0 and stockHolding[i][a] > 0 :  # Suggested action is "buy" and "sell"
				currentPriceSell = currentPriceVec[a]  # The current price of sell stock
				currentPriceBuy = currentPriceVec[b]  # The current price of buy stock
				sellStock = z / currentPriceSell
				if stockHolding[i][a] < sellStock :  # "sell" all only if you don't have enough stock holding
					sellStock = stockHolding[i][a]
				getCash = sellStock * currentPriceSell*(1-transFeeRate)	 # Sell stock to have cash
				stockHolding[i][a] -= sellStock	 # Stocking holding
				stockHolding[i][b] += getCash*(1-transFeeRate) / currentPriceBuy # Buy stock using cash
				realAction[i] = 2
			else:
				assert False
		else:
			assert False
			
	# calculate total cash you get at last day
	total = capital
	for stock in range(stockCount) :
		currentPriceVec = priceMat[ actionMat[-1][0] ]
		total += stockHolding[-1][stock] * currentPriceVec[stock]*(1-transFeeRate)	# Total asset, including stock holding and cash 
		
	returnRate=(total-capitalOrig)/capitalOrig	# Return rate of this run
	return returnRate
	
transFeeRate = 0.01
priceMat = df.values	# Get price as the m×n matrix which holds n stocks' price over m days
actionMat = myOptimAction(priceMat, transFeeRate)	# Obtain the suggested action
rr = computeReturnRate(priceMat, transFeeRate, actionMat)  # Compute return rate
print("rr=%f%%" %(rr*100))
	