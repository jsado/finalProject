Team members: Justin Sado
Demo link: 
https://drive.google.com/file/d/1kvTaWrfsdbXzuxVnKJ0HMXT_c37r_Rmb/view?usp=sharing
Github repo link: 
	SSH - git@github.com:jsado/finalProject.git
	HTTPS - https://github.com/jsado/finalProject.git
Instructions:
	1. Connect the GrovePi RGB LCD Display to 12C-3 on the GrovePi shield
	2. Download cryptoServer.py onto the rPi
	3. In a command line and from the folder containing cryptoServer.py, run: python3 cryptoServer.py -p [arbitrary password]
	4. Download cryptoClient.py onto any client computer on the same network as the rPi
	5. In a command line on the client computer, run: python3 cryptoClient.py -p [password] -i [rPi IP address]
		note: the IP address of the rPi can be found by running ifconfig -a in a command line on the rPi
Libraries:
grove_rgb_lcd
os
flask
json
requests
socket
urllib.request
argparse 
pickle
pprint
