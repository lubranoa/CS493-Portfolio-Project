# Author: Alexander Lubrano
# Course: CS 493
# Assignment: Assignment 7 - More Authentication and Authorization
# Date: 05/22/2023
# File: main.py
# Description: This flask application

import json
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

BOATS = 'boats'

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


def get_resp(content, status):
    """Create a general response object"""
    response = make_response(jsonify(content))
    response.status_code = status
    return response


def get_entity(id):
    """Helper method for retrieving an entity stored on datastore

    Return a datastore object
    """
    key = client.key(BOATS, int(id))
    return client.get(key)


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


@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('callback', _external=True)
    )


@app.route('/callback', methods=['GET', 'POST'])
def callback():
    token = oauth.auth0.authorize_access_token()
    session['user'] = token
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


@app.route('/boats', methods=['POST', 'GET'])
def boats_post_get():
    """Handles requests to /boats route.

    If POST, validates the sent JWT. If JWT is valid, create a boat, set
    boat's owner to JWT's 'sub' value, put the boat on datastore, and return a
    response with status 201 that contains created boat info. If JWT is invalid
    or no JWT was provided, return a response with status 401 that contains
    any error info.

    If GET, validates the sent JWT. If JWT is valid, return response with
    status 200 that contains an array of all boats whose 'owner' value matches
    the JWT's 'sub' value. If JWT is invalid or no JWT was provided, return a
    response with status 200 that contains an array of all boats whose 'public'
    value is set to True regardless of owner.

    If disallowed method, returns a response with status 405 that contains an
    error message.
    """
    if request.method == 'POST':
        results = verify_jwt(request)
        if results.err is not None:
            return results.err
        content = request.get_json()
        new_boat = datastore.entity.Entity(key=client.key(BOATS))
        new_boat.update({'name': content['name'],
                         'type': content['type'],
                         'length': content['length'],
                         'public': content['public'],
                         'owner': results.payload['sub']})
        client.put(new_boat)
        new_boat['id'] = new_boat.key.id
        return get_resp(new_boat, 201)

    elif request.method == 'GET':
        query = client.query(kind=BOATS)
        results = verify_jwt(request)
        if results.err is not None:
            query.add_filter('public', '=', True)
        else:
            query.add_filter('owner', '=', results.payload['sub'])
        boats = list(query.fetch())
        for boat in boats:
            boat['id'] = boat.key.id
        return get_resp(boats, 200)

    else:
        return get_resp({'error': 'Method not allowed'}, 405)


@app.route('/boats/<id>', methods=['DELETE'])
def boats_delete(id):
    """Handles requests to /boats route.

    If DELETE, validates the sent JWT. Only deletes a boat if the sent JWT is
    valid, the boat exists, and the JWT's 'sub' value matches the boat's
    'owner' value. Then, delete the boat and return a response with status 204
    that contains no content.

    If JWT is invalid or no JWT was provided, return a response with status 401
    that contains any error info. If JWT is valid but no boat with the supplied
    boat id exists, return response with status 403 that contains an error
    message. If JWT is valid and the boat exists but is owned by a different
    owner, return response with status 403 that contains an error message.

    If disallowed method, returns a response with status 405 that contains an
    error message.
    """
    if request.method == 'DELETE':
        results = verify_jwt(request)
        if results.err is not None:
            return results.err
        boat = get_entity(id)
        if boat is None:
            return get_resp({'error': 'No boat with this boat id exists'}, 403)
        if results.payload['sub'] != boat['owner']:
            return get_resp({'error': 'Boat is owned by someone else'}, 403)
        client.delete(boat)
        return get_resp(None, 204)
    else:
        return get_resp({'error': 'Method not allowed'}, 405)


@app.route('/owners/<owner_id>/boats', methods=['GET'])
def owners_boats_get(owner_id):
    """Handles requests to /owners/:owner_id/boats route.

    If GET, returns a response with status 200 that contains an array of all
    boats whose 'owner' value matches the supplied owner id and whose 'public'
    values are set to True regardless of valid, invalid, or missing JWTs. If
    the owner has no public boats, returns a response with status 200 that
    contains an empty array.

    If disallowed method, returns a response with status 405 that contains an
    error message.
    """
    if request.method == 'GET':
        query = client.query(kind=BOATS)
        query.add_filter('public', '=', True)
        query.add_filter('owner', '=', owner_id)
        boats = list(query.fetch())
        for boat in boats:
            boat['id'] = boat.key.id
        return get_resp(boats, 200)
    else:
        return get_resp({'error': 'Method not allowed'}, 405)


# Decode the JWT supplied in the Authorization header
@app.route('/decode', methods=['GET'])
def decode_jwt():
    payload = verify_jwt(request)
    return get_resp(payload.payload, 200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
