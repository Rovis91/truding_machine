import pandas as pd
import ta

# -- Generate and clean dataframe --
def dataframe_generator(filepath):
    df=pd.read_json(filepath)
    # Names
    df.columns= ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ]
    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['open'] = pd.to_numeric(df['open'])
   
    # -- Set index -- 
    df = df.set_index('timestamp')
    # df.index = pd.to_datetime(df.index, unit='ms')

    # -- Clean --
    df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)

    print("Data loaded 100%")
    return df

def indicator_gen(df):

    #Simple Moving Average
    df['SMA']= ta.trend.sma_indicator(close=df['close'], window=12)
    df['EMA1']= ta.trend.ema_indicator(close=df['close'], window=7)
    df['EMA2']= ta.trend.ema_indicator(close=df['close'], window=30)
    df['EMA3']= ta.trend.ema_indicator(close=df['close'], window=50)
    df['EMA4']= ta.trend.ema_indicator(close=df['close'], window=100)
    df['EMA5']= ta.trend.ema_indicator(close=df['close'], window=121)
    df['EMA6']= ta.trend.ema_indicator(close=df['close'], window=200)

    #Exponential Moving Average
    # df['EMA1']=ta.trend.ema_indicator(close=df['close'], window=13)
    # df['EMA2']=ta.trend.ema_indicator(close=df['close'], window=38)

    # #Relative Strength Index (RSI)
    #df['RSI'] =ta.momentum.rsi(close=df['close'], window=14)
    df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=14, smooth1=3, smooth2=3)

    # #MACD
    # MACD = ta.trend.MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
    # df['MACD'] = MACD.macd()
    # df['MACD_SIGNAL'] = MACD.macd_signal()
    # df['MACD_DIFF'] = MACD.macd_diff() #Histogramme MACD

    # #Stochastic RSI
    # df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=14, smooth1=3, smooth2=3) #Non moyenné 
    # df['STOCH_RSI_D'] = ta.momentum.stochrsi_d(close=df['close'], window=14, smooth1=3, smooth2=3) #Orange sur TradingView
    # df['STOCH_RSI_K'] =ta.momentum.stochrsi_k(close=df['close'], window=14, smooth1=3, smooth2=3) #Bleu sur TradingView

    # #Ichimoku
    # df['KIJUN'] = ta.trend.ichimoku_base_line(high=df['high'], low=df['low'], window1=9, window2=26)
    # df['TENKAN'] = ta.trend.ichimoku_conversion_line(high=df['high'], low=df['low'], window1=9, window2=26)
    # df['SSA'] = ta.trend.ichimoku_a(high=df['high'], low=df['low'], window1=9, window2=26)
    # df['SSB'] = ta.trend.ichimoku_b(high=df['high'], low=df['low'], window2=26, window3=52)

    # #Bollinger Bands
    # BOL_BAND = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    # df['BOL_H_BAND'] = BOL_BAND.bollinger_hband() #Bande Supérieur
    # df['BOL_L_BAND'] = BOL_BAND.bollinger_lband() #Bande inférieur
    # df['BOL_MAVG_BAND'] = BOL_BAND.bollinger_mavg() #Bande moyenne

    # #Average True Range (ATR)
    # df['ATR'] = ta.volatility.average_true_range(high=df['high'], low=df['low'], close=df['close'], window=14)

    # #Super Trend
    # ST_length = 10
    # ST_multiplier = 3.0
    # superTrend = pda.supertrend(high=df['high'], low=df['low'], close=df['close'], length=ST_length, multiplier=ST_multiplier)
    # df['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)] #Valeur de la super trend
    # df['SUPER_TREND_DIRECTION'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)] #Retourne 1 si vert et -1 si rouge

    # #Awesome Oscillator
    # df['AWESOME_OSCILLATOR'] = ta.momentum.awesome_oscillator(high=df['high'], low=df['low'], window1=5, window2=34)

    # # Kaufman’s Adaptive Moving Average (KAMA)
    # df['KAMA'] = ta.momentum.kama(close=df['close'], window=10, pow1=2, pow2=30)

    # #Choppiness index
    # df['CHOP'] = get_chop(high=df['high'], low=df['low'], close=df['close'], window=14)  
    print("Indicators loaded 100%")
    return df


def indicator_gen_optimizer(df,*enums):
    dfTest['STOCH_RSI'] = ta.momentum.stochrsi(close=dfTest['close'], window=i, smooth1=3, smooth2=3)
    