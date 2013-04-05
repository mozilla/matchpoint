from __future__ import absolute_import

import json

from flask import jsonify, request, make_response
from mongoalchemy.session import Session

from matchpoint import app
from matchpoint.models import Namespace


@app.route('/api/v1/<name>', methods=['GET', 'HEAD'])
def get_namespace(name):
    s = Session.connect('default')  # XXX
    ns = s.query(Namespace).filter(Namespace.name == name).first()

    if ns is None:
        return '', 404, {'Content-Type': 'application/json'}

    fmt = lambda s: '/'.join((ns.name, s))
    interests = dict(((fmt(i.name), i.current.to_dict()) for i in ns.interests))

    headers = {
        'Content-Type': 'application/json',
        'Last-Modified': ns.modified.isoformat() + 'Z',
    }

    return json.dumps(interests), 200, headers
