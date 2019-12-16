
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

import logging




if install:
    to_install = " ".join(install)
    os.system(sys.executable + " -m pip install " + to_install)
    print("[STARTUP] INSTALLED MODULES: "+str(install))
    quit()

init()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# defaults:
PORT = 8080
HOST = "127.0.0.1"


## parsing
ARGS = sys.argv[1:]
i = 0
for arg in ARGS:
    if arg == "-H" or arg == "--Host":
        try:
            HOST = str(ARGS[i + 1])
        except ValueError:
            critical("Invalid HOST!")
        except Exception as err:
            critical(str(err))
    i = i + 1

#TODO: -p, -h -v 


# flask base
app = Flask(__name__)
api = Api(app)
CORS(app)

# udb = TinyDB('./data/user.db')
# keydb = TinyDB('./data/keys.data')
# cdb = TinyDB('./data/msg.json')

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
        return 200

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='error.log',level=logging.ERROR)
    info("Now running on port "+str(PORT))

    api.add_resource(base,'/') 


    app.run(host=HOST,port=PORT,debug=False)