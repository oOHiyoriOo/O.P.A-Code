import uuid
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
rootCookie = str(uuid.uuid4())
# watch only user
wUser = cfg['wUser']['wUser']
wUserToken = cfg['wUser']['wUserToken']

DbrootDir = cfg['dir']['DbRootDir']

info("Loaded config secussfully")


# snipped for handling db's
# if not os.path.isdir(DbrootDir):
#     warn("Creating Database Directory. . .")

#     os.system("mkdir "+DbrootDir.replace("./","") )
# try:
#     udb = TinyDB(DbrootDir+"/auth.bin")
# except Exception as err:
#     critical("Cannot load Database!: "+err)

# FLASK
app = Flask(__name__)
api = Api(app)
CORS(app)




# query
query = Query()

class ping():
    def get(self):
        return {'error':False}
    def post(self):
        return {'error':False}

class connect(Resource):
    global rootCookie

    def post(self):
        if request.form['user'] == rootUser and request.form['pass'] == rootPw:
            rootCookie = uuid.uuid4()
            return {'error':False,'cookie':rootCookie}
        
        elif request.form['user'] == wUser and request.form['token'] in wUserToken:
            return {'error':False}

        else:
            return {'error':True} 


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='DB_Server.log',level=logging.ERROR)
    info("Running app on: http://"+HOST+":"+str(PORT))

    api.add_resource(ping,"/ping") # are u there ?
    api.add_resource(connect,'/api/login/') # login form

    app.run(host=HOST,port=PORT,debug=False)