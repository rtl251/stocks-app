import csv
from dotenv import load_dotenv
import json
import os
import pdb
import requests
import datetime
now = datetime.datetime.now()
from datetime import datetime



def parse_response(response_text):
    #function, job is to accept reponse text string and convert it to dictionary, accepts a parameter called response text
    # response_text can be either a raw JSON string or an already-converted dictionary
    if isinstance(response_text, str): # if not yet converted, then:
        response_text = json.loads(response_text) # convert string to dictionary (converting to a list of dictionaries)

    results = []
    time_series_daily = response_text["Weekly Time Series"]
    #time_series_daily = response_text["Time Series (Daily)"] #> a nested dictionary
    for trading_date in time_series_daily: # FYI: can loop through a dictionary's top-level keys/attributes
        prices = time_series_daily[trading_date] #> {'1. open': '101.0924', '2. high': '101.9500', '3. low': '100.5400', '4. close': '101.6300', '5. volume': '22165128'}
        result = {
            "date": trading_date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        }
        results.append(result)
    return results

def write_prices_to_file(prices=[], filename="db/prices.csv"):
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for d in prices:
            row = {
                "timestamp": d["date"], # change attribute name to match project requirements
                "open": d["open"],
                "high": d["high"],
                "low": d["low"],
                "close": d["close"],
                "volume": d["volume"]
            }
            writer.writerow(row)

if __name__ == '__main__': # only execute if file invoked from the command-line, not when imported into other files, like tests

    load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") or "O4EFFBTE7FU54HHU"
    #ALPHAVANTAGE_API_KEY
    # CAPTURE USER INPUTS (SYMBOL)

    symbol =input("Please input a stock symbol:")
        # VALIDATE SYMBOL AND PREVENT UNECESSARY REQUESTS
    if 1 > len(symbol) or len(symbol) > 5:
        print("INCORRECT AMOUNT OF CHARACTERS, ENTER A SYMBOL BETWEEN 1 AND 5 CHARACTERS:")
        quit("Stopping the program")
    else:
        pass
        try:
            float(symbol)
            print("CHECK YOUR SYMBOL, EXPECTING A NON-NUMERIC SYMBOL")
            quit("Stopping the program")
        except ValueError as e:
            pass



    # ASSEMBLE REQUEST URL
    # ... see: https://www.alphavantage.co/support/#api-key
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={api_key}"
    #request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    # ISSUE "GET" REQUEST
    response = requests.get(request_url)
        # VALIDATE RESPONSE AND HANDLE ERRORS
        # ... todo
    if "Error Message" in response.text:
        print("REQUEST ERROR, PLEASE TRY AGAIN. CHECK YOUR STOCK SYMBOL.")
        quit("Stopping the program")

    # PARSE RESPONSE (AS LONG AS THERE ARE NO ERRORS)
    daily_prices = parse_response(response.text)
    # WRITE TO CSV
    write_prices_to_file(prices=daily_prices, filename="db/prices.csv")



    # PERFORM CALCULATIONS
    # Latest Closing Price
    print("")
    # ... todo (HINT: use the daily_prices variable, and don't worry about the CSV file anymore :-)
    latest_closing_price = daily_prices[0]["close"]
    latest_closing_price = float(latest_closing_price)
    latest_closing_price_usd = "${0:,.2f}".format(latest_closing_price)

    #Last Date of Data
    last_day = str((daily_prices[0]["date"]))
    last_day_format =datetime.strptime(last_day, '%Y-%m-%d')
    last_day_final = last_day_format.strftime("%A %B %d, %Y")

#Generate 52 Week High
    highlist=[]
    hundred_daily_prices = daily_prices[0:52]
    for h in hundred_daily_prices:
        highlist.append(float(h["high"]))
    highmax= max(highlist)
    highmax = float(highmax)
    highmax_usd = "${0:,.2f}".format(highmax)

#Generate 52 Week Low
    lowlist=[]
    hundred_daily_prices = daily_prices[0:52]
    for l in hundred_daily_prices:
        lowlist.append(float(l["low"]))
    lowmin = min(lowlist)
    lowmin = float(lowmin)
    lowmin_usd = "${0:,.2f}".format(lowmin)

