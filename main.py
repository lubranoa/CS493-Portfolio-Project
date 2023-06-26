# Author: Alexander Lubrano
# Course: CS 493
# Assignment: Portfolio Project
# Date: 06/11/2023
# File: main.py

# TODO: Add authentication to load routes
# TODO: Add comments

import json
import const
import err_obj

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
# Some of this program is adapted from three sources:
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


def construct_loads(loads):
    """Construct a loads list from a list of load ID values for boat
    response objects

    Return a list of load dictionaries with the attributes 'id' and 'self'
    """
    load_arr = []
    for load_id in loads:
        load_arr.append({
            "id": int(load_id),
            "self": BASE_URL + '/loads/' + str(load_id)})
    return load_arr


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


@app.route('/users', methods=const.METHODS)
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
            user['id'] = user.key.id_or_name
        return get_resp(users, 200)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


@app.route('/boats', methods=const.METHODS)
def boats_post_get():
    """"""
    if const.APP_JSON not in request.accept_mimetypes:
        return get_resp(err_obj.WRONG_ACCEPT_406['msg'],
                        err_obj.WRONG_ACCEPT_406['status'],
                        False)

    if request.method == 'POST':

        if request.mimetype != const.APP_JSON:
            return get_resp(err_obj.WRONG_TYPE_415['msg'],
                            err_obj.WRONG_TYPE_415['status'])

        if len(request.get_json()) < 3:
            return get_resp(err_obj.MISS_ATTR_ONE_400['msg'],
                            err_obj.MISS_ATTR_ONE_400['status'])

        results = verify_jwt(request)
        if results.err is not None:
            return results.err
        content = request.get_json()
        new_boat = create_entity(
            const.BOATS,
            {'name': content['name'],
             'type': content['type'],
             'length': content['length'],
             'owner': results.payload['sub'],
             'loads': []})
        new_boat['id'] = new_boat.key.id
        new_boat['self'] = BASE_URL + '/boats/' + str(new_boat.key.id)
        return get_resp(new_boat, 201)

    elif request.method == 'GET':
        query = client.query(kind=const.BOATS)
        results = verify_jwt(request)
        if results.err is not None:
            return results.err

        q_limit = int(request.args.get('limit', '5'))
        q_offset = int(request.args.get('offset', '0'))
        query = client.query(kind=const.BOATS)
        query.add_filter('owner', '=', results.payload['sub'])
        # Get a list of at most 5 boats from datastore
        g_iterator = query.fetch(limit=q_limit, offset=q_offset)
        pages = g_iterator.pages
        boats = list(next(pages))

        # If there is another page, set next url using limit and offset
        next_url = None
        if g_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = BASE_URL + '/boats' + '?limit=' + str(
                q_limit) + '&offset=' + str(next_offset)

        # Add 'id', 'self', and convert loads list for each boat object
        for boat in boats:
            boat['id'] = boat.key.id
            # Convert any loads from ID value to dict with 'id', 'self'
            if len(boat['loads']) > 0:
                loads = construct_loads(boat['loads'])
                boat['loads'] = loads
            boat['self'] = BASE_URL + '/boats/' + str(boat.key.id)

        # Add list to dict
        resp_body = {'boats': boats}
        # Add next url to dict if not None
        if next_url:
            print("next url detected")

            resp_body['next'] = next_url

        return get_resp(resp_body, 200)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


