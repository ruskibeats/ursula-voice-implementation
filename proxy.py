from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        # Print the received payload with more detail
        print("\n=== Received Webhook Payload ===")
        print("Headers:", self.headers)
        print("\nRaw Body:", body.decode('utf-8'))
        try:
            json_body = json.loads(body.decode('utf-8'))
            print("\nJSON Body:", json.dumps(json_body, indent=2))
            print("\nAvailable fields:", list(json_body.keys()))
        except:
            print("\nNot valid JSON")
        print("===============================\n")
        
        # Just send 200 OK response without forwarding
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())

httpd = HTTPServer(('', 8081), ProxyHTTPRequestHandler)
print("Proxy server running on port 8081")
httpd.serve_forever() 