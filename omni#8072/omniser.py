import serial
import os, sys
from tinydb import TinyDB, Query
import threading

query = Query()

if not os.path.isdir("db"):
    os.system("mkdir db")

try:
    open("db/curservos.json", "w").close()
    sdb = TinyDB("db/curservos.json")
except:
    print("restart script as sudo.")
    sys.exit()


PORT = ""
if os.name == "nt":
    PORT = "COM8"
else:
    PORT = "/dev/ttyACM0"

#For windows: "/COMX"  RPI: "/dev/ttyACM0"



def update():
    data = "000".encode()
    serial.write(data)

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 


ser = serial.Serial(PORT, 9600)




#reset position and db on start
data = "0.set0".encode()
ser.write(data)
data = "1.set0".encode()
ser.write(data)

data = {}
data["id"] = 0
data["pos"] = 0
sdb.insert(data)

data = {}
data["id"] = 1
data["pos"] = 0
sdb.insert(data)


print("Ready.\n")

t1 = threading.Thread(target=update)

def send(data:str):
    OUT = data.replace("> ", "")

    #end command
    if OUT == "end":
        print("terminating . . .")
        OUT = "0.set0"
        data = OUT.encode()
        ser.write(data)
        OUT = "1.set0"
        data = OUT.encode()
        ser.write(data)
        sys.exit()

    data = OUT.encode()
    print("sending " + str(OUT))

    #add new pos to db
    if "0." in OUT:
        if "end" in OUT:
            newpos = "0"
        else:
            outdata = OUT.replace("0.set", "")
            newpos = str(outdata)
        
        sdb.update({"pos":str(newpos)}, query.id == 0)

    elif "1." in OUT:
        if "end" in OUT:
            newpos = "0"
        else:
            outdata = OUT.replace("1.set", "")
            newpos = str(outdata)

        sdb.update({"pos":str(newpos)}, query.id == 1)


    

    ser.write(data)


while True:
    clear()

    IN = input("> ")
    send(IN)

