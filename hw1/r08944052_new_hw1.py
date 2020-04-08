import sys
import numpy as np
import pandas as pd
import datetime as dt

#select csv file
file = "C:/Users/12157/Desktop/hw-108/fintech/hw1/Daily_2019_09_05.csv"
#file = str(sys.argv[1])

#load in data
df = pd.read_csv(file, 
					encoding='big5',
					skiprows=[0],
					names=['Date', 'P_id', 'Due_month', 'Time', 'Price', 'Amount', 'Close_month_price', 'Far_month_price', 'Open_price'])

#find the third wednesday(due_date) of the month, mon=0, sun=6
def third_wed(y,m):
	day = 21 - (dt.date(y, m, 1).weekday() + 4) % 7		
	return dt.date(y,m,day)

date = np.amax(df.Date)
date = str(date)
month = int(date[0:6])
third_wed = int(str(third_wed(int(date[0:4]), int(date[4:6]))).split('-')[-1])
if int(date[6:]) > third_wed:
    due_month = month+1
else:
    due_month = month

#Select data
df = df[['Date', 'P_id', 'Due_month', 'Time', 'Price']]
df = df[df['P_id']=='TX     ']
midx = pd.to_numeric(df.Due_month.str.replace('/',''))
tidx = pd.to_numeric(df.Time)
df = df[midx==due_month][:]
df = df[tidx>=84500][:]
df = df[tidx<=134500][:]
idf = df.reset_index(drop=True)

#Compute OHLC
Open = int(idf.Price[0])
High = int(np.amax(idf.Price))
Low = int(np.amin(idf.Price))
Close = int(idf.Price[len(idf)-1])
print(Open,High,Low,Close)

