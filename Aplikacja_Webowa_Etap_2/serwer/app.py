from flask import  Flask, request, jsonify,redirect, make_response ,send_file

import sys
import redis
import hashlib

POST = "POST"
GET = "GET"
SESSION_ID = "session-id"
INVALIDATE = -1

app = Flask(__name__)

db = redis.Redis(host='redis', port=6379, decode_responses=True)
db.flushdb()

bazadanych = {'admin': "admin"}



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
