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

# Enum settings
loopI = [7,30,1]
enumI = ceil((loopI[1] - loopI[0]) / loopI[2])
loopII = [7,30,1]
enumII = ceil((loopII[1] - loopII[0]) / loopII[2])
loopIII = [7,30,1]
enumIII = ceil((loopIII[1] - loopIII[0]) / loopIII[2])

count = 0
maxCount = enumI*enumII*enumIII



# Load datas
data_filepath = "ETHUSDT_1644595200000_1643072400000_1h.json"
filepath = getcwd() + "\\data\\" + data_filepath

# Generate dataframe
df = dataframe_generator(filepath)
df = indicator_gen_optimizer(df, enumI, enumII, enumIII)




for i in range(loopI[0], loopI[1], loopI[2]):
    for j in range(loopII[0], loopII[1], loopII[2]):
        for i in range(loopIII[0], loopIII[1], loopIII[2]):
            # -- Update loading screen
            count += 1
            print("Loading...",count,'/',maxCount)
            dt,data = backtest(df,trade_set)

        