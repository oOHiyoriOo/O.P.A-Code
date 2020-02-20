import os
import serial
from tinydb import TinyDB, Query
import random

open("db/measurements.json", "w").close() 
mdb = TinyDB("db/measurements.json")

query = Query()

rand = []
for i in range(4):
    rand.append(random.randint(0,100))

data = {}
data["input"] = rand
data["dir"] = ["U","D","L","R"]
data["id"] = 1
mdb.insert(data)


INPUT = mdb.search(query.id == 1)[0]["input"]
DIR = mdb.search(query.id == 1)[0]["dir"]
#print(INPUT)
#print(DIR)
MAX = max(INPUT)
IND = INPUT.index(max(INPUT))  
DIRECTION = DIR[IND]
#print(DIRECTION)

if DIRECTION == "L":
    print("Sending Left . . .")
    #TODO Send to db, rotate towards direction 

elif DIRECTION == "R":
    print("Sending Right . . .")


elif DIRECTION == "U":
    print("Sending Up . . .")


elif DIRECTION == "D":
    print("Sending Down . . .")




