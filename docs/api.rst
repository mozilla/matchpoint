================================
UP Rules Server API (DRAFT) v0.1
================================

Overview
========

The Client periodically needs to update and refresh its UserProfile
ruleset (a list of Rules) from the Server. This describes the API
endpoints implemented by the Server.

While the transport mechanism is HTTP, this is not necessarily a
"RESTful" API.  We will make use of HTTP headers where appropriate but
don't read too much into 
the verbs.


Notes
-----

* All API endpoints are prefixed with a version number. For this draft,
  that version is "v0" but for release it will be "v1" and in the future,
  if necessary, a monotonically increasing integer.
* This is a draft for feedback, not final.


Get all/updated Rules for a Namespace
=====================================

**Request**::

    GET /api/v0/rules/<namespace>
    If-Modified-Since: <date>

In response to any 2xx or 3xx response, the client should save the
current date as a "last updated" to send back as ``If-Modified-Since``.
If no ``If-Modified-Since`` header is sent, the response will be the
complete ruleset for that namespace.

It is possible that not all namespaces can be requested this way. In
that case, we will return a distinct response code.

**Responses**:

In any case, if the Server responds with a ``Retry-After``, the Client
should respect this value.

If we're sending the whole namespace, the Server will send ``200 OK``
and a JSON response. If there are updates, the Server will send ``206
Partial Content`` and a JSON response. Otherwise, these responses are
identical::

    HTTP/1.1 200 OK
    Content-Length: <int>
    Content-Type: application/json
    Last-Modified: <date>

    {
        "name": {IFR + integer ID},
        ...
    }

Each entry in the ``rules`` object will be a complete IFR (pending any
change in this definition) representation of the Rule along with an
integer ID field, or ``null``. The Client should replace its IFR
definition of a Rule with the new one, or delete it if the value is
``null``. If the Client has a Rule that is not included in the response,
the Client should assume the Rule has not changed in the case of a 206.
In the case of a 200, assume this is the complete ruleset for the
namespace and any missing Rules do not exist.

The ``Last-Modified`` date should be stored and used for
``If-Modified-Since`` on subsequent requests. (It will be set to the
modified date of the most recently updated rule in the response.)

The integer ID will be an ``update_id`` key at the same level as
``threshold`` and ``duration``.

If there are no updates, the Server will send ``304 Not Modified`` and
no response body::

    HTTP/1.1 304 Not Modified
    Content-Length: 0

If the Client has somehow malformed the request, the Server will send
``400 Bad Request`` and no response body::

    HTTP/1.1 400 Bad Request
    Content-Length: 0

If the namespace is unknown or cannot be requested this way, the Server
will send ``404 Not Found`` and no response body::

    HTTP/1.1 404 Not Found
    Content-Length: 0

If the namespace has been deleted entirely, the Server will send ``410
Gone`` and no response body::

    HTTP/1.1 410 Gone
    Content-Length: 0

In the event of any 5xx response code, the Client should wait and try
again (respecting ``Retry-After`` if included).


Get updates of specific Rules
=============================

**Request**::

To ask about specific Rules, the Client should ``POST`` a request with a
JSON body including a count of the number of Rules being requested and a
list of the Rules identified by namespace and name, or by integer ID.

::

    POST /api/v0/rules
    If-Modified-Since: <date>

    {
        "count": X (number of requested rules),
        "rules": [
            "<namespace>/<rule>",
            123,
            ...
        ]
    }

If an ``If-Modified-Since`` header is included, only Rules changed or
deleted since ``<date>`` will be returned.

**Reponse**::

Responses and status codes are identical to the GET API above. The
client should store the value of ``Last-Modified`` for subsequent
requests.
