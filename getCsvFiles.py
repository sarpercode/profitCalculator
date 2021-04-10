import requests
import pandas as pd
from requests.api import request
import os



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
            #print("[INFO] The data is saved")

    else:
        print("[INFO] No data found")

    