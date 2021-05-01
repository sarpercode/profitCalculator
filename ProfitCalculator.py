from datetime import datetime
import pandas as pd
from requests.api import request
import os
import time
from getCsvFiles import *



def daily_profit_calculator(symbol):

    #Checking the pdf's existance
    #If it's not exits trying to download
    while True:
        try:
            df = pd.read_csv(f"{symbol}_hour.csv")
            #print("[INFO] The file has read")
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


    if not os.path.exists(f"{symbol}_day.csv"):

        daily_csv = save_data(symbol=symbol,datetime_interval="day",limit=num_day)
        daily_df = pd.read_csv(f"{symbol}_day.csv")

    else:
        daily_df = pd.read_csv(f"{symbol}_day.csv") 


    index = len(daily_df) - 1

    daily_df.drop(index=index,inplace=True)
    daily_df.drop(['low'],axis=1,inplace=True)
    daily_df.drop(['high'],axis=1,inplace=True)
    daily_df['Percentage'] = profits
    print(daily_df)
    return daily_df




def weekly_profit_calculator(df):
    
    percentages = []
    num_of_week = len(df)//7
    
    moneyL = []
    count = 0
    money = 1
    for week in range(num_of_week):
        dummy_money = 1
        for i in range(7):

            percentage = float(df['Percentage'][i+count])
            dummy_money = dummy_money + dummy_money * percentage/100
        
        
        weekly_percentage = (dummy_money*100)-100
        money = money + money*weekly_percentage/100
        percentages.append(weekly_percentage)
        moneyL.append(money)

        count +=7


    #print(moneyL)
    #print(percentages)
    return moneyL,percentages