@app.route('/boats/<id>', methods=const.METHODS)
def boat_del_get_put_patch(id):
    """"""
    if const.APP_JSON not in request.accept_mimetypes:
        return get_resp(err_obj.WRONG_ACCEPT_406['msg'],
                        err_obj.WRONG_ACCEPT_406['status'],
                        False)

    if request.method != 'POST':

        results = verify_jwt(request)
        if results.err is not None:
            return results.err
        boat = get_entity(const.BOATS, int(id))

        if boat is None:
            return get_resp(err_obj.NO_BOAT_FOUND_404['msg'],
                            err_obj.NO_BOAT_FOUND_404['status'])

        if results.payload['sub'] != boat['owner']:
            if request.method == 'DELETE':
                return get_resp(err_obj.FBD_BOAT_DELETE_403['msg'],
                                err_obj.FBD_BOAT_DELETE_403['status'])
            elif request.method == 'GET':
                return get_resp(err_obj.FBD_BOAT_READ_403['msg'],
                                err_obj.FBD_BOAT_READ_403['status'])
            elif request.method == 'PATCH' or request.method == 'PUT':
                return get_resp(err_obj.FBD_BOAT_UPDATE_403['msg'],
                                err_obj.FBD_BOAT_UPDATE_403['status'])

        if request.method == 'DELETE':
            query = client.query(kind=const.LOADS)
            query.add_filter('carrier', '=', int(id))
            loads = list(query.fetch())
            for i in range(len(loads)):
                with client.transaction():
                    loads[i]['carrier'] = None
                    client.put(loads[i])

            client.delete(boat)
            return get_resp(None, 204)

        elif request.method == 'PATCH':
            if request.mimetype != const.APP_JSON:
                return get_resp(err_obj.WRONG_TYPE_415['msg'],
                                err_obj.WRONG_TYPE_415['status'])
            keys = request.get_json().keys()
            if len(keys) < 1:
                return get_resp(err_obj.MISS_ATTR_ALL_400['msg'],
                                err_obj.MISS_ATTR_ALL_400['status'])
            with client.transaction():
                for key in keys:
                    boat[key] = request.get_json()[key]
                client.put(boat)

        elif request.method == 'PUT':
            if request.mimetype != const.APP_JSON:
                return get_resp(err_obj.WRONG_TYPE_415['msg'],
                                err_obj.WRONG_TYPE_415['status'])
            body = request.get_json()
            if len(body) < 3:
                return get_resp(err_obj.MISS_ATTR_ONE_400['msg'],
                                err_obj.MISS_ATTR_ONE_400['status'])
            with client.transaction():
                boat['name'] = body['name']
                boat['type'] = body['type']
                boat['length'] = body['length']
                client.put(boat)

        # Same block for 'GET', 'PATCH', and 'PUT'
        if len(boat['loads']) > 0:
            loads = construct_loads(boat['loads'])
            boat['loads'] = loads
        boat['id'] = boat.key.id
        boat['self'] = BASE_URL + '/boats/' + str(boat.key.id)
        return get_resp(boat, 200)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


@app.route('/boats/<boat_id>/loads/<load_id>', methods=const.METHODS)
def boats_put_remove_load(boat_id, load_id):
    """"""
    if request.method == 'PUT' or request.method == 'DELETE':

        results = verify_jwt(request)
        if results.err is not None:
            return results.err

        boat = get_entity(const.BOATS, int(boat_id))
        load = get_entity(const.LOADS, int(load_id))

        if boat is None or load is None:
            return get_resp(err_obj.NO_BOAT_LOAD_FOUND_404['msg'],
                            err_obj.NO_BOAT_LOAD_FOUND_404['status'])

        if results.payload['sub'] != boat['owner']:
            if request.method == 'DELETE':
                return get_resp(err_obj.FBD_RM_USER_BOAT_403['msg'],
                                err_obj.FBD_RM_USER_BOAT_403['status'])
            elif request.method == 'PUT':
                return get_resp(err_obj.FBD_ADD_USER_BOAT_403['msg'],
                                err_obj.FBD_ADD_USER_BOAT_403['status'])

        if request.method == 'PUT':
            if load['carrier'] is not None:
                if int(load['carrier']) != int(boat.key.id):
                    return get_resp(err_obj.FBD_LOAD_LOADED_403['msg'],
                                    err_obj.FBD_LOAD_LOADED_403['status'])
                elif int(load.key.id) in boat['loads']:
                    return get_resp(err_obj.FBD_LOAD_LOADED_403['msg'],
                                    err_obj.FBD_LOAD_LOADED_403['status'])

            with client.transaction():
                boat['loads'].append(int(load_id))
                load['carrier'] = int(boat.key.id)
                client.put(boat)
                client.put(load)
            return get_resp(None, 204)

        elif request.method == 'DELETE':
            if load['carrier'] != boat.key.id:
                return get_resp(err_obj.FBD_LOAD_DIFF_403['msg'],
                                err_obj.FBD_LOAD_DIFF_403['status'])
        # Update boat's loads and load's carrier value and put on datastore
            with client.transaction():
                boat['loads'].remove(int(load.key.id))
                load['carrier'] = None
                client.put(boat)
                client.put(load)
            return get_resp(None, 204)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


@app.route('/loads', methods=const.METHODS)
def loads_post_get():
    """"""
    if const.APP_JSON not in request.accept_mimetypes:
        return get_resp(err_obj.WRONG_ACCEPT_406['msg'],
                        err_obj.WRONG_ACCEPT_406['status'],
                        False)

    if request.method == 'POST':

        # TODO: Add authorization

        if request.mimetype != const.APP_JSON:
            return get_resp(err_obj.WRONG_TYPE_415['msg'],
                            err_obj.WRONG_TYPE_415['status'])

        if len(request.get_json()) < 3:
            return get_resp(err_obj.MISS_ATTR_ONE_400['msg'],
                            err_obj.MISS_ATTR_ONE_400['status'])

        content = request.get_json()
        new_load = create_entity(
            const.LOADS,
            {'volume': content['volume'],
             'item': content['item'],
             'creation_date': content['creation_date'],
             'carrier': None})
        new_load['id'] = new_load.key.id
        new_load['self'] = BASE_URL + '/loads/' + str(new_load.key.id)
        return get_resp(new_load, 201)

    elif request.method == 'GET':

        # TODO: Add authorization

        query = client.query(kind=const.LOADS)

        q_limit = int(request.args.get('limit', '5'))
        q_offset = int(request.args.get('offset', '0'))
        query = client.query(kind=const.LOADS)
        # Get a list of at most 5 loads from datastore
        g_iterator = query.fetch(limit=q_limit, offset=q_offset)
        pages = g_iterator.pages
        loads = list(next(pages))

        # If there is another page, set next url using limit and offset
        next_url = None
        if g_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = BASE_URL + '/loads' + '?limit=' + str(
                q_limit) + '&offset=' + str(next_offset)

        # Add 'id', 'self', and convert loads list for each load object
        for load in loads:
            load['id'] = load.key.id
            # Convert any loads from ID value to dict with 'id', 'self'
            load['self'] = BASE_URL + '/loads/' + str(load.key.id)

        # Add list to dict
        resp_body = {'loads': loads}
        # Add next url to dict if not None
        if next_url:
            resp_body['next'] = next_url

        return get_resp(loads, 200)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


@app.route('/loads/<id>', methods=const.METHODS)
def load_del_get_put_patch(id):
    """"""
    if const.APP_JSON not in request.accept_mimetypes:
        return get_resp(err_obj.WRONG_ACCEPT_406['msg'],
                        err_obj.WRONG_ACCEPT_406['status'],
                        False)

    if request.method != 'POST':

        # TODO: Add authorization

        load = get_entity(const.LOADS, int(id))

        if load is None:
            return get_resp(err_obj.NO_LOAD_FOUND_404['msg'],
                            err_obj.NO_LOAD_FOUND_404['status'])

        if request.method == 'DELETE':
            if load['carrier'] is not None:
                boat = get_entity(const.BOATS, load['carrier'])
                with client.transaction():
                    boat['loads'].remove(int(id))
                    client.put(boat)
            client.delete(load)
            return get_resp(None, 204)

        elif request.method == 'PATCH':

            if request.mimetype != const.APP_JSON:
                return get_resp(err_obj.WRONG_TYPE_415['msg'],
                                err_obj.WRONG_TYPE_415['status'])
            keys = request.get_json().keys()
            if len(keys) < 1:
                return get_resp(err_obj.MISS_ATTR_ALL_400['msg'],
                                err_obj.MISS_ATTR_ALL_400['status'])
            with client.transaction():
                for key in keys:
                    load[key] = request.get_json()[key]
                client.put(load)

        elif request.method == 'PUT':
            if request.mimetype != const.APP_JSON:
                return get_resp(err_obj.WRONG_TYPE_415['msg'],
                                err_obj.WRONG_TYPE_415['status'])
            body = request.get_json()
            if len(body) < 3:
                return get_resp(err_obj.MISS_ATTR_ONE_400['msg'],
                                err_obj.MISS_ATTR_ONE_400['status'])
            with client.transaction():
                load['volume'] = body['volume']
                load['item'] = body['item']
                load['creation_date'] = body['creation_date']
                client.put(load)

        # Same block for 'GET', 'PATCH', and 'PUT'
        load['id'] = load.key.id
        load['self'] = BASE_URL + '/boats/' + str(load.key.id)
        return get_resp(load, 200)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


if __name__ == '__main__':
    BASE_URL = const.BASE_LOCAL_URL
    app.run(host='127.0.0.1', port=8080, debug=True)
