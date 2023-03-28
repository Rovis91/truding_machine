# Imports
from os import getcwd
import pandas as pd
import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from backtest_tool.backtest_analysis import *
from backtest_tool.backtest_run import *
from backtest_tool.database_strategy_generator import *

#Select here the strategie to test
strategy_name = 'strategie_test'
sm = __import__('Strategies.' + strategy_name, fromlist=['*'])

# Load datas
data_filepath = "ETHUSDT_1644595200000_1643072400000_1h.json"
#data_filepath = "ETHUSDT_1678795200000_1677000000000_1h.json" # 1 year
filepath = getcwd() + "\\data\\" + data_filepath



def optimize_strategy(filepath,strategy_name):
    #Import strategie settings 
    trade_set, param_combinations = sm.parameters()
    combinations=len(param_combinations)
    tested_combinations = 1
    # Initialize a list to store the backtest results for each parameter combination
    backtest_results = []

    # Test the strategy with each combination of parameter values
    for params in param_combinations:
        df = dataframe_generator(filepath)
        trade_set, trash = sm.parameters()
        print("Testing paramameters: ", params, "    (", tested_combinations,"//",combinations,')')
        
        # # -- Clean and regenerate --
        #df.drop(df.columns.difference(['open','high','low','close','volume']))
        df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)
        
        df = sm.ndf_gen(df,params)
        
        # -- Backtest --
        trades, data = backtest(df, trade_set,strategy_name)
        
        if data is False:
            print("No trades")
        else:
            backtest_results.append((params, data['wallet'],data['totalTrades'],data['AveragePercentagePositivTrades'],data['winRateRatio'],data['tradesPerformance']))
        tested_combinations += 1
        
       

    # Find the best parameter combination based on the backtest results
    result = max(backtest_results, key=lambda x: x[1])

    
    
    return backtest_results,result 


#result = optimize_strategy(df, strategy_name)
backtest_results,result = optimize_strategy(filepath, strategy_name)
print(f"Best result {result} \n \n")

# for x in range(backtest_results):
#    print(x)

# Split the data into separate lists for x, y, and z values
x_values = [data[0][0] for data in backtest_results]
y_values = [data[0][1] for data in backtest_results]
z_values = [data[1] for data in backtest_results]

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_values, y_values, z_values)

# Set the axis labels and title
ax.set_xlabel('Parameter 1')
ax.set_ylabel('Parameter 2')
ax.set_zlabel('Backtest Result')
ax.set_title('Backtest Results')

# Display the plot
plt.show()

# # Split the data into separate lists for x, y, and z values
# x_values = [data[0][1] for data in backtest_results]
# y_values = [data[0][2] for data in backtest_results]
# z_values = [data[1] for data in backtest_results]

# # Create the 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x_values, y_values, z_values)

# # Set the axis labels and title
# ax.set_xlabel('Parameter 2')
# ax.set_ylabel('Parameter 3')
# ax.set_zlabel('Backtest Result')
# ax.set_title('Backtest Results')

# # Display the plot
# plt.show()