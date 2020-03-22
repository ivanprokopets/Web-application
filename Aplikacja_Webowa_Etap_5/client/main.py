from flask import render_template

from jwt import encode
from uuid import uuid4
from flask import Flask
from flask import session
from flask import redirect
from functools import wraps
import json
from authlib.flask.client import OAuth
from flask import url_for
from six.moves.urllib.parse import urlencode
from flask import request
from flask import make_response
from dotenv import load_dotenv
from os import getenv

load_dotenv(verbose=True)
import redis
import datetime

app = Flask(__name__)
JWT_SECRET = getenv('JWT_SECRET')
CDN = getenv("CDN")
WEB = getenv("WEB")
JWT_SECREATE_DATABASE = getenv("JWT_SECREATE_DATABASE")
JWT_SESSION_TIME = int(getenv('JWT_SESSION_TIME'))
SESSION_TIME = int(getenv("SESSION_TIME"))
app.secret_key = 'super secret key'
db = redis.Redis(host='client_redis', port=6381, decode_responses=True)
INVALIDATE = -1
SESSION_ID = "session_id"
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=getenv('client_id'),
    client_secret=getenv('client_secret'),
    api_base_url='https://dev--q5a6esf.auth0.com',
    access_token_url='https://dev--q5a6esf.auth0.com/oauth/token',
    authorize_url='https://dev--q5a6esf.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/')
def index():
    return render_template('login.html', WEB=WEB)


@app.route('/send_pdf', methods=['GET'])
def upload():
    session_id = request.cookies.get(SESSION_ID)
    if session_id:
        content_type = "application/pdf"
        login = db.hget("session:" + session_id, "username")
        fids = db.hvals("files:" + login)
        download_tokens = []
        filenames = []
        for fidx in fids:
            download_tokens.append(create_download_token(fidx).decode())
            filenames.append(db.hget("filename:" + login, fidx))
        upload_token = create_upload_token().decode('ascii')
        return render_template("send_pdf.html",
                               fids=fids,
                               content_type=content_type,
                               CDN=CDN,
                               upload_token=upload_token,
                               download_tokens=download_tokens,
                               WEB=WEB,
                               filenames=filenames)
    return mi_redirect("/")


@app.route('/error', methods=['GET'])
def wrong():
    return render_template('error.html')


@app.route('/callback')
def uploaded():
    session_id = request.cookies.get(SESSION_ID)
    print("SESSION ID", session_id)
    fid = request.args.get('fid')
    err = request.args.get('error')
    filename = request.args.get('namefile')
    print(filename)
    if not session_id:
        return redirect("/")
        return mi_redirect("/")
    if err:
        return f"<h1>APP</h1> Upload failed: {err}", 400
    if not fid:
        return f"<h1>APP</h1> Upload successfull, but no fid returned", 500
    new_fied_prefix = str(db.incr(JWT_SECREATE_DATABASE))
    new_fied = new_fied_prefix + fid
    login = db.hget("session:" + session_id, "username")
    db.hset("files:" + login, new_fied, fid)
    db.hset("filename:" + login, fid, filename)
    return mi_redirect("/send_pdf")


def create_download_token(fid):
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({"iss": "client", "exp": exp}, JWT_SECRET, "HS256")


def create_upload_token():
    exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_SESSION_TIME)
    return encode({"iss": "client", "exp": exp}, JWT_SECRET, "HS256")


@app.route('/auth0_callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return mi_redirect('/dashboard')


@app.route('/auth0_login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5001/auth0_callback')


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return mi_redirect('/')
        return f(*args, **kwargs)

    return decorated


@app.route('/dashboard')
@requires_auth
def dashboard():
    print(session['profile'])
    userinfo = session['jwt_payload']
    print(userinfo)
    print(type(userinfo))
    response = make_response('', 303)
    session_id = str(uuid4())
    login = userinfo['name']
    db.hset("session:" + session_id, "username", login)
    print("SESSION ID", session_id)
    response.set_cookie(SESSION_ID, session_id, max_age=SESSION_TIME, httponly=True)
    response.headers["Location"] = "/send_pdf"
    return response


@app.route('/auth0_logout')
def auth0_logout():
    # Clear session stored data
    session_id = request.cookies.get(SESSION_ID)
    print("TEST", db.hget("session:" + session_id, "username"))
    dele = db.hdel("session:" + session_id, "username")
    print("DELETE SESJA", dele)
    client_id = getenv('client_id')
    response = redirect(
        auth0.api_base_url + '/v2/logout?' + "http%3A%2F%2localhost:5001%2Flogout&client_id=" + client_id)
    response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE, httponly=True)
    print("SESSION ID", SESSION_ID)
    session.clear()
    return response


def mi_redirect(location):
    response = make_response('', 303)
    response.headers["Location"] = location
    return response
