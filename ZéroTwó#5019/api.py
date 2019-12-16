
from uuid import uuid4
import json
import sys 
import os

# install modules if missing!
install = []
try: from tinydb import TinyDB, Query
except: install.append("TinyDB")

try: from flask import Flask, abort, request
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

if install:
    to_install = " ".join(install)
    os.system(sys.executable + " -m pip install " + to_install)
    print("[STARTUP] INSTALLED MODULES: "+str(install))
    quit()

init()

## Config Parsing an loading
try: from lib.config import cfg
except FileNotFoundError: critical("Pls Provide a config file, like the one in github.")

HOST = cfg['cn']['host']
PORT = cfg['cn']['port']

rootUser = cfg['root']['name']
rootPw = cfg['root']['pw']

DbrootDir = cfg['dir']['DbRootDir']

info("Loaded config secussfully")

warn("Loading Args.")

import lib.args as ParseArgs


# FLAK
app = Flask(__name__)
api = Api(app)
CORS(app)


# Try to loud it 2 times!
try:udb = TinyDB(DbrootDir+"/auth.bin")
except FileNotFoundError: 
    error("No Db Directiony... trying to fix your mess!")
    try:os.system("mkdir "+DbrootDir)
    except Exception as err: critical("Cant create Directiony!")

try:udb = TinyDB(DbrootDir+"/auth.bin")
except Exception as err: critical("Cant Load Db!: "+err)


# query
query = Query()

class connect(Resource):
    def post(self):
        info(request.form)
        return {"error":False}


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='DB_Server.log',level=logging.ERROR)
    info("Running app on: http://"+HOST+":"+str(PORT))

    api.add_resource(connect,'/api/login/') # login form :heh:

    app.run(host=HOST,port=PORT,debug=False)