#Generate 10Year Moving Average
    movingavglist=[]
    hundred_daily_prices = daily_prices[0:52]
    for m in hundred_daily_prices:
        movingavglist.append(float(l["close"]))
    movingavg  = sum(movingavglist) / len(movingavglist)
    movingavg_usd = "${0:,.2f}".format(movingavg)



# DAILY

    #highlist=[]
    #hundred_daily_prices = daily_prices[0:100]
    #for h in hundred_daily_prices:
    #    highlist.append(float(h["high"]))
    #highmax= max(highlist)
    #highmax = float(highmax)
    #highmax_usd = "${0:,.2f}".format(highmax)


    #lowlist=[]
    #hundred_daily_prices = daily_prices[0:100]
    #for l in hundred_daily_prices:
    #    lowlist.append(float(l["low"]))
    #lowmin = min(lowlist)
    #lowmin = float(lowmin)
    #lowmin_usd = "${0:,.2f}".format(lowmin)

    #movingavglist=[]
    #hundred_daily_prices = daily_prices[0:100]
    #for m in hundred_daily_prices:
    #    movingavglist.append(float(l["close"]))
    #movingavg  = sum(movingavglist) / len(movingavglist)
    #movingavg_usd = "${0:,.2f}".format(movingavg)



#The selected stock symbol(s) (e.g. "Stock: MSFT")
print("Stock Symbol: " + symbol.upper())
#The date and time when the program was executed, formatted in a human-friendly way (e.g. "Run at: 11:52pm on June 5th, 2018")
print(now.strftime("Program run on: %A %B %d, %Y" + " at " + "%I:%M%p"))
#The date when the data was last refreshed, usually the same as the latest available day of daily trading data (e.g. "Latest Data from: June 4th, 2018")
print("Latest Data from: " + last_day_final)
#For each stock symbol: its latest closing price, its recent average high price, and its recent average low price, calculated according to the instructions below,
# and formatted as currency with a dollar sign and two decimal places with a thousands separator as applicable (e.g. "Recent Average High: $1,234.56", etc.)
print("Latest Closing Price: " + latest_closing_price_usd)
print("")
print("52-Week High: " + highmax_usd)
print("")
print("52-Week Low: " + lowmin_usd)
print("")
    # PRODUCE FINAL RECOMMENDATION
if latest_closing_price/movingavg > 1.1:
    print("RECOMMENDATION: SELL")
elif latest_closing_price/movingavg < .9:
        print("RECOMMENDATION: BUY")
else:
    print("RECOMMENDATION: HOLD")

#Explanation
print("")
print("EXPLANATION: Our patent-pending stock-picking algorithm figures out if the latest closing stock price is above or below the 1-year moving average by 10%. ")
print("If the latest closing price is lower than the 1-year moving average by more than 10%, we recommend that you buy the stock!")
print("If the latest closing price is higher than the 1-year moving average by more than 10%, we recommend that you sell the stock!")
print("If the latest closing price is within |10%| of the the 1-year moving average, we recommend that you hold the stock.")
print("")
print("In this case, the latest closing price was " + latest_closing_price_usd)
print("In this case, the 1-year moving average was " + movingavg_usd)
print("Latest closing price / 1-year moving average = " + str(latest_closing_price/movingavg))

#Daily Explanation
#print("")
#print("EXPLANATION: Our patent-pending stock-picking algorithm figures out if the latest closing stock price is above or below the 100-day moving average by 10%. ")
#print("If the latest closing price is lower than the 100-day moving average by more than 10%, we recommend that you buy the stock!")
#print("If the latest closing price is higher than the 100-day moving average by more than 10%, we recommend that you sell the stock!")
#print("If the latest closing price is within |10%| of the the 100-day moving average,we recommend that you hold the stock.")
#print("")
#print("In this case, the latest closing price was " + latest_closing_price_usd)
#print("In this case, the 100-day moving average was " + movingavg_usd)
#print("Latest closing price / 100-day moving average = " + str(latest_closing_price/movingavg))
