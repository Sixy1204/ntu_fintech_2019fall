# -*- coding: utf-8 -*-
"""
@author: Xiaoyu SI 
NTU GINM
r08944052
"""
import sys
import numpy as np
import pandas as pd
import datetime as dt

#select csv file
file = str(sys.argv[1])

#load in data
df = pd.read_csv(file, 
					encoding='big5',
					skiprows=[0],
					names=['Date', 'P_id', 'Due_month', 'Time', 'Price', 'Amount', 'Close_month_price', 'Far_month_price', 'Open_price'])

df.drop('Amount',axis=1,inplace=True)
df.drop('Close_month_price',axis=1,inplace=True)
df.drop('Far_month_price',axis=1,inplace=True)
df.drop('Open_price',axis=1,inplace=True)

#Paring data
id_list = []
p_id = [str(x) for x in df.P_id]
for i, p in enumerate(p_id):
    if p.strip()=="TX":
        id_list.append(i)

input_df = df[id_list[0]:(id_list[-1]+1)]
input_df = input_df.reset_index(drop=True)

#find the third wednesday(due_date) of the month, mon=0, sun=6
def third_wed(y,m):
	day = 21 - (dt.date(y, m, 1).weekday() + 4) % 7		
	return dt.date(y,m,day)

date = np.amax(input_df.Date)
date = str(date)
month = int(date[0:6])
third_wed = int(str(third_wed(int(date[0:4]), int(date[4:6]))).split('-')[-1])
if int(date[6:]) > third_wed:
    due_month = month+1
else:
    due_month = month

#compute OHLC
trade_p = []
for i in range(len(input_df)):
    try:
        if int(input_df.Due_month[i].strip())==due_month:
            if input_df.Time[i]>=84500 and input_df.Time[i]<=134500:
                trade_p.append(int(input_df.Price[i]))
    except:
        pass    
        
Open = trade_p[0]
High = np.amax(trade_p)
Low = np.amin(trade_p)
Close = trade_p[-1]
print(Open,High,Low,Close)



