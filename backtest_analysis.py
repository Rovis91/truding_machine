import pandas as pd
from types import SimpleNamespace
from tabulate import tabulate

def analysis_backtest(dfTest,dt,data):
    d = SimpleNamespace(**data)

    print(tabulate(dt, headers='keys', tablefmt='psql'))

    print("Pair Symbol :",d.pairName,)
    print("Period : [" + str(dfTest.index[0]) + "] -> [" +
        str(dfTest.index[len(dfTest)-1]) + "]")
    print("Starting balance :", d.initalWallet, "$")

    print("\n----- General Informations -----")
    print("Final balance :", round(d.wallet, 2), "$")
    print("Performance vs US Dollar :", round(d.algoPercentage*100, 2), "%")
    print("Buy and Hold Performence :", round(d.holdPercentage*100, 2),
        "% | with Leverage :", round(d.holdPercentage*100, 2)*d.leverage, "%")
    print("Performance vs Buy and Hold :", round(d.vsHoldPercentage, 2), "%")

    print("Best trade : +"+str(d.bestTrade), "%, the ", d.idbest)
    print("Worst trade :", str(d.worstTrade), "%, the ", d.idworst)
    print("Worst drawBack :", str(100*round(dt['drawBack'].min(), 2)), "%")
    print("Total fees : ", round(dt['frais'].sum(), 2), "$")

    print("\n----- Trades Informations -----")
    print("Total trades on period :",d.totalTrades)
    print("Number of positive trades :", d.TotalGoodTrades)
    print("Number of negative trades : ", d.TotalBadTrades)
    print("Trades win rate ratio :", round(d.winRateRatio, 2), '%')
    print("Average trades performance :",d.tradesPerformance,"%")
    print("Average positive trades :", d.AveragePercentagePositivTrades, "%")
    print("Average negative trades :", d.AveragePercentageNegativTrades, "%")

    print("\n----- LONG Trades Informations -----")
    print("Number of LONG trades :",d.TotalLongTrades)
    print("Average LONG trades performance :",d.AverageLongTrades, "%")
    print("Best  LONG trade +"+d.bestLongTrade, "%, the ", d.idBestLong)
    print("Worst LONG trade", d.worstLongTrade, "%, the ", d.idWorstLong)
    print("Number of positive LONG trades :",d.totalGoodLongTrade)
    print("Number of negative LONG trades :",d.totalBadLongTrade)
    print(type(d.totalGoodLongTrade),d.totalGoodLongTrade)
    print(type(d.TotalGoodTrades),d.TotalGoodTrades)
    print("LONG trade win rate ratio :", round(d.totalGoodLongTrade/d.TotalLongTrades*100, 2), '%')

    print("\n----- SHORT Trades Informations -----")
    print("Number of SHORT trades :",d.TotalShortTrades)
    print("Average SHORT trades performance :",d.AverageShortTrades, "%")
    print("Best  SHORT trade +"+d.bestShortTrade, "%, the ", d.idBestShort)
    print("Worst SHORT trade", d.worstShortTrade, "%, the ", d.idWorstShort)
    print("Number of positive SHORT trades :",d.totalGoodShortTrade)
    print("Number of negative SHORT trades :",d.totalBadShortTrade)
    print("SHORT trade win rate ratio :", round(d.totalGoodShortTrade/d.TotalShortTrades*100, 2), '%')

    print("\n----- Trades Reasons -----")
    reasons = dt['reason'].unique()
    for r in reasons:
        print(r+" number :", dt.groupby('reason')['date'].nunique()[r])
    
    #dt[['wallet', 'price']].plot(subplots=True, figsize=(20, 10))
    #print("\n----- Plot -----")
