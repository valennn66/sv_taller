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

def app(environ, start_response):
    global next_id
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    if path == '/tasks':
        if method == 'GET':
            return response(start_response, '200 OK', tasks)

        if method == 'POST':
            new_task = read_json_body(environ)
            new_task['id'] = next_id
            next_id += 1
            tasks.append(new_task)
            return response(start_response, '201 Created', new_task)

        return response(start_response, '405 Method Not Allowed', {'error': 'Method not allowed'})

    if path.startswith('/tasks/'):
        parts = path.split('/')

        if len(parts) == 3 and parts[2].isdigit():
            task_id = int(parts[2])

            found_task = None
            for task in tasks:
                if task['id'] == task_id:
                    found_task = task
                    break
            
            if not found_task:
                return response(start_response, '404 Not Found', {'error': 'Task not found'})

            if method == 'GET':
                return response(start_response, '200 OK', found_task)

            if method == 'PATCH':
                update_data = read_json_body(environ)
                for key, value in update_data.items():
                    found_task[key] = value
                return response(start_response, '200 OK', found_task)

            if method == 'DELETE':
                tasks.remove(found_task)
                return response(start_response, '200 OK', found_task)

            return response(start_response, '405 Method Not Allowed', {'error': 'Method not allowed'})
        
        return response(start_response, '404 Not Found', {'error': 'Not found'})

    return response(start_response, '404 Not Found', {'error': 'Not found'})

if __name__ == "__main__":
    port = 9292
    with make_server("0.0.0.0", port, app) as server:
        print(f"Serving on http://localhost:{port}")
        server.serve_forever()