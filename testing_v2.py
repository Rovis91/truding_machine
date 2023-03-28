import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from backtest_tool.database_strategy_generator import dataframe_generator
# from data.data_collector import get_historical_data
from os import getcwd
import pandas as pd
from backtest_tool.backtest_analysis import analysis_backtest
from tabulate import tabulate

## Settings
#filepath = "ETHUSDT_1675234800000_1675213200000_5m.json" 
#filepath = "ETHUSDT_1675234800000_1675213200000_1m.json"
#filepath = "ETHUSDT_1677682800000_1677632400000_1m.json" # 25 months
filepath = "ETHUSDT_1677682800000_1677632400000_1m_modified_10p.json" # 25 months modified
strategy_name = 'scalping_v1'


# Open Datas
try:
    data_filepath = getcwd() +"\\Backtest\\data\\" + filepath
except OSError:
    # Not working yet
    print('New database is loading')
    get_historical_data()
    data_filepath = getcwd()  +"\\Backtest\\data\\" + filepath

class Strategie:
    strat = __import__('Strategies.' + strategy_name, fromlist=['*'])
    params=None
    update_rule = "trailling"
    close_condition = False
    takeProfit_rule = False
    def __init__(self,filepath,option=None) :
        self.df = dataframe_generator(filepath)
        self.settings = self.strat.Settings()
        self.get_settings()
        self.lastAth = self.wallet
        self.LAIndex = 0
    def open(self,row):
        if self.strat.openLongCondition(row):
            return 'LONG'
        elif self.strat.openShortCondition(row):
            return 'SHORT'
        else:
            return False
    def close(self,row):
        if self.strat.closeLongCondition(row):
            return "LONG"
        elif self.strat.closeShortCondition(row):
            return "SHORT"
        else:
            return False
    def update(self, row, ongoingTrade, update_rule=False):
        match update_rule:
            case "trailling":
                new_SL=self.get_stopLoss(row['close'])
                if new_SL > ongoingTrade["stopLoss"]:
                    ongoingTrade["stopLoss"]=new_SL
                    print("SL updated")
                return ongoingTrade
            case _:
                return ongoingTrade
    def get_fee(self,dt, current_date):
        volume=volume_30days(dt, current_date)
        if volume < 100000:
            self.fee = (0,0)
        elif volume < 1000000:
            self.fee = (0.0002,0.0005)
        elif volume < 5000000:
            self.fee = (0.00015,0.00040)
        elif volume < 10000000:
            self.fee = (0.00010,0.00035)
        elif volume < 50000000:
            return(0.00005,0.00030)
        elif volume < 200000000:
            self.fee = (0,0.00025)
        elif volume > 200000000:
            self.fee = (0,0.0002)
        else:
            return "Error"  
    def get_settings(self):
        self.leverage = self.settings.leverage()
        self.wallet = self.settings.wallet()
        self.stopLoss = self.settings.stopLoss()
        self.takeProfit = self.settings.takeProfit()
        self.rule = self.settings.rule()
        self.close_condition = self.settings.close_condition()
    def get_df(self):
        return self.strat.ndf_gen(self.df,self.params)
    def optimization_settings(self):
        self.params = self.strat.combinations()
    def get_stopLoss(self,price):
        return price*(1-self.stopLoss)
    def get_takeProfit(self,price):
        return price*(1+self.takeProfit)
    def LAIndex_set(self, index):
        self.LAIndex = index

def open_trade(dt,trade_type,index,row,strat):
    print("Opening trade")
    closePrice = row['close']
    wallet = strat.wallet * (1-strat.fee[0]) 
    position = closePrice* strat.leverage
    trade_fee = strat.fee[0] * strat.wallet *  strat.leverage
    takeProfit = strat.get_takeProfit(closePrice)
    stopLoss = strat.get_stopLoss(closePrice)
    periods=index-strat.LAIndex / 300000
    strat.LAIndex_set(index)
    ongoingTrade = {'date': index, 'trade_type': trade_type, 'position': position , 'price': closePrice,
            'fee': trade_fee , 'wallet': wallet, 'var': None, 'periods': periods, 'takeProfit': takeProfit , 'stopLoss': stopLoss}
    ser = pd.Series(data=ongoingTrade, index=['date', 'trade_type','position','price', 'fee', 'wallet', 'var','periods'])
    dt = pd.concat([dt, ser.to_frame().T], ignore_index=True)
    return ongoingTrade,dt

