import pandas as pd
# -- Condition to open Market LONG --
def openLongCondition(row, previousRow):
    if (row['EMA1'] < row['EMA6'] 
    and row['STOCH_RSI'] < 0.82):
        return True
    else:
        return False

# -- Condition to close Market LONG --
def closeLongCondition(row, previousRow,takeProfit):
    if (row['EMA6'] < row['EMA1']) or row['close']>=(1+takeProfit)*previousRow['close']:
        return True
    else:
        return False
    
# -- Condition to open Market SHORT --
def openShortCondition(row, previousRow):
    if ( row['EMA6'] < row['EMA1'] 
    and row['STOCH_RSI'] > 0.2 ):
        return True
    else:
        return False

# -- Condition to close Market SHORT --
def closeShortCondition(row, previousRow,takeProfit):
    if (row['EMA1'] < row['EMA6']) or row['close']>=(1-takeProfit)*previousRow['close'] :
        return True
    else:
        return False