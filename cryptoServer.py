from grove_rgb_lcd import *
import os
import time
from flask import Flask
from flask import jsonify
from flask import request
import json
import requests
import socket
import urllib.request
import argparse
import json
import pickle

currency = ""
portPickle = 'port.pickle'
app = Flask('Crypto Server')

@app.route('/crypto', methods=['GET'])
def crypto_connect():
    password = request.args.get('password')
    if password == cryptoPassword:
        response = jsonify({'Response': 'Password accepted'})
    else:
        response = jsonify({'Response': 'Password incorrect'})
    return response
    
@app.route('/crypto/check', methods=['GET'])
def crypto_check():
    password = request.args.get('password')
    if password == cryptoPassword:
        try:
            with open(portPickle, 'rb') as f:
                state = pickle.load(f)
                port = state[0]
                mode = state[1]
                coins = port[0]
                coinQ = port[1]
        except FileNotFoundError:
                coins = []
                coinQ = []
                mode = ["0",""]
                port = [coins, coinQ]
                state = [port, mode]
                pass
        portSum = ""
        for i in range(len(coins)):
            portSum = portSum + coins[i] + ": " + str(coinQ[i]) + " = $" + str(float(coinQ[i]) * priceCheck(coins[i])) + ", " 
        portSum = portSum + "Total: $" + str(portUpdate(coins, coinQ))
        response = jsonify({'Response': portSum})
    else:
        response = jsonify({'Response': 'Error: Incorrect Password'})
    return response

@app.route('/crypto/mode', methods=['GET'])
def crypto_mode():
    password = request.args.get('password')
    if password == cryptoPassword:
        try:
            with open(portPickle, 'rb') as f:
                state = pickle.load(f)
                port = state[0]
                mode = state[1]
                coins = port[0]
                coinQ = port[1]
        except FileNotFoundError:
                coins = []
                coinQ = []
                mode = ["0",""]
                port = [coins, coinQ]
                state = [port, mode]
                pass
        mode[0] = request.args.get('mode')
        mode[1] = request.args.get('currency')
        state[1] = mode 
        with open(portPickle, 'wb') as f:
            pickle.dump(state, f)
        response = jsonify({'Response': 'Configured'})
    else:
        response = jsonify({'Response': 'Error: Incorrect password'})
    return response
        
@app.route('/crypto/reset', methods=['GET'])
def crypto_reset():
    password = request.args.get('password')
    if password == cryptoPassword:
        if os.path.exists('port.pickle'):
            os.remove('port.pickle')
        response = jsonify({'Response': 'Portfolio reset'})
    else:
        response = jsonify({'Response': 'Error: Incorrect password'})
    return response
        
@app.route('/crypto/edit', methods=['GET'])
def crypto_edit():
    password = request.args.get('password')
    if password == cryptoPassword:
        try:
            with open(portPickle, 'rb') as f:
                state = pickle.load(f)
                port = state[0]
                mode = state[1]
                coins = port[0]
                coinQ = port[1]
        except FileNotFoundError:
                coins = []
                coinQ = []
                mode = ["0",""]
                port = [coins, coinQ]
                state = [port, mode]
                pass
        coin = request.args.get('coin')
        quantity = request.args.get('quantity')
        if available(coin):
            coins.append(coin)
            coinQ.append(quantity)
            port = [coins, coinQ]
            state[0] = port
            with open(portPickle, 'wb') as f:
                pickle.dump(state, f)
            response = jsonify({"Response": "Portfolio updated"})
        else:
            response = jsonify({"Response": "Error: Currency Unknown"})
    else:
        response = jsonify({"Response": "Error: Incorrect Password"})
    return response
    
def portUpdate(coins, coinQ):
    portSum = 0
    for i in range(len(coins)):
        coinPrice = priceCheck(coins[i])
        portSum = portSum + coinPrice * float(coinQ[i])
    return portSum
    
def available(coin):
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    output = response.json()
    cryptos = []
    for i in range(len(output)):
        cryptos.append(output[i]["id"])
    if coin in cryptos:
        return True
    else:
        return False
        
def priceCheck(coin):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + coin
    apiResp = requests.get(url)
    if apiResp.status_code == 200:
        apiResp = apiResp.json()
        price = apiResp[0]['current_price']
        print(price)
    else:
        price = 0
    return float(price) 
        
if __name__ == '__main__':
    setRGB(0, 255, 0)
    setText("Stocks :D")
    time.sleep(2)
    oldPort = 0
    parser = argparse.ArgumentParser(prog = 'cryptoServer', description = 'gaming')
    parser.add_argument('-p', metavar = 'password', required = True, help = 'Password')
    args = parser.parse_args()
    cryptoPassword = args.p
    forkID = os.fork()
    if forkID == 0:
        app.run(debug = False, host = '0.0.0.0', port = 5000)
    else:
        while(True):
            try:
                with open(portPickle, 'rb') as f:
                    state = pickle.load(f)
                    port = state[0]
                    mode = state[1]
                    coins = port[0]
                    coinQ = port[1]
            except FileNotFoundError:
                coins = []
                coinQ = []
                mode = ["0",""]
                port = [coins, coinQ]
                state = [port, mode]
                pass
            portSum = portUpdate(coins, coinQ)
            print(portSum)
            printStr = str(portSum)
            
            if len(printStr) < 16:
                for i in range(16 - len(printStr)):
                    printStr = printStr + " "
            else:
                printStr = printStr[0:16]
            dispStr = "0"
            
            if mode[0] == "0":
                disp = portSum - oldPort
                dispStr = str(disp)
            if mode[0] == "1":
                oldPort = portSum
                mode[0] = "0"
            if mode[0] == "2":
                disp = priceCheck(mode[1])
                dispStr = str(disp)
            if mode[0] == "3":
                if mode[1] == "1":
                    setRGB(255, 0, 0)
                elif mode[1] == "2":
                    setRGB(0, 255, 0)
                elif mode[1] == "3":
                    setRGB(0, 0, 255)
                    
            printStr = printStr + dispStr
            setText(printStr)
            print(mode[0], "is mode", mode[1], "is currency")
            time.sleep(15)
