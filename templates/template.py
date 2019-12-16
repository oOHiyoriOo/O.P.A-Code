
from uuid import uuid4
import json
import sys 

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

# Standart Values:
PORT = 3406
HOST = "127.0.0.1"
## ARG Parsing
ARGS = sys.argv[1:]
i = 0
for arg in ARGS:
    if arg == "-H":
        try:
            HOST = str(ARGS[i + 1])
        except ValueError:
            critical("Invalid HOST!")
        except Exception as err:
            critical(str(err))
    i = i + 1


# FLAK
app = Flask(__name__)
api = Api(app)
CORS(app)

udb = TinyDB('./data/user.db')
keydb = TinyDB('./data/keys.data')
cdb = TinyDB('./data/msg.json')

# query
query = Query()

class login(Resource):
    def post(self):
        return {'error':True,'msg':'No such User'}

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='error.log',level=logging.ERROR)
    info("Running app on: http://"+HOST+":"+str(PORT))

    api.add_resource(login,'/api/login/') # login form :heh:

    app.run(host=HOST,port=PORT,debug=False)