import json
from wsgiref.simple_server import make_server

tasks = []
next_id = 1

def response(start_response, status, body):
    data = json.dumps(body).encode('utf-8')
    start_response(status, [('Content-Type', 'application/json'), ('Content-Length', str(len(data)))])
    return [data]

def read_json_body(environ):
    length = int(environ.get('CONTENT_LENGTH', 0))
    raw_body = environ['wsgi.input'].read(length)
    if not raw_body:
        return {}
    return json.loads(raw_body.decode('utf-8'))