def close_trade(dt,close_type,index,row,strat):
    print("Closing trade")
    closePrice = row['close']
    closePriceWithFee = row['close'] * (1-strat.fee[1])
    strat.wallet = closePriceWithFee
    position = closePrice* strat.leverage
    trade_fee = strat.fee[1] * closePrice *  strat.leverage 
    periods=index-strat.LAIndex / 300000
    strat.LAIndex_set(index)
    closed_trade = {'date': index, 'trade_type': close_type, 'position': position, 'price': closePrice,
            'fee': trade_fee , 'wallet': closePriceWithFee, 'var': round((closePriceWithFee-strat.lastAth)/strat.lastAth*100,2), 'periods': periods}
    ser = pd.Series(data=closed_trade, index=['date', 'trade_type','position','price', 'fee', 'wallet', 'var','periods'])
    dt = pd.concat([dt, ser.to_frame().T], ignore_index=True)
    strat.lastAth=max(strat.lastAth,closePriceWithFee)
    return dt

def volume_30days(dt, current_date):
    if len(dt.index) > 2:
        df_volume = dt.drop(dt[(dt['date'] < current_date) | (dt['date'] > current_date - 2592000000)].index)
        total_volume =  df_volume.loc[df_volume['trade_type'] != 'close', 'position'].sum()
        return total_volume
    else:
        return 0


def backtest(data_filepath,option):
    # -- Load strategie --
    strat = Strategie(data_filepath, option)
    strat.get_settings()
    df = strat.get_df()
    dt = pd.DataFrame(columns=['date', 'trade_type','position','price', 'fee', 'wallet', 'var','periods'])
    # -- Load optimization settings if requiered --
    ongoingTrade=False
    strat.LAIndex_set(df.index[0])
    for index, row in df.iterrows():
        # -- Update fees --
        strat.get_fee(dt,index)
        # -- Pass the first lineswithout indicators
        if row.isnull().values.any():
            continue     
        # -- If there is no order in progress --
        if ongoingTrade == False:
            # Open Position
            if strat.open(row) == "LONG":
                ongoingTrade,dt = open_trade(dt,"LONG",index,row,strat)
            elif strat.open(row) == "SHORT":
                ongoingTrade,dt = open_trade(dt,"SHORT",index,row,strat)
            else:
                # print("No possible trade")
                pass
        # -- If there is an order in progress --
        else:
            # Condition Close
            if ongoingTrade["trade_type"] == strat.close(row):
                dt = close_trade(dt,"CD",index,row,strat) 
                ongoingTrade = False
            # Automatic close
            if ongoingTrade["trade_type"] == "LONG":
                # StopLoss
                if row['low'] <= ongoingTrade["stopLoss"]:
                    dt = close_trade(dt,"SL",index,row,strat)
                    ongoingTrade = False
                # Liquidation 
                elif strat.leverage*(ongoingTrade["price"]-row["low"]) > ongoingTrade["wallet"]:
                    print("\n Position liquidated \n")
                    break
                # Take profit 
                elif (strat.takeProfit_rule == True) and (row['high'] >= ongoingTrade["takeProfit"]):
                    dt = close_trade(dt,"TP",index,row,strat) 
                    ongoingTrade = False
                else:
                    pass    
            else: #SHORT
                # StopLoss
                if row['high'] >= strat.stopLoss:
                    dt = close_trade(dt,"SL",index,row,strat)
                    ongoingTrade = False
                # Liquidation 
                elif strat.leverage*(row["high"]-dt["price"]) > ongoingTrade["wallet"]:
                    print("\n Position liquidated \n")
                    break
                # Take profit 
                elif (strat.takeProfit_rule == True) and row['low'] <= strat.takeProfit:
                    dt = close_trade(dt,"TP",index,row,strat)
                    ongoingTrade = False
                else:
                    pass
            # -- If trade still open --
            if (strat.update_rule != False and ongoingTrade != False):
                ongoingTrade = strat.update(row, ongoingTrade, strat.update_rule) 

        # -- Close last trade if still open
    if ongoingTrade != False:
        index = df.iloc[-1].name
        row = df.iloc[-1]
        dt = close_trade(dt,"LT",index,row,strat)
        ongoingTrade = False
    return dt        

dt=backtest(data_filepath, None) 
analysis_backtest(dt)
