import json
import sys
import os
import uuid
from datetime import datetime
from importlib import reload as BEANS
import json

import threading # sup routins

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
        curdb = TinyDB("db/curstats.json")

    if not os.path.isfile("/lib/config.py"):
        warn("No configuration file provided or configuration file unable to be read. \nCreating default file. . .")
        with open("lib/config.py","w") as cnf:
            cnf.write("""cfg = {
    "cn": {
        "host":"0.0.0.0",
        "port":8080,
    },
    
    "root":{
        "name":"root",
        "pw":"0000",

    "users":[
        "John Doe:Password"
    ],
        
    },
    "wUser":{
        "wUser":"Node", # watch only user.
        "wUserToken":[ # to limit read only acces we use tokens to grant access
            "2876665379"
        ],
    },
    "users":[
        "override:ov123"
    ],
    "dir":{
        "DbRootDir":"./db"  # pls provide full path ("./" is current directiony)
    }    

}""")
        info("Reloading Config.")
        return True
        #critical("Configuration file created. Please restart script.")


## Config Parsing an loading
try: from lib.config import cfg
except ModuleNotFoundError: 
    if mkconf():
        from lib.config import cfg


HOST = cfg['cn']['host']
PORT = cfg['cn']['port']

# user with edit rights
rootUser = cfg['root']['name']
rootPw = cfg['root']['pw']
rootCookie = str(uuid.uuid4())

#users
USERS = cfg["users"]

# watch only user
wUser = cfg['wUser']['wUser']
wUserToken = cfg['wUser']['wUserToken']

DbrootDir = cfg['dir']['DbRootDir']






if not os.path.isdir("db"):
    warn("Creating Database Directory. . .")
    os.system("mkdir db")

    
try:histdb = TinyDB("db/history.json")
except Exception as err: critical("Cannot load Database!: "+str(err))

    
try:reqdb = TinyDB("db/requests.json")
except Exception as err: critical("Cannot load Database!: "+str(err))

try: authdb = TinyDB('db/auth.bin')
except Exception as err: critical("Cannot load Auth Database: "+str(err))

if not os.path.isfile("db/curstats.json"):
    try:
        curdb = TinyDB("db/curstats.json")
    except Exception as err: critical("Cannot create database file!: "+str(err))
else:
    try:    
        curdb = TinyDB("db/curstats.json") 
        curdb.purge()
    except Exception:
        os.remove("db/curstats.json")
        curdb = TinyDB("db/curstats.json")


# flask base
app = Flask(__name__)
api = Api(app)
CORS(app)

# query
query = Query()

###################################################################################
###################################################################################
###################################################################################


def checkData(data:dict):
    if data['voltage'] != "" and data['batt'] != "" and data['x'] != "" and data['y'] != "":
        return True
    else:
        return False

def confReload(): # i cant reload critical things like HOST and PORT because the server is already running!
    global rootCookie
    global wUserToken
    global wUser
    global rootUser
    global rootPw
    from lib.config import cfg

    # user with edit rights
    rootUser = cfg['root']['name']
    rootPw = cfg['root']['pw']
    rootCookie = str(uuid.uuid4())

    #users
    USERS = cfg["users"]

    # watch only user
    wUser = cfg['wUser']['wUser']
    wUserToken = cfg['wUser']['wUserToken']


def logRequest(usr:str,data,valid:bool):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H:%M:%S")
    reqID = str(uuid.uuid4())

    Data = {}

    if str(data) == "":
        data = "NODATA"

    Data["fromUser"] = str(usr)
    Data["data"] = str(data)
    Data["requestID"] = str(reqID)
    Data["timestamp"] = str(timestamp)
    Data["valid"] = bool(valid)
    reqdb.insert(Data)




###################################################################################
###################################################################################
###################################################################################







class base(Resource):
    def post(self):

        usr = (request.form["user"])
        cookie = (request.form["cookie"])
        data = (request.form["data"])
        try:
            data = json.loads(data)
        except Exception as err:
            error("in Request: "+str(err))
            return {"error":True}
            
        # only root is permitted to post!
        if str(usr) == rootUser and str(cookie) == rootCookie:
            # curdb
            #| ID | time | CSpannung | BatterieLadung? | X | Y |

            if checkData(data):
                logRequest(usr,data,True) #Log Request
                
                update = {}
                update['ID'] = str(uuid.uuid4())
                update['time'] = datetime.now.strftime("%Y-%m-%d_%H:%M:%S")
                update['voltage'] = data['voltage']
                update['batt'] = data['batt'] # Batterie state.
                update['x'] = data['x']
                update['y'] = data['y']

                curdb.insert(update)

            else:
                logRequest(usr,data,False)
            
            

            return {"error":False}
            
        else:
            return {"error":True}


       

    def get(self):      #http://127.0.0.1:3600/?user=Node&cookie=2876665379
        if str(request.args['user']) == wUser and str(request.args['cookie']) in wUserToken:
            return {"error":False}
        else:
            return {"error":True}


class connect(Resource):
    confReload() # Reload to make sure everything is up to date!
    global rootCookie

    def post(self):
        if request.form['user'] == rootUser and request.form['pass'] == rootPw:
            rootCookie = str(uuid.uuid4())
            
            return {'error':False,'cookie':rootCookie}
        
        elif request.form['user'] == wUser and request.form['token'] in wUserToken:
            return {'error':False}

        else:
            return {'error':True} 

# just to check the cookie / auth is still valid!
class check(Resource):
    global rootCookie
    global wUserToken
    global wUser
    global rootUser
    def post(self):
        if request.form['user'] == rootUser and request.form['cookie'] == rootCookie:
            done_task("Valid Root user!")
            return {"error":False}
        elif request.form['user'] == wUser and request.form['cookie'] in wUserToken:
            return {"error":False}
        else:
            return {"error":True}

class QueryDB(Resource):
    def get(self):

        movingThread.stop = True

        try:
            info(request.args['user']+" : "+request.args['cookie'])

            if request.args['user'] == rootUser and request.args['cookie'] == rootCookie:
                return curdb.all()
            elif request.args['user'] == wUser and request.args['cookie'] in wUserToken:
                return curdb.all()
            else:
                return [{'error':True}]
        except:
            return [{'error':True}]









# willkommen in der threading hölle.
# Bitte nehmen sie sich einen keks UND kaffee
# wenn eines fehlt sterben wir also stell keine fragen und tu es einfach.



################################################################################################################
################################################################################################################
################################################################################################################

class DB_MOVER(threading.Thread):
    def __init__(self): # Pre define stuff like name etc...
        threading.Thread.__init__(self)
        self.stop = False
        self.name = "DB_Mover"

    def run(self):
        while not self.stop:
            time = datetime.now().strftime('%H:%M:%S')
            if str(time) == "00:00:00":
                entrys = curdb.all()
                info("Moving: "+str(entrys))






































if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='DB_Server.log',level=logging.ERROR)
        
    if sys.platform == "linux":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')
    else:
        error("Dont know what platform this is.")

    info("Now running on port "+str(PORT))

    api.add_resource(base,'/') # send raw request data to database
    api.add_resource(connect,'/api/login/') # login form
    api.add_resource(QueryDB,'/query/')

    movingThread = DB_MOVER()
    movingThread.start()

    app.run(host=HOST,port=PORT,debug=False)