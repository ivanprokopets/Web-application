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

import redis
import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'
db = redis.Redis(host='client_redis', port=6381, decode_responses=True)

JWT_SECREATE_DATABASE = "SECRET"
CDN = "http://localhost:5000"
WEB = "http://localhost:5001"
JWT_SECRET = "TESTSECRET"
JWT_SESSION_TIME = 30
SESSION_TIME = 180
INVALIDATE = -1
SESSION_ID = "session_id"

db.set("users:" + "test", "test")
db.set("users:" + "ivan", "ivan")
db.set("users:" + "login", "password")

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='zKR5GaNW9dAWqpUxUUXj7ZCN4gAtqPkr',
    client_secret='LsUabfN3AUVH2-1ytoDFya5dIlYVf5btKrUcmUiOxaNrw-O6RBkPW-oiWQ4nofpP',
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


@app.route('/auth', methods=['POST'])
def auth():
    response = make_response('', 303)
    login = request.form.get('login')
    password = request.form.get('password')
    if db.get("users:" + login) == password:
        session_id = str(uuid4())
        db.hset("session:" + session_id, "username", login)
        response.set_cookie(SESSION_ID, session_id, max_age=SESSION_TIME)
        response.headers["Location"] = "/send_pdf"
    else:
        response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
        response.headers["Location"] = "/"
    return response


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


@app.route('/logout')
def logout():
    response = make_response('', 303)
    response.set_cookie(SESSION_ID, "INVALIDATE", max_age=INVALIDATE)
    response.headers["Location"] = "/"
    return response


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
    userinfo=session['jwt_payload']
    print(userinfo)
    print(type(userinfo))
    response = make_response('', 303)
    session_id = str(uuid4())
    login=userinfo['name']
    db.hset("session:" + session_id, "username", login)
    print("SESSION ID", session_id)
    response.set_cookie(SESSION_ID, session_id, max_age=SESSION_TIME)
    response.headers["Location"] = "/send_pdf"
    return response

@app.route('/auth0_logout')
def auth0_logout():
    # Clear session stored data
    session.clear()
    return redirect(auth0.api_base_url + '/v2/logout?' + "http%3A%2F%2localhost:5001%2Flogout&client_id=zKR5GaNW9dAWqpUxUUXj7ZCN4gAtqPkr")


def mi_redirect(location):
    response = make_response('', 303)
    response.headers["Location"] = location
    return response
