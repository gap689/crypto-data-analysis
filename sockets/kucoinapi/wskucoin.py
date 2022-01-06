import json
import threading
import time
import traceback

import websocket
import requests

def get_ws_response():
    url = 'https://api.kucoin.com/api/v1/bullet-public'
    response = requests.request('post', url) #, headers=headers
    return response.json()

def get_ws_token():
    token = get_ws_response()['data']['token']
    return token

def get_ws_server():
    server = get_ws_response()['data']['instanceServers'][0]['endpoint']
    return server

#websocket
socket = get_ws_server()
#socket = "wss://push1-v2.kucoin.com/endpoint"

#token
token = get_ws_token()

#connect_id
connect_id = str(int(time.time() * 1000))

ws_endpoint = f"{socket}?token={token}&connectId={connect_id}&acceptUserMessage=true"
print(ws_endpoint)

def on_open(wsapp):
    print('open connection')
    def ping(wsapp):
        while True:
            now = int(time.time() * 1000)
            wsapp.send('{"id":"'+str(now)+'", "type":"ping"}')
            wsapp.send('{"id":"'+str(now)+'", "type": "subscribe", "topic": "/market/ticker:BTC-USDT", "response": "true"}')
            time.sleep(50)

    th = threading.Thread(target=ping, kwargs={"ws": wsapp})
    th.start()
    
#def on_close(wsapp, close_status_code, close_msg):
#    print('closed connection')
#    if close_status_code or close_msg:
#       print("close status code: " + str(close_status_code))
#       print("close message: " + str(close_msg))

def on_message(wsapp, message):
    print('received message')
    print(message)

if __name__ == "__main__":
    websocket.enableTrace(True)
    wsapp = websocket.WebSocketApp(ws_endpoint, on_open=on_open, on_message=on_message)
    #wsapp = websocket.WebSocketApp(ws_endpoint, on_open=on_open, on_close=on_close, on_message=on_message)
    wsapp.run_forever()