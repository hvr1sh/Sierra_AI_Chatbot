from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        data = {
            "message": "Hello, world!",
            "status": "success"
        }

        json_bytes = json.dumps(data).encode("utf-8")
        self.wfile.write(json_bytes)