import serial
import os, sys
from tinydb import TinyDB, Query



if not os.path.isdir("db"):
    os.system("mkdir db")


open("db/curservos.json", "w").close() #TODO: this is nonsense, make better workaround, not now tho
sdb = TinyDB("db/curservos.json")

data = {}
data["id"] = 0
data["pos"] = 0

sdb.insert(data)

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

ser = serial.Serial("COM5", 9600)

print("connected.\n")

def send(data):
    OUT = IN.replace("> ", "")

    if OUT == "r45":
        OUT = "r150"
    elif OUT == "r90":
        OUT = "r240"
    elif OUT == "l45":
        OUT = "l150"
    elif OUT == "l90":
        OUT = "l240"
    else: 
        OUT == "blink:3"

    data = OUT.encode()
    print("sending " + str(OUT))

    curpos = int(sdb.search(query.id == 1)[0]['pos'])
    #TODO: update database accordingly

    ser.write(data)


while True:
    clear()

    IN = input("> ")
    send(IN)
    

