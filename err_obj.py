# Error message objects containing a message and appropriate 40* status code


MISS_ATTR_ONE_400 = {
    'msg': {'Error': 'The request object is missing at least one '
            'of the required attributes'},
    'status': 400
}

MISS_ATTR_ALL_400 = {
    'msg': {'Error': 'The request object is empty. Must update at '
            'least one attribute'},
    'status': 400
}

FBD_BOAT_READ_403 = {
    'msg': {'Error': 'User is not allowed to view boats owned by '
            'someone else'},
    'status': 403
}

FBD_BOAT_UPDATE_403 = {
    'msg': {'Error': 'User is not allowed to update boats owned by '
            'someone else'},
    'status': 403
}

FBD_BOAT_DELETE_403 = {
    'msg': {'Error': 'User is not allowed to delete boats owned by '
            'someone else'},
    'status': 403
}

FBD_LOAD_LOADED_403 = {
    'msg': {'Error': 'Load is already loaded on a boat'},
    'status': 403
}

FBD_LOAD_DIFF_403 = {
    'msg': {'Error': 'Load is not on this boat'},
    'status': 403
}

FBD_ADD_USER_BOAT_403 = {
    'msg': {'Error': 'Cannot add load to a different user boat'},
    'status': 403
}

FBD_RM_USER_BOAT_403 = {
    'msg': {'Error': 'Cannot remove load from a different user boat'},
    'status': 403
}

NO_BOAT_FOUND_404 = {
    'msg': {'Error': 'No boat with this boat_id exists'},
    'status': 404
}

NO_LOAD_FOUND_404 = {
    'msg': {'Error': 'No load with this load_id exists'},
    'status': 404
}

NO_BOAT_LOAD_FOUND_404 = {
    'msg': {'Error': 'The specified boat and/or load does not exist'},
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
