import serial
import os

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

ser = serial.Serial("COM8", 9600)

print("connected.\n")

while True:
    clear()

    IN = input("> ")
    OUT = IN.replace("> ", "")

    if OUT == "r45":
        OUT = "r150"
    elif OUT == "r90":
        OUT = "r240"
    elif OUT == "l45":
        OUT = "l150"
    elif OUT == "l90":
        OUT = "l240"





    data = OUT.encode()
    print("sending " + str(OUT))

    ser.write(data)

