import requests
from datetime import datetime
import pandas as pd
from requests.api import request
import matplotlib.pyplot as plt
import os
import time








def download_data(symbol,datetime_interval,limit):

    supported_intervals = {'minute','hour','day'}

    assert datetime_interval in supported_intervals,\
        'datetime_interval should be one of %s' % supported_intervals

    to_symbol = "USD"
    
    try:
        base_url = "https://min-api.cryptocompare.com/data/histo"
        url = '%s%s' %(base_url,datetime_interval)
        params = {'fsym':symbol,'tsym':to_symbol,
                    'limit':limit,'aggregate':1}
            
        request = requests.get(url=url,params=params)
        data = request.json()
        print(f'[INFO] We got the data')
        return data

    except:
        print(f"[INFO] There is a problem with the process")

def convert_df(data):

    df = pd.json_normalize(data,['Data'])
    df['datetime'] = pd.to_datetime(df.time,unit="s")
    df = df[['datetime','low','high']]
    return df

def save_data(symbol,datetime_interval,limit):

    data = download_data(symbol=symbol,datetime_interval=datetime_interval,limit=limit)

    if data is not None:

        if not os.path.exists(f"{symbol}_{datetime_interval}.csv"):

            df = convert_df(data)
            df.to_csv((f"{symbol}_{datetime_interval}.csv"),index=False)
            print("[INFO] The data is saved")

    else:
        print("[INFO] No data found")

symbol = input("Symbol:")
save_data(symbol=symbol,datetime_interval="hour",limit=2000)
#save_data(symbol,datetime_interval="day",limit=82)



def daily_profit_calculator(symbol):

    while True:
        try:
            df = pd.read_csv(f"{symbol}_hour.csv")
            print("[INFO] The file has read")
            break
        except:
            print("[INFO] Can't find the csv file")
            time.sleep(3)
            print("[INFO] Trying to download")
            try:
                save_data(symbol=symbol)
            except:
                print("[INFO] There is something wrong with it")
                break

    
    df = df.iloc[13:]
    di_df = df.set_index(pd.DatetimeIndex(df['datetime'].values))
    di_df = di_df.drop(['datetime'],axis=1)
    array = di_df.values


    profits = []
    count = 0
    num_day = len(df)//24

    for dayz in range(num_day):
        
        dummy_diff = 0
        for i in range(24):
            for j in range(2):

                if j % 2 == 0:
                    
                    low_row,loc1 = array[i+count][j],(i+count)

                
                if j % 2 == 1:

                    for k in range(24-i):

                        diff,loc2 = array[k+count][j] - low_row,(k+count)
                        if diff > dummy_diff:
                            dummy_diff = diff
                            h = loc2
                            l = loc1
        



        highest = float(array[h][1])
        lowest = float(array[l][0])

        percentage = ((highest-lowest)*100)/lowest
        profits.append(percentage)
        count += 24



    daily_csv = save_data(symbol=symbol,datetime_interval="day",limit=num_day)
    daily_df = pd.read_csv(daily_csv)

    index = len(daily_df) - 1

    daily_df.drop(index=index,inplace=True)
    daily_df.drop(['low'],axis=1,inplace=True)
    daily_df.drop(['high'],axis=1,inplace=True)
    daily_df['Percentage'] = profits

    print(daily_df)










        