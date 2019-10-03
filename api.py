from __future__ import absolute_import, division, print_function
import logging
import time
import json
import redis

from flask import Flask, render_template, request
from flask_restful import Api, Resource

import core

logger = logging.getLogger(__name__)

config = core.Config()

app = Flask(__name__)
logger.info('Init flask ')

api = Api(app)
logger.info('Init API ')

logger.info(f'Init Redis {config["redis_host"]}:{config["redis_port"]}')
r = redis.Redis(host=config['redis_host'], port=int(config['redis_port']), db=0, decode_responses=True)
messages = {"First": "I'm the first message"}
r.hmset("messages", messages)

@app.route('/api/hello')
def hello():
    return json.dumps({'msg': 'hello world'})

@app.route('/api/echo/<msg>')
def echo(msg):
    return json.dumps({'msg': msg})

@app.route('/')
def index():
    s = r.hgetall("messages")
    return json.dumps(s)

@app.route('/config')
def getConfig():
  s = {}
  for k in config:
    s[k] = config[k]
  return str(s)

class Message(Resource):

  def get(self, title):
    messages = r.hgetall("messages")
    if title in messages:
      return messages[title],200
    else:
      return "Not Found", 404
  
  def post(self, title):
    messages[title] =  request.form['data']
    r.hmset("messages", messages)
    return {title: messages[title]}

  def delete(self, title):
    del messages[title]
    r.hmset("messages", messages)
    return "OK", 200

api.add_resource(Message, '/msg/<string:title>')
