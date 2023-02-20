import pandas as pd
from types import SimpleNamespace 
from strategie import *

def backtest(dfTest, trade_set):


    # Dataframe to store trades
    dt = pd.DataFrame(columns=['tradenumber','date', 'position', 'reason',
                            'price', 'frais', 'wallet', 'drawBack'])
    dt = dt.set_index('tradenumber')

    
    # Import settings for trades
    t_set = SimpleNamespace(**trade_set)
    
    
    previousRow = dfTest.iloc[0]
    orderInProgress = ''
    

    # Export datas from dict
    wallet = t_set.initialwallet
    takerFee = t_set.takerFee
    leverage = t_set.leverage
    takeProfit = t_set.takeProfit
    initalWallet = wallet
    lastAth = wallet
    
    
    
    # -- Iteration on all your price dataset (df) --
    for index, row in dfTest.iterrows():

        # -- If there is an order in progress --
        if orderInProgress != '':
            # -- Check if there is a LONG order in progress --
            if orderInProgress == 'LONG':
                # -- Check Liquidation --
                if row['low'] < longLiquidationPrice:
                    print('/!\ YOUR LONG HAVE BEEN LIQUIDATED the',index)
                    break
                
                # -- Check Stop Loss --
                elif row['low'] < stopLoss:
                    orderInProgress = ''
                    closePrice = stopLoss
                    closePriceWithFee = closePrice -  takerFee * closePrice
                    pr_change = (closePriceWithFee - longIniPrice) / longIniPrice
                    wallet = wallet + wallet*pr_change* leverage

                
                    # -- Check if your wallet hit a new ATH to know the drawBack --
                    if wallet > lastAth:
                        lastAth = wallet
                    
                    # -- Add the trade to DT to analyse it later --
                    myrow = {'date': index, 'position': "LONG", 'reason': 'Stop Loss Long', 'price': closePrice,
                            'frais':  takerFee * wallet *  leverage, 'wallet': wallet, 'drawBack': (wallet-lastAth)/lastAth}
                    previousRow=row
                    dt = dt.append(myrow, ignore_index=True)
                # -- Check If you have to close the LONG --
                elif closeLongCondition(row, previousRow,takeProfit) == True:
                    orderInProgress = ''
                    closePrice = row['close']
                    closePriceWithFee = row['close'] -  takerFee * row['close']
                    pr_change = (closePriceWithFee - longIniPrice) / longIniPrice
                    wallet = wallet + wallet*pr_change* leverage

                
                    # -- Check if your wallet hit a new ATH to know the drawBack --
                    if wallet > lastAth:
                        lastAth = wallet
                    
                    # -- Add the trade to DT to analyse it later --
                    myrow = {'date': index, 'position': "LONG", 'reason': 'Close Long Market', 'price': closePrice,
                            'frais':  takerFee * wallet *  leverage, 'wallet': wallet, 'drawBack': (wallet-lastAth)/lastAth}
                    previousRow=row
                    dt = dt.append(myrow, ignore_index=True)


            # -- Check if there is a SHORT order in progress --
            elif orderInProgress == 'SHORT':
                # -- Check Liquidation --
                if row['high'] > shortLiquidationPrice:
                    print('/!\ YOUR SHORT HAVE BEEN LIQUIDATED the',index)
                    break
                # -- Check stop loss --
                elif row['high'] > stopLoss:
                    orderInProgress = ''
                    closePrice = stopLoss
                    closePriceWithFee = closePrice +  takerFee * closePrice
                    pr_change = -(closePriceWithFee - shortIniPrice) / shortIniPrice
                    wallet = wallet + wallet*pr_change* leverage

                  
                    # -- Check if your wallet hit a new ATH to know the drawBack --
                    if wallet > lastAth:
                        lastAth = wallet

                    # -- Add the trade to DT to analyse it later --
                    myrow = {'date': index, 'position': "SHORT", 'reason': 'Stop Loss Short', 'price': closePrice,
                            'frais':  takerFee * wallet *  leverage, 'wallet': wallet, 'drawBack': (wallet-lastAth)/lastAth}
                    previousRow=row
                    dt = dt.append(myrow, ignore_index=True)
                # -- Check If you have to close the SHORT --
                elif closeShortCondition(row, previousRow,takeProfit) == True:
                    orderInProgress = ''
                    closePrice = row['close']
                    closePriceWithFee = row['close'] +  takerFee * row['close']
                    pr_change = -(closePriceWithFee - shortIniPrice) / shortIniPrice
                    wallet = wallet + wallet*pr_change* leverage


                    # -- Check if your wallet hit a new ATH to know the drawBack --
                    if wallet > lastAth:
                        lastAth = wallet

                    # -- Add the trade to DT to analyse it later --
                    myrow = {'date': index, 'position': "SHORT", 'reason': 'Close Short Market', 'price': closePrice,
                            'frais':  takerFee * wallet *  leverage, 'wallet': wallet, 'drawBack': (wallet-lastAth)/lastAth}
                    previousRow=row
                    dt = dt.append(myrow, ignore_index=True)
        # -- If there is NO order in progress --
        if orderInProgress == '':
            # -- Check If you have to open a LONG --
            if openLongCondition(row, previousRow) == True:
                orderInProgress = 'LONG'
                closePrice = row['close']
                longIniPrice = row['close'] +  takerFee * row['close']
                tokenAmount = (wallet *  leverage) / row['close']
                longLiquidationPrice = longIniPrice - (wallet/tokenAmount)
                stopLoss = closePrice - t_set.SL_ratio * closePrice
                
                # -- Add the trade to DT to analyse it later --
                myrow = {'date': index, 'position': "Open Long", 'reason': 'Open Long Market', 'price': closePrice,
                        'frais':  takerFee * wallet *  leverage, 'wallet': wallet, 'drawBack': (wallet-lastAth)/lastAth}
                previousRow=row
                dt = dt.append(myrow, ignore_index=True)
            
            # -- Check If you have to open a SHORT --
            if openShortCondition(row, previousRow) == True:
                orderInProgress = 'SHORT'
                closePrice = row['close']
                shortIniPrice = row['close'] -  takerFee * row['close']
                tokenAmount = (wallet *  leverage) / row['close']
                shortLiquidationPrice = shortIniPrice + (wallet/tokenAmount)
                stopLoss = closePrice + t_set.SL_ratio * closePrice
              
                # -- Add the trade to DT to analyse it later --
                myrow = {'date': index, 'position': "Open Short", 'reason': 'Open Short Market', 'price': closePrice,
                        'frais':  takerFee * wallet *  leverage, 'wallet': wallet, 'drawBack': (wallet-lastAth)/lastAth}
                previousRow=row
                dt = dt.append(myrow, ignore_index=True)
        
    # -- BackTest Analyses --
    dt['resultat%'] = dt['wallet'].pct_change()*100

    dt['tradeIs'] = ''
    dt.loc[dt['resultat%'] > 0, 'tradeIs'] = 'Good'
    dt.loc[dt['resultat%'] < 0, 'tradeIs'] = 'Bad'

    iniClose = dfTest.iloc[0]['close']
    lastClose = dfTest.iloc[len(dfTest)-1]['close']
    holdPercentage = ((lastClose - iniClose)/iniClose)
    holdWallet = holdPercentage *  leverage * initalWallet
    algoPercentage = ((wallet - initalWallet)/initalWallet)
    vsHoldPercentage = ((wallet - holdWallet)/holdWallet) * 100

    try:
        tradesPerformance = round(dt.loc[(dt['tradeIs'] == 'Good') | (dt['tradeIs'] == 'Bad'), 'resultat%'].sum()
                / dt.loc[(dt['tradeIs'] == 'Good') | (dt['tradeIs'] == 'Bad'), 'resultat%'].count(), 2)
    except:
        tradesPerformance = 0
        print("/!\ There is no Good or Bad Trades in your BackTest, maybe a problem...")

    try:
        TotalGoodTrades = dt.groupby('tradeIs')['date'].nunique()['Good']
        AveragePercentagePositivTrades = round(dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].sum()
                                            / dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].count(), 2)
        idbest = dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].idxmax()
        bestTrade = str(
            round(dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].max(), 2))
    except:
        TotalGoodTrades = 0
        AveragePercentagePositivTrades = 0
        idbest = ''
        bestTrade = 0
        print("/!\ There is no Good Trades in your BackTest, maybe a problem...")
    try:
        TotalBadTrades = dt.groupby('tradeIs')['date'].nunique()['Bad']
        AveragePercentageNegativTrades = round(dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].sum()
                                            / dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].count(), 2)
        idworst = dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].idxmin()
        worstTrade = round(dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].min(), 2)
    except:
        TotalBadTrades = 0
        AveragePercentageNegativTrades = 0
        idworst = ''
        worstTrade = 0
        print("/!\ There is no Bad Trades in your BackTest, maybe a problem...")

    totalTrades = TotalBadTrades + TotalGoodTrades

    try:
        TotalLongTrades = dt.groupby('position')['date'].nunique()['LONG']
        AverageLongTrades = round(dt.loc[dt['position'] == 'LONG', 'resultat%'].sum()
                                / dt.loc[dt['position'] == 'LONG', 'resultat%'].count(), 2)
        idBestLong = dt.loc[dt['position'] == 'LONG', 'resultat%'].idxmax()
        bestLongTrade = str(
            round(dt.loc[dt['position'] == 'LONG', 'resultat%'].max(), 2))
        idWorstLong = dt.loc[dt['position'] == 'LONG', 'resultat%'].idxmin()
        worstLongTrade = str(
            round(dt.loc[dt['position'] == 'LONG', 'resultat%'].min(), 2))
    except:
        AverageLongTrades = 0
        TotalLongTrades = 0
        bestLongTrade = ''
        idBestLong = ''
        idWorstLong = ''
        worstLongTrade = ''
        print("/!\ There is no LONG Trades in your BackTest, maybe a problem...")
    try:
        TotalShortTrades = dt.groupby('position')['date'].nunique()['SHORT']
        AverageShortTrades = round(dt.loc[dt['position'] == 'SHORT', 'resultat%'].sum()
                                / dt.loc[dt['position'] == 'SHORT', 'resultat%'].count(), 2)
        idBestShort = dt.loc[dt['position'] == 'SHORT', 'resultat%'].idxmax()
        bestShortTrade = str(
            round(dt.loc[dt['position'] == 'SHORT', 'resultat%'].max(), 2))
        idWorstShort = dt.loc[dt['position'] == 'SHORT', 'resultat%'].idxmin()
        worstShortTrade = str(
            round(dt.loc[dt['position'] == 'SHORT', 'resultat%'].min(), 2))
    except:
        AverageShortTrades = 0
        TotalShortTrades = 0
        bestShortTrade = ''
        idBestShort = ''
        idWorstShort = ''
        worstShortTrade = ''
        print("/!\ There is no SHORT Trades in your BackTest, maybe a problem...")

    try:
        totalGoodLongTrade = dt.groupby(['position', 'tradeIs']).size()['LONG']['Good']
    except:
        totalGoodLongTrade = 0
        print("/!\ There is no good LONG Trades in your BackTest, maybe a problem...")

    try:
        totalBadLongTrade = dt.groupby(['position', 'tradeIs']).size()['LONG']['Bad']
    except:
        totalBadLongTrade = 0
        print("/!\ There is no bad LONG Trades in your BackTest, maybe a problem...")

    try:
        totalGoodShortTrade = dt.groupby(['position', 'tradeIs']).size()['SHORT']['Good']
    except:
        totalGoodShortTrade = 0
        print("/!\ There is no good SHORT Trades in your BackTest, maybe a problem...")
    try:
        totalBadShortTrade = dt.groupby(['position', 'tradeIs']).size()['SHORT']['Bad']
    except:
        totalBadShortTrade = 0
        print("/!\ There is no bad SHORT Trades in your BackTest, maybe a problem...")

    TotalTrades = TotalGoodTrades + TotalBadTrades
    winRateRatio = (TotalGoodTrades/TotalTrades) * 100

    reasons = dt['reason'].unique()

    print("BackTest finished, final wallet :",wallet,"$")
    
    trade_data={"wallet": wallet,

                "totalTrades" : totalTrades,
                "TotalGoodTrades" : TotalGoodTrades,
                "TotalBadTrades" : TotalBadTrades,

                "totalGoodLongTrade" : totalGoodLongTrade,
                "totalBadLongTrade" : totalBadLongTrade,
                "AverageLongTrades" : AverageLongTrades,
                "TotalLongTrades" :  TotalLongTrades, 
                "bestLongTrade" : bestLongTrade,
                "idBestLong" : idBestLong ,
                "idWorstLong" : idWorstLong,
                "worstLongTrade" : worstLongTrade,

                "totalGoodShortTrade" : totalGoodShortTrade,
                "totalBadShortTrade" : totalBadShortTrade,
                "AverageShortTrades" : AverageShortTrades,
                "TotalShortTrades" :  TotalShortTrades, 
                "bestShortTrade" : bestShortTrade,
                "idBestShort" : idBestShort ,
                "idWorstShort" : idWorstShort,
                "worstShortTrade" : worstShortTrade,

                "AveragePercentagePositivTrades" : AveragePercentagePositivTrades,
                "idbest" : idbest,
                "bestTrade" : bestTrade,
                "AveragePercentageNegativTrades" : AveragePercentageNegativTrades,
                "idworst" : idworst,
                "worstTrade" : worstTrade,

                "iniClose" : iniClose,
                "lastClose" : lastClose,

                "holdPercentage" : holdPercentage,
                "holdWallet" : holdWallet,
                "algoPercentage" : algoPercentage,
                "vsHoldPercentage" : vsHoldPercentage,
                "initalWallet" : initalWallet,
                "lastAth" : lastAth,

                
                "winRateRatio" : winRateRatio,
                "tradesPerformance" : tradesPerformance

             }
    data = {**trade_set, **trade_data}
    
    return(dt,data)