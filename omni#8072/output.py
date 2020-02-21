import json
import sys
import os
import uuid
from datetime import datetime
import logging
import random
import time
import math

install = []
try: from tinydb import TinyDB, Query
except: install.append("TinyDB")

try: from colorama import Fore, init
except: install.append("colorama")

try: from ZeroLogger.ZeroLogger import *
except: install.append("ZeroLogger")

if install:
    to_install = " ".join(install)
    os.system(sys.executable + " -m pip install " + to_install)
    print("[STARTUP] INSTALLED MODULES: "+str(install))
    quit()

DELAY = 1

print("Connecting Database. . .")
try:histdb = TinyDB("db/history.json")
except Exception as err: critical("Cannot load Database!: "+str(err))

    
try:curdb = TinyDB("db/curstats.json")
except Exception as err: critical("Cannot load Database!: "+str(err))

query = Query()



init()



def refresh(delay = DELAY):
    now = datetime.now()
    curtime = now.strftime("%d.%m.%Y %H:%M:%S")
    try:
        voltage = curdb.search(query.id == id)[0]["voltage"]
    except IndexError:
        voltage = random.uniform(0,5)
        
    percentage = (voltage / 5) * 100
    amt = math.floor(percentage / 10)
    tomax = 10 - amt

    voltstring = "[" + 5*amt*"=" + 5*tomax *" " + "] " +str(voltage)

    

    os.system("cls")
    print(Fore.RESET + str(curtime) + "\n\n\n")
    #print(str(percentage))

    print(Fore.YELLOW + "Output "+ str(voltstring))
    time.sleep(int(delay))
    refresh(delay = DELAY)



while True:
    refresh()
    
