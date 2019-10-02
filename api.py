from __future__ import absolute_import, division, print_function
import logging
import time
import json

from flask import Flask
from flask_restful import Api, Resource
from flasgger import Swagger

import core

logger = logging.getLogger(__name__)

config = core.Config()

app = Flask(__name__)
logger.info('Init flask ')

api = Api(app)
logger.info('Init API ')


@app.route('/api/hello')
def index():
    return json.dumps({'msg': 'hello world'})

@app.route('/api/echo/<msg>')
def echo(msg):
    return json.dumps({'msg': msg})