# Error message objects containing a message and appropriate 40* status code


MISSING_ATTR_400 = {
    'msg': {'Error': 'The request object is missing at least one '
            'of the required attributes'},
    'status': 400
}

TOO_MANY_ATTR_400 = {
    'msg': {'Error': 'The request object contains too many attributes'},
    'status': 400
}

INCORRECT_ATTR_400 = {
    'msg': {'Error': 'The request object contains one or more '
            'incorrect attributes'},
    'status': 400
}

INVALID_VAL_400 = {
    'msg': {'Error': 'The request object contains one or '
            'more invalid attribute values'},
    'status': 400
}

NON_UNIQUE_NAME_403 = {
    'msg': {'Error': 'Boat name not unique and is already used'},
    'status': 403
}

NO_BOAT_FOUND_404 = {
    'msg': {'Error': 'No boat with this boat_id exists'},
    'status': 404
}

DISALLOWED_METHOD_405 = {
    'msg': {'Error': 'Method not allowed'},
    'status': 405
}

WRONG_ACCEPT_406 = {
    'msg': {'Error': 'Client Accept header not set to application/json'},
    'status': 406
}

WRONG_TYPE_415 = {
    'msg': {'Error': 'Client sent content in an unsupported MIME type'},
    'status': 415
}
