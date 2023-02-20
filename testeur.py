import pandas as pd
from database_strategy_generator import *
from backtest_run import backtest
from backtest_analysis import analysis_backtest
from os import getcwd

trade_set={
    "pairName" : "ETHUD",
    "leverage" : 1,
    "initialwallet" : 1000,
    "makerFee" : 0.0002,
    "takerFee" : 0.0007,
    "SL_ratio" : 0.1,
    "takeProfit" : 0.1,
    "longLiquidationPrice" : 500000,
    "shortLiquidationPrice" : 0,
    }

#Path to the datas
data_filepath = "ETHUSDT_1644595200000_1643072400000_1h.json"
filepath = getcwd() + "\\data\\" + data_filepath

# Generate dataframe
df = dataframe_generator(filepath)
df = indicator_gen(df)
dt,data = backtest(df,trade_set)
analysis_backtest(df,dt,data)
