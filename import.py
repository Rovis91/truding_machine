from binance import Client
import requests
import json
import time
import os

client = Client("jt1nQiuAp9EM7DoaQlbLo0rFC6kBtr8FW0r89C7qWH6KUcgb7NmKbrzqEjlpbSoP","jCPkDfwkyfu3PtnqLteQKFhydHuSiVYvX9K3IrBYQzIqE6lRuaXunP1BY90LFuGe")
symbol='ETHUSDT'
start_time=1640995200000
end_time=1643072400000  
interval="1h"

def get_historical_data(client=client,symbol='ETHUSDT', start_time=1640995200000, end_time=None, interval='1h'):
    limit = 500

    def string_to_ms(interval):
        units = {"s": 1000, "m": 60 * 1000, "h": 60 * 60 * 1000, "d": 24 * 60 * 60 * 1000}
        number = int(interval[:-1])
        unit = interval[-1:]
        return number * units[unit]

    diff = string_to_ms(interval)*limit
    all_data = []
    if end_time == None:
        end_time=time.time()*1000

    while True:
        end_time_request = start_time + diff
        if end_time_request > end_time:
            end_time_request=end_time
        
        response = client.futures_historical_klines(symbol, interval, start_time, end_time_request)
        data = json.dumps(response)
        all_data.extend(response)
        
        start_time = start_time + diff
        if start_time > end_time:
            break
        time.sleep(10)

    # Store the data in a JSON file
    current_path = os.getcwd() + "\\data"
    if not os.path.exists(current_path):
        os.makedirs(current_path)
    filepath = current_path + "\\" + symbol + '_' + str(start_time) + '_' + str(end_time) + '_' + interval + '.json'
    print(filepath)
    with open(filepath, 'w') as file:
        json.dump(all_data, file)

# Call the function to import historical data
get_historical_data(client, symbol, start_time, end_time, interval )





