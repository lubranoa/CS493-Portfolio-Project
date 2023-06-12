# Author: Alexander Lubrano
# Course: CS 493
# Assignment: Portfolio Project
# Date: 06/11/2023
# File: main.py
# Description: This flask application

import json
import const
import err_obj
import boats
import loads

from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from flask import Flask, redirect, render_template, session, make_response
from flask import url_for, request, jsonify, _request_ctx_stack

from six.moves.urllib.request import urlopen
from jose import jwt

from google.cloud import datastore

# -------------------------------------------------------------------------------
# Much of this program is adapted from three sources:
#
#   1) Example program from Exploration - Authentication in Python
#   2) Auth0 Python Tutorial:
#      - https://auth0.com/docs/quickstart/webapp/python
#   3) Auth0 Python API: Authorization:
#      - https://auth0.com/docs/quickstart/backend/python/01-authorization
#
# -------------------------------------------------------------------------------

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_DOMAIN = str(env.get('AUTH0_DOMAIN'))
AUTH0_CLIENT_ID = str(env.get('AUTH0_CLIENT_ID'))
AUTH0_CLIENT_SECRET = str(env.get('AUTH0_CLIENT_SECRET'))
ALGORITHMS = ['RS256']

app = Flask(__name__)
app.secret_key = env.get('APP_SECRET_KEY')
client = datastore.Client()

BASE_URL = const.BASE_GAE_URL


# Error handling class
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Result handling class
class Result():
    def __init__(self, err=None, payload=None, token=None):
        """Initializes a Result class object with properties that hold error,
        payload, and token objects.

        Error property used to hold error response objects of any AuthErrors
        that occur in JWT verification.

        Payload property used to hold a decoded JWT payload.

        Token property used to hold a token authorization header.
        """
        self.err = err
        self.payload = payload
        self.token = token


oauth = OAuth(app)

oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url='https://' + AUTH0_DOMAIN,
    access_token_url='https://' + AUTH0_DOMAIN + '/oauth/token',
    authorize_url='https://' + AUTH0_DOMAIN + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}'
                        '/.well-known/openid-configuration'
)


def get_auth_error_resp(err):
    """Create an authorization error response object"""
    response = make_response(jsonify(err.error))
    response.status_code = err.status_code
    return response


def get_resp(content, status, make_json=True):
    """Create a general response object"""
    response = make_response(jsonify(content))
    response.status_code = status
    if not make_json:
        response.mimetype = const.TEXT_PLAIN
    return response


def get_entity(entity, id):
    """Helper method for retrieving an entity stored on datastore

    Return a datastore object
    """
    key = client.key(entity, id)
    return client.get(key)


def create_entity(key_val, info, id=None):
    if id is None:
        new_key = client.key(key_val)
    else:
        new_key = client.key(key_val, id)
    entity = datastore.Entity(key=new_key)
    entity.update(info)
    client.put(entity)
    return entity


# Format error response and append status code
def get_token_auth_header(req):
    """Obtains the Access Token from the Authorization Header
    """
    results = Result()
    auth = req.headers.get('Authorization', None)
    if not auth:
        results.err = get_auth_error_resp(
            AuthError({'code': 'authorization_header_missing',
                       'description':
                       'Authorization header is expected'}, 401))
        return results

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        results.err = get_auth_error_resp(
            AuthError({'code': 'invalid_header',
                       'description':
                       'Authorization header must start with Bearer'}, 401))
        return results
    elif len(parts) == 1:
        results.err = get_auth_error_resp(
            AuthError({'code': 'invalid_header',
                       'description':
                       'Token not found'}, 401))
        return results
    elif len(parts) > 2:
        results.err = get_auth_error_resp(
            AuthError({"code": "invalid_header",
                       "description":
                       "Authorization header must be Bearer token"}, 401))
        return results

    results.token = parts[1]
    return results


def verify_jwt(req):
    """Determines if the Access Token is valid
    """
    results = get_token_auth_header(req)
    if results.err is not None:
        return results
    jsonurl = urlopen('https://'+AUTH0_DOMAIN+'/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(results.token)
    except jwt.JWTError:
        results.err = get_auth_error_resp(
            AuthError({"code": "invalid_header",
                       "description":
                       'Invalid header.'
                       ' Use an RS256 signed JWT Access Token'}, 401))
        return results

    if unverified_header["alg"] == "HS256":
        results.err = get_auth_error_resp(
            AuthError({"code": "invalid_header",
                       "description":
                       "Invalid header."
                       " Use an RS256 signed JWT Access Token"}, 401))
        return results

    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                results.token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_CLIENT_ID,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )
        except jwt.ExpiredSignatureError:
            results.err = get_auth_error_resp(
                AuthError({'code': 'token_expired',
                           'description':
                           'token is expired'}, 401))
            return results

        except jwt.JWTClaimsError:
            results.err = get_auth_error_resp(
                AuthError({'code': 'invalid_claims',
                           'description':
                           'incorrect claims,'
                           ' please check the audience and issuer'}, 401))
            return results

        except Exception:
            results.err = get_auth_error_resp(
                AuthError({'code': 'invalid_header',
                           'description':
                           'Unable to parse authentication token.'}, 401))
            return results

        _request_ctx_stack.top.current_user = payload
        results.payload = payload
        return results
    else:
        results.err = get_auth_error_resp(
            AuthError({'code': 'invalid_header',
                       'description':
                       'Unable to find appropriate key'}, 401))
        return results


app.register_blueprint(boats.bp)
app.register_blueprint(loads.bp)


@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('callback', _external=True)
    )


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    token = oauth.auth0.authorize_access_token()
    session['user'] = token
    user_id = token['userinfo']['sub']
    entity = get_entity(const.USERS, user_id)
    if not entity:
        create_entity(
            const.USERS,
            {'name': token['userinfo']['name']},
            user_id)
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        'https://' + env.get('AUTH0_DOMAIN')
        + '/v2/logout?'
        + urlencode(
            {
                'returnTo': url_for('index', _external=True),
                'client_id': AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )


@app.route('/')
def index():
    return render_template(
        'index.html',
        session=session.get('user'),
        pretty=json.dumps(session.get('user'), indent=4))


@app.route('/users', methods=['GET'])
def users_get():
    """"""
    if const.APP_JSON not in request.accept_mimetypes:
        return get_resp(err_obj.WRONG_ACCEPT_406['msg'],
                        err_obj.WRONG_ACCEPT_406['status'],
                        False)

    if request.method == 'GET':
        query = client.query(kind=const.USERS)
        users = list(query.fetch())
        for user in users:
            user['id'] = user.key.id
        return get_resp(users, 200)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


if __name__ == '__main__':
    BASE_URL = const.BASE_LOCAL_URL
    app.run(host='127.0.0.1', port=8080, debug=True)
