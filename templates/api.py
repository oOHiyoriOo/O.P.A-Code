from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask import Flask, abort, request
from flask_restful import Resource, Api
from json import dumps
# from flask.ext.jsonpify import jsonify not working anymore use below:
from flask_jsonpify import jsonify

import os
import string
from colorama import Fore, init
init()

true_key = "3124" #read password form fiel later

chatbot = ChatBot("Hiyori")


if not os.path.isfile("db.sqlite3"):
    conversation = [    # read this from file too later
        "hallo",        # for configurable sentences
        "hi"            #
    ]                   # 

    trainer = ListTrainer(chatbot)
    trainer.train(conversation)

################## Functions ######################################
def warn(text):
    print("["+Fore.YELLOW+"WARN"+Fore.RESET+"] "+str(text))

def error(text):
    print("["+Fore.RED+"ERROR"+Fore.RESET+"] "+str(text))

def done_task(text):
    print("["+Fore.GREEN+"DONE"+Fore.RESET+"] "+str(text))

################## END LOGGING ###################################


from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/add_message/<key>', methods=['GET', 'POST'])
def add_message(key):
    if key == true_key:
        content = request.json
        print(str(content))
        return jsonify({"answer":str(chatbot.get_response(content['text'])) })

if __name__ == '__main__':
    app.run(port= '3406',debug=False)