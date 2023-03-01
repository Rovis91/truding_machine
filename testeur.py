import pandas as pd
from backtest_tool.backtest_analysis import *
from backtest_tool.backtest_run import *
from backtest_tool.database_strategy_generator import *
from os import getcwd

strategy_name =  'strategie_name'


sm = __import__('Strategies.' + strategy_name, fromlist=['*'])
trade_set, param_combinations = sm.parameters()

#Path to the datas
data_filepath = "ETHUSDT_1678795200000_1677000000000_1h.json" # 1 year
#data_filepath = "ETHUSDT_1644595200000_1643072400000_1h.json" # 1 month
filepath = getcwd() + "\\data\\" + data_filepath


# Generate dataframe
df = dataframe_generator(filepath)
df = indicator_gen(df)
# df.drop(df.columns.difference(['open','high','low','close','volume','RSI','Buy Signal','Sell Signal','MACD_DIFF']), 1, inplace=True)


dt,data = backtest(df,trade_set,strategy_name)

if data is False:
    print("No trades")
else:
    analysis_backtest(df,dt,data)
