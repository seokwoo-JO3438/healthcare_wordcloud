import pandas_datareader as web
import pandas as pd
import datetime
# tickers(healthcare 기업 종목코드), sets(기업의 주가 데이터를 저장할 데이터) list 생성
tickers = ['MDT', 'JNJ', 'GE', 'ABT', 'PHIA.AS', 'BDX', 'CAH', \
           'SIEGY', 'SYK', 'BAX', 'BSX', 'DHR', 'EL', 'ZBH', 'ALC', \
           'FMS', 'OCPNY', 'TRUMY', 'SNN', 'XRAY', 'EW', 'ISRG', 'HOCPY', \
           'HOLX', 'VAR', 'HRC', 'SOON.SW']
sets = ['data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', \
        'data8', 'data9', 'data10', 'data11', 'data12', 'data13', 'data14', 'data15', \
        'data16', 'data17', 'data18', 'data19', 'data20', 'data21', 'data22', 'data23', \
        'data24', 'data25', 'data26', 'data27']
data = []
five_days_later = []
five_days_before = []
a = 0
# AdjClose의 전날 대비 증가, 감소를 0 or 1로 표시
for i, j in zip(tickers, sets):
    j = web.DataReader(i, data_source='yahoo', start='1997-01-01', end='today')
    j.rename(columns={'Adj Close':'AdjClose'}, inplace=True)
    j['PriceLag1'] = j['AdjClose'].shift(-1)
    j['PriceDiff'] = j['PriceLag1']-j['AdjClose']
    j['DailyReturn'] = j['PriceDiff']/j['AdjClose']
    j['UpDown'] = [1 if j['DailyReturn'].loc[date] > 0 else 0 for date in j.index]
    j = j.filter(['AdjClose','UpDown'])
    j.rename(columns={'UpDown':i+'_Up(1)/Down(0)'}, inplace=True)
    j.filter([i+'_Up(1)/Down(0)'])
    sets[a] = j
    a += 1
data = pd.concat(sets, join='outer', axis=1)
data = data[data>0]
# 최대한 1이 많은 날짜 60일 추출
for i in tickers:
    data = data[(data[i+'_Up(1)/Down(0)'] == 1)]
    if len(data.index) < 61:
        break
date = data.index

# 추출한 60일의 전 2일, 후 5일 데이터 저장
for i in range(len(date)):
    five_days_later.append(date[i] + datetime.timedelta(days=5))
    five_days_later[i] = five_days_later[i].strftime('%Y.%m.%d')

    five_days_before.append(date[i] - datetime.timedelta(days=2))
    five_days_before[i] = five_days_before[i].strftime('%Y.%m.%d')