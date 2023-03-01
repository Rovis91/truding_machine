# Imports
from os import getcwd
import pandas as pd
import itertools
import numpy as np
import matplotlib.pyplot as plt
from backtest_tool.backtest_analysis import *
from backtest_tool.backtest_run import *
from backtest_tool.database_strategy_generator import *

#Select here the strategie to test
strategy_name = 'chatGPT_strat'
sm = __import__('Strategies.' + strategy_name, fromlist=['*'])



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

# Load datas
data_filepath = "ETHUSDT_1644595200000_1643072400000_1h.json"
filepath = getcwd() + "\\data\\" + data_filepath



df = dataframe_generator(filepath)


param1_range = np.arange(5, 25, 10)
param2_range = np.arange(10, 210, 50)

def optimize_strategy(df, trade_set,strategy_name, *param):
    
    # Generate all possible combinations of parameter values
    param_combinations = list(itertools.product(*param))
    combinations=len(param_combinations)
    tested_combinations = 1
    # Initialize a list to store the backtest results for each parameter combination
    backtest_results = []

    # Test the strategy with each combination of parameter values
    for params in param_combinations:
        # -- Clean --
        df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)

        print("Testing paramameters: ", params, "    (", tested_combinations,"//",combinations,')')
        indicators = [{'name': str(params[0]), 'func': ta.trend.sma_indicator, 'params': {'close': df['close'], 'window': params[0]}}, 
                      {'name': str(params[1]), 'func': ta.momentum.stochrsi, 'params': {'close': df['close'], 'window': params[1],'smooth1': 3,'smooth2': 3, 'fillna': True}}]
        df=indicator_gen_optimizer(df, indicators)
        trades, data = backtest(df, trade_set,strategy_name)
        
        backtest_results.append((params, data['wallet'],data['totalTrades'],data['AveragePercentagePositivTrades'],data['winRateRatio'],data['tradesPerformance']))
        tested_combinations += 1
        
        

    # Find the best parameter combination based on the backtest results
    result= max(backtest_results, key=lambda x: x[1])
    
    
    
    '''
    # Create a heatmap of the parameter combinations and corresponding backtest results
    param1_values = [x[0] for x in param_combinations]
    param2_values = [x[1] for x in param_combinations]
    profit_values = [x[1] for x in backtest_results]

    param1_mesh, param2_mesh = np.meshgrid(param1_range, param2_range)
    profit_mesh = np.array(profit_values).reshape(len(param2_range), len(param1_range))

    fig, ax = plt.subplots()
    heatmap = ax.pcolormesh(param1_mesh, param2_mesh, profit_mesh, cmap='YlOrRd')
    fig.colorbar(heatmap, ax=ax)

    ax.set_xlabel("Parameter 1")
    ax.set_ylabel("Parameter 2")
    ax.set_title("Backtest Results")

    plt.show()
    '''
    return result 


result = optimize_strategy(df, trade_set,strategy_name, param1_range, param2_range)


for x in range(len(result)):
    print(result[x])