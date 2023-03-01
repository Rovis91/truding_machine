import pandas as pd
from os import getcwd
from backtest_tool.database_strategy_generator import *

data_filepath = "ETHUSDT_1644595200000_1643072400000_1h.json" # 1 month
filepath = getcwd() + "\\data\\" + data_filepath


# Generate dataframe
df = dataframe_generator(filepath)
df['var_low']=((df['close']-df['low'])/df['close'])*100
df['var_high']=((df['high']-df['close'])/df['close'])*100
df['var_max']=df[['var_high','var_low']].max(axis=1)
print(df)
# calculate absolute percentage variation between close prices
close_variation = (df['close'].pct_change() * 100).abs()

# calculate average and median variation
avg_variation = close_variation.mean()
med_variation = close_variation.median()

var_max = pd.Series(df.var_max)
avg_variation_max = var_max.mean()
med_variation_max = var_max.median()


print(f"Close price - Average variation: {avg_variation:.2f}%, Median variation: {med_variation:.2f}%")
print(f"Close price - Average variation: {avg_variation_max:.2f}%, Median variation: {med_variation_max:.2f}%")
