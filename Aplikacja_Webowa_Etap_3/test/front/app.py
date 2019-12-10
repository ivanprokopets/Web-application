from flask import Flask
app = Flask(__name__)

@app.route("/front")
def main():
    return "Welcome from front!"