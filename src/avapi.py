import os
import requests
import collections

def get_stock_market_info(symbol):
    url = "https://www.alphavantage.co/query"
    qs = "?function=TIME_SERIES_DAILY&outputsize=compact"
    qs += "&symbol=" + symbol
    qs += "&apikey=" + os.getenv("ALPHA_VANTAGE_API_KEY")
    r = requests.get(url + qs)
    objJSON = r.json()
    last_closings = get_last_closings(objJSON, 2)
    data = collections.OrderedDict()
    data["Meta Data"] = objJSON["Meta Data"]
    data["Last Closings"] = last_closings
    data["Results"] = get_results(last_closings)
    return data

def get_last_closings(dict, quantity):
    arr = []
    counter = 0
    for key in dict["Time Series (Daily)"]:
        element = collections.OrderedDict()
        #dt_string = key
        # ET > Eastern Time > UTC-5:00/-4:00
        #format = "%Y-%m-%d"
        #element["date"] = datetime.datetime.strptime(dt_string, format)
        element["date"] = key
        element["open"] = float(dict["Time Series (Daily)"][key]["1. open"])
        element["high"] = float(dict["Time Series (Daily)"][key]["2. high"])
        element["low"] = float(dict["Time Series (Daily)"][key]["3. low"])
        element["close"] = float(dict["Time Series (Daily)"][key]["4. close"])
        #element["volume"] = int(dict["Time Series (Daily)"][key]["5. volume"])
        if counter < quantity:
            arr.append(element)
            counter += 1
        else:
            break
    return arr

def get_results(last_closings):
    data = collections.OrderedDict()
    data["open"] = last_closings[0]["open"]
    data["high"] = last_closings[0]["high"]
    data["low"] = last_closings[0]["low"]
    #data["variation"] = last_closings[0]["close"] - last_closings[1]["close"]
    data["variation"] = round(last_closings[0]["close"] - last_closings[1]["close"], 3)
    return data

if __name__ == '__main__':
    get_last_closings(dict, 2)