import itertools
import numpy as np
import matplotlib.pyplot as plt
from backtest_run import backtest   
from database_strategy_generator import *
from os import getcwd
import pandas as pd

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


param1_range = np.arange(1, 201, 10)
param2_range = np.arange(1, 20, 1)

def optimize_strategy(df, trade_set, *param):

    # Generate all possible combinations of parameter values
    param_combinations = list(itertools.product(*param))
    # Initialize a list to store the backtest results for each parameter combination
    backtest_results = []

    # Test the strategy with each combination of parameter values
    for params in param_combinations:

        indicators = [{'name': str(params[0]), 'func': ta.trend.sma_indicator, 'params': {'close': df['close'], 'window': params[1]}},
                      {'name': str(params[1]), 'func': ta.momentum.stochrsi, 'params': {'close': df['close'], 'window': params[2],'smooth1': 3,'smooth2': 3}}]
        df_n=indicator_gen(df, indicators)
        print(df_n)
        trades, data = backtest(df_n, trade_set)
        backtest_results.append((params, data['wallet'],data['totalTrades'],data['AveragePercentagePositivTrades'],data['winRateRatio'],data['tradePerformance']))

    # Find the best parameter combination based on the backtest results
    best_params, best_profit = max(backtest_results, key=lambda x: x[1])

    print("Best parameters: ", best_params)
    print("Best profit: ", best_profit)

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

    return best_params, backtest_results


best_params, backtest_results = optimize_strategy(df, trade_set, param1_range, param2_range)
