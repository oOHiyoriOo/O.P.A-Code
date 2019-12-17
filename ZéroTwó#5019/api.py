
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

def mkconf():
    info("Called Func")

## Config Parsing an loading
try: from lib.config import cfg
except ModuleNotFoundError: 
    mkconf()
    critical("Pls Provide a config file, like the one in github.")

HOST = cfg['cn']['host']
PORT = cfg['cn']['port']

# user with edit rights
rootUser = cfg['root']['name']
rootPw = cfg['root']['pw']
# watch only user
watchUser = cfg['root']['wUser']

DbrootDir = cfg['dir']['DbRootDir']

info("Loaded config secussfully")

## Refresh the database on restart to prevent data trash
warn("Refreshing db.")

if not os.path.isdir(DbrootDir):
    warn("Creating Database Directory. . .")

    os.system("mkdir "+DbrootDir.replace("./","") )
try:
    udb = TinyDB(DbrootDir+"/auth.bin")
except Exception as err:
    critical("Cannot load Database!: "+err)

udb.insert({'root':{'user':'root','pass':'0000','cookie':'Created by Omni and ZéroTwó'},"wUser":{'user':'Node','cookie':'Created by Omni and ZéroTwó'}})





# FLASK
app = Flask(__name__)
api = Api(app)
CORS(app)




# query
query = Query()

class connect(Resource):
    def post(self):
        if request.form['user'] == rootUser and request.form['pass'] == rootPw:
            cookie = uuid4()

            return {'error':False,'cookie':cookie}
        
        elif request.form['user'] == watchUser:
            info("Read Only acces granted!")
        
        
        return {'status':200} 


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='DB_Server.log',level=logging.ERROR)
    info("Running app on: http://"+HOST+":"+str(PORT))

    api.add_resource(connect,'/api/login/') # login form :heh:

    app.run(host=HOST,port=PORT,debug=False)