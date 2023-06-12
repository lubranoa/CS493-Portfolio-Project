import const
import err_obj

from flask import Blueprint, request
from main import BASE_URL, client
from main import verify_jwt, create_entity, get_entity, get_resp

bp = Blueprint('loads', __name__, url_prefix='/loads')


@bp.route('', methods=['POST', 'GET'])
def loads_post_get():
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
    if const.APP_JSON not in request.accept_mimetypes:
        return get_resp(err_obj.WRONG_ACCEPT_406['msg'],
                        err_obj.WRONG_ACCEPT_406['status'],
                        False)

    if request.method == 'POST':
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
        new_boat['self'] = BASE_URL + bp.url_prefix + str(new_boat.key.id)
        return get_resp(new_boat, 201)

    elif request.method == 'GET':
        query = client.query(kind=const.BOATS)
        results = verify_jwt(request)
        if results.err is not None:
            return results.err
        else:
            query.add_filter('owner', '=', results.payload['sub'])
            boats = list(query.fetch())
            for boat in boats:
                boat['id'] = boat.key.id
                boat['self'] = BASE_URL + 'boats/' + str(boat.key.id)
            return get_resp(boats, 200)

    else:
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])


@bp.route('/loads/<id>', methods=['DELETE'])
def loads_delete(id):
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
    if const.APP_JSON not in request.accept_mimetypes:
        return get_resp(err_obj.WRONG_ACCEPT_406['msg'],
                        err_obj.WRONG_ACCEPT_406['status'],
                        False)

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
        return get_resp(err_obj.DISALLOWED_METHOD_405['msg'],
                        err_obj.DISALLOWED_METHOD_405['status'])
