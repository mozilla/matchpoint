from __future__ import absolute_import

import json
from datetime import datetime
from functools import wraps

from flask import jsonify, request, make_response

from matchpoint import app
from matchpoint.models import Namespace


JSON = 'application/json'


# TODO: Move.
def jsonify(f):
    @wraps(f)
    def _wrapped(*a, **kw):
        ret = f(*a, **kw)
        if isinstance(ret, tuple):
            if len(ret) == 2:
                data, status = ret
                headers = {}
            elif len(ret) == 3:
                data, status, headers = ret
            else:
                data = ret
                status = 200
                headers = {}
        else:
            data = ret
            status = 200
            headers = {}
        content = json.dumps(data)
        headers['Content-Type'] = JSON
        headers['Content-Length'] = len(content)
        return content, status, headers
    return _wrapped


@app.route('/api/v1/<name>', methods=['GET', 'HEAD'])
@jsonify
def get_namespace(name):
    ns = Namespace.query().filter(Namespace.name == name).first()

    if ns is None:
        return None, 404

    total_interests = len(ns.interests)
    since = request.if_modified_since
    if since is None:
        since = datetime.min

    fmt = lambda s: '/'.join((ns.name, s))
    interests = dict(((fmt(i.name), i.current.to_dict()) for i
                      in ns.interests if
                      i.modified.replace(microsecond=0) > since))

    matched_interests = len(interests)

    if matched_interests == 0:
        return {}, 304

    if matched_interests < total_interests:
        status = 206
    else:
        status = 200

    headers = {
        'Last-Modified': ns.modified.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    }

    return interests, status, headers
