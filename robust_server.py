import http.server
import socketserver
import time
import socket
import os
import signal
import sys

# Very simple HTML page
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>BGMI Coach Basic Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #6200ea;
        }
        .status {
            padding: 10px;
            background-color: #e0f7fa;
            border-radius: 4px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BGMI Esports Coach Basic Demo</h1>
        
        <div class="status">
            <h2>Server Status: ONLINE</h2>
            <p>Basic web server is running correctly!</p>
        </div>
        
        <p>This is a minimal demo of the BGMI Esports Coach application.</p>
        <p>The full version will include:</p>
        <ul>
            <li>Gameplay recording and analysis</li>
            <li>Performance metrics tracking</li>
            <li>Personalized coaching recommendations</li>
        </ul>
    </div>
</body>
</html>
"""

# Configuration
PORT = 5000
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

def signal_handler(sig, frame):
    print("\nShutting down the server...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class BasicHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Respond with our simple HTML
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode())
        
    def log_message(self, format, *args):
        # Simple logging
        print("[Server]", format % args)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_port_to_be_free(port, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Wait for a port to become free"""
    for attempt in range(max_retries):
        if not is_port_in_use(port):
            return True
            
        print(f"Port {port} is still in use. Waiting {delay} seconds... (Attempt {attempt+1}/{max_retries})")
        time.sleep(delay)
    
    return False

if __name__ == "__main__":    
    print(f"Starting robust server on port {PORT}...")
    
    # First check if port is in use
    if is_port_in_use(PORT):
        print(f"Port {PORT} is already in use. Waiting for it to be free...")
        if not wait_for_port_to_be_free(PORT):
            print(f"Port {PORT} did not become free after {MAX_RETRIES} attempts.")
            print("Please manually kill any processes using port 5000")
            sys.exit(1)
    
    # Create the HTTP server with allow_reuse_address to help with "Address already in use" errors
    socketserver.TCPServer.allow_reuse_address = True
    
    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), BasicHTTPRequestHandler) as httpd:
            print(f"Server is running at http://0.0.0.0:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        print(f"Error starting server: {e}")
        print("If the port is already in use, try again in a few moments or restart the environment.")
        sys.exit(1)