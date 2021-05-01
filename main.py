from ProfitCalculator import *
from getCsvFiles import *


symbol = input("Symbol:").upper()


save_data(symbol=symbol,datetime_interval="hour",limit=2000)



daily_df=daily_profit_calculator(symbol=symbol)



#Creating a dataframe that contains weekly profits
moneyL,percentages = weekly_profit_calculator(df=daily_df)
data = {"Percentages":percentages,"Money($)":moneyL}
weekly_df = pd.DataFrame(data,index=[f"{x}th week" for x in range(1,len(daily_df)//7+1)])



print(weekly_df)


