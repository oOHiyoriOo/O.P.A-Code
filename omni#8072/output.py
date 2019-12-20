import json
import sys
import os
import uuid
from datetime import datetime
import logging
import random
import time

install = []
try: from tinydb import TinyDB, Query
except: install.append("TinyDB")

try: from colorama import Fore, init
except: install.append("colorama")

try: from ZeroLogger.ZeroLogger import *
except: install.append("ZeroLogger")




try:histdb = TinyDB("db/history.json")
except Exception as err: critical("Cannot load Database!: "+str(err))

    
try:curdb = TinyDB("db/curstats.json")
except Exception as err: critical("Cannot load Database!: "+str(err))

query = Query()

if install:
    to_install = " ".join(install)
    os.system(sys.executable + " -m pip install " + to_install)
    print("[STARTUP] INSTALLED MODULES: "+str(install))
    quit()

init()

print("Connecting Database. . .")

def refresh(delay = 3):
    now = datetime.now()
    time = now.strftime("%d.%m.%Y %H:%M:%S")
    try:
        voltage = curdb.search(query.id == id)[0]["voltage"]
    except IndexError:
        voltage = random.uniform(0,5)
        
    percentage = (voltage / 5) * 100   
    voltstring = "["

    

    os.system("cls")
    print(Fore.RESET + str(time) + "\n\n\n")
    print(str(percentage))
    print(Fore.BLUE + "Output "+ str(voltstring))
    time.sleep(delay)
    refresh(delay = 3)



while True:
    refresh()
    
