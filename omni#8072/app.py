from uuid import uuid4
import json
import sys
import os
import uuid
from datetime import datetime


# install modules if missing!
install = []
try: from tinydb import TinyDB, Query
except: install.append("TinyDB")

try: from flask import Flask, abort, request, Response
except: install.append("flask")

try: from flask_restful import Resource, Api
except: install.append("flask_restful")

try: from flask_jsonpify import jsonify
except: install.append("flask_jsonpify")

try: from colorama import Fore, init
except: install.append("colorama")

try: from ZeroLogger.ZeroLogger import *
except: install.append("ZeroLogger")

try: from flask_cors import CORS
except: install.append("flask_cors")

import logging

if install:
    to_install = " ".join(install)
    os.system(sys.executable + " -m pip install " + to_install)
    print("[STARTUP] INSTALLED MODULES: "+str(install))
    quit()

init()

def mkconf():
    if not os.path.isdir("lib"):
        warn("Creating Libraries Directory. . .")
        os.system("mkdir lib")

    if not os.path.isfile("/lib/config.py"):
        warn("No configuration file provided or configuration file unable to be read. \nCreating default file. . .")
        with open("lib/config.py","w") as cnf:
            cnf.write("""cfg = {"cn": {"host":"0.0.0.0","port":8080,},"root":{"name":"root","pw":"0000","wUser":"Node"},"dir":{"DbRootDir":"./db"}}""")
        critical("Configuration file created. Please restart script.")


## Config Parsing an loading
try: from lib.config import cfg
except ModuleNotFoundError: mkconf()


if not os.path.isdir("db"):
    warn("Creating Database Directory. . .")
    os.system("mkdir db")

    
try:histdb = TinyDB("db/history.json")
except Exception as err: critical("Cannot load Database!: "+str(err))

    
try:reqdb = TinyDB("db/requests.json")
except Exception as err: critical("Cannot load Database!: "+str(err))


if not os.path.isfile("db/curstats.json"):
    try:
        curdb = TinyDB("db/curstats.json")
    except Exception as err: critical("Cannot create database file!: "+str(err))
else:
    try:     
        curdb.purge()
    except Exception:
        os.remove("db/curstats.json")
        curdb = TinyDB("db/curstats.json")

HOST = cfg['cn']['host']
PORT = cfg['cn']['port']

rootUser = cfg['root']['name']
rootPw = cfg['root']['pw']

DbrootDir = cfg['dir']['DbRootDir']

warn("Loaded config sucessfully.")

# flask base
app = Flask(__name__)
api = Api(app)
CORS(app)

# query
query = Query()

class base(Resource):
    def post(self):

        usr = (request.form["user"])
        print("<<< " + str(usr))
        data = (request.form["data"])
        print(data)
        #Post Denied
        if str(usr) != "PI":
            print(">>> 403")
            ret = '{"RESPONSE": 403}'

            resp = Response(response=ret,
                        status=403,
                        mimetype="application/json") 
            return resp
        #Post Accepted
        if str(usr) == "PI":
            print(">>> 200")
            
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
            reqID = uuid.uuid4()

            Data = {}

            if str(data) == "":
                data = "NODATA"

            Data["fromUser"] = str(usr)
            Data["isAdmin"] = False
            Data["data"] = str(data)
            Data["requestID"] = str(reqID)
            Data["timestamp"] = str(timestamp)

            reqdb.insert(Data)

            ret = '{"RESPONSE": 200}'

            resp = Response(response=ret,
                        status=200,
                        mimetype="application/json") 
            return resp
    #Deny GET requests
    def get(self):
        ret = '{"RESPONSE": 403}'

        resp = Response(response=ret,
                    status=403,
                    mimetype="application/json")

        return resp

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='error.log',level=logging.ERROR)
    os.system("cls")
    info("Now running on port "+str(PORT))

    api.add_resource(base,'/') 

    app.run(host=HOST,port=PORT,debug=False)
