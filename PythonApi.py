from uuid import uuid4
import json
import sys
import os


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

## Config Parsing an loading
try: from lib.config import cfg
#TODO auto config creation
except FileNotFoundError: warn("Configuration file not found.")

HOST = cfg['cn']['host']
PORT = cfg['cn']['port']

rootUser = cfg['root']['name']
rootPw = cfg['root']['pw']

DbrootDir = cfg['dir']['DbRootDir']

info("Loaded config sucessfully.")

info("Loading Args.")


# flask base
app = Flask(__name__)
api = Api(app)
CORS(app)

#TODO fix this nonsense
if not os.path.isdir("db"):
    warn("Creating Database Directory. . .")
    os.system("mkdir db")

try:udb = TinyDB(DbrootDir+"/auth.bin")
except Exception as err: critical("Cannot load Database!: "+err)


# query
query = Query()

class base(Resource):
    def post(self):

        usr = (request.form["user"])
        print("<<< " + str(usr))
        data = print(request.form["data"])
        print(data)

        if str(usr) != "PI":
            print(">>> 403")
            return {"RESPONSE":403}
        if str(usr) == "PI":
            print(">>> 200")
            return {"RESPONSE":200}
            
        

    def get(self):
        ret = '{"RESPONSE": "200"}'

        resp = Response(response=ret,
                    status=404,
                    mimetype="application/json")

        return resp

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='error.log',level=logging.ERROR)
    info("Now running on port "+str(PORT))

    api.add_resource(base,'/') 


    app.run(host=HOST,port=PORT,debug=False)