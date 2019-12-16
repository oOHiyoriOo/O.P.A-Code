from flask import Flask, abort, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

import os
import string

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/add_message/<key>', methods=['GET', 'POST'])
def add_message(key):
    pass

if __name__ == '__main__':
    app.run(port= '8080',debug=False)