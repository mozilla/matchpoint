from __future__ import absolute_import

import json

from flask import jsonify, request, make_response

from matchpoint import app
from matchpoint.models import Namespace


JSON = 'application/json'


@app.route('/api/v1/<name>', methods=['GET', 'HEAD'])
def get_namespace(name):
    ns = Namespace.query().filter(Namespace.name == name).first()

    if ns is None:
        return '', 404, {'Content-Type': JSON}

    fmt = lambda s: '/'.join((ns.name, s))
    interests = dict(((fmt(i.name), i.current.to_dict()) for i in ns.interests))

    headers = {
        'Content-Type': JSON,
        'Last-Modified': ns.modified.isoformat() + 'Z',
    }

    return json.dumps(interests), 200, headers
