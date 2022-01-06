import websocket
import pandas as pd
import json
#import pudb

SOCKET = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"

df = pd.DataFrame()

def on_open(ws):
    print("opened connection")

def on_close(ws):
    print("closed connection")

def on_message(ws, message):
    print("received message")
    global df

    # convert str to dict
    data = json.loads(message)
    data = data["k"]
    data = {indx:[val] for indx,val in data.items()}

    # convert dict to dataframe
    data = pd.DataFrame.from_dict(data)

    # concatenate df with data.
    df = pd.concat([df,data])
    print(df.head())


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()