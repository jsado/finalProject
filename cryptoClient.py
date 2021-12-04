from pprint import pprint
import json
import requests
import argparse

parser = argparse.ArgumentParser(prog = "cryptoClient", description = "gaming")
parser.add_argument('-p', metavar = 'password', required = True, help = 'Password')
parser.add_argument('-i', metavar = 'ip', required = True, help = 'IP Address')
args = parser.parse_args()
password = args.p
ip = args.i
address = ip + ':5000'

while True:
    print("Commands:\n1. Edit portfolio\n2. Reset portfolio\n3. Check portfolio\n4. Configure display\nq. Quit")
    command = input()
    
    if command == "1":
        while(True):
            print("Enter coin and amount (ex. dogecoin 69); can enter negative numbers; enter q to stop")
            coinAdd = input()
            if coinAdd == 'q':
                break
            if " " in coinAdd:
                ind = coinAdd.find(" ")
            else:
                print("Error: Improper Formatting")
                break
            quantity = coinAdd[ind+1:len(coinAdd)]
            quantity = quantity
            coin = coinAdd[0:ind]
            params = {
                'password': password,
                'coin': coin,
                'quantity': quantity
            }
            response = requests.get("http://{}/crypto/edit".format(address), params = params)
            pprint(response.json())
            
    elif command == "2":
        params = {
            'password': password
        }
        response = requests.get("http://{}/crypto/reset".format(address), params = params)
        pprint(response.json())
        
    elif command == "3":
        params = {
            'password': password
        }
        response = requests.get("http://{}/crypto/check".format(address), params = params)
        pprint(response.json())
    
    elif command == "4":
        mode = 0
        single = ""
        print("Display Config:\n1. Portfolio change\n2. Reset\n3. Single currency\n4. Color change")
        config = input()
        if config not in "1234":
            print("Error: Unknown Command")
            break
        mode = int(config) - 1
        if mode == 2:
            single = input("Currency: ")    
        if mode == 3:
            single = input("Colors:\n1. Red\n2. Green\n3. Blue\n")
            if single not in "123":
                print("Error: Unknown Command")
                break
        params = {
            'password': password,
            'mode': str(mode),
            'currency': single
        }
        response = requests.get("http://{}/crypto/mode".format(address), params = params)
        pprint(response.json())
    elif command == 'q':
        break
    
    else:
        print("Error: Unknown Command")
    print("\n")
#response = requests.get("http://{}/crypto".format(address), params = params)
#pprint(response.json())
