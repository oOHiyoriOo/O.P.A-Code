import serial
import os, sys
from tinydb import TinyDB, Query



query = Query()

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

def send(data:str):
    OUT = data.replace("> ", "")

    if OUT == "r45":
        OUT = "r150"
    elif OUT == "r90":
        OUT = "r240"
    elif OUT == "l45":
        OUT = "l150"
    elif OUT == "l90":
        OUT = "l240"

    elif OUT == "terminate":
        print("terminating. . .")
        curpos = int(sdb.search(query.id == 0)[0]['pos'])
        
        if curpos < 0:
            OUT = "r" +  str(curpos).replace("-", "")
            print(OUT)
        elif curpos > 0:
            OUT = "l" + str(curpos)

        data = OUT.encode()
        ser.write(data)
        print("Terminated.")
        sys.exit()

        

    curpos = int(sdb.search(query.id == 0)[0]['pos'])

    if "l" in OUT:
        outdata = OUT.replace("l", "")
        newpos = int(curpos) - int(outdata)

    elif "r" in OUT:
        outdata = OUT.replace("r", "")
        newpos = int(curpos) + int(outdata)


    data = OUT.encode()
    print("sending " + str(OUT))

   
    #print(curpos)
    
    sdb.update({"pos":int(newpos)}, query.id == 0)
    #TODO: update database accordingly

    ser.write(data)


while True:
    clear()

    IN = input("> ")
    send(IN)
    

