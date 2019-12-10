from flask import Flask
from .api_blueprint import api
from .front_blueprint import front
app = Flask(__name__)
app.register_blueprint(front, url_prefix= '/front')
app.register_blueprint(api, url_prefix= '/api')

@app.route("/")
def main():
    return "Welcome from base app!"