#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys
import time
import socket
import signal

# Configuration
PORT = 5000
DIRECTORY = "."  # Serve from root directory
MAX_RETRIES = 5
RETRY_DELAY = 2  # seconds

def signal_handler(sig, frame):
    print("\nShutting down BGMI Esports Coach server...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create all required directories
if not os.path.exists("data"):
    os.makedirs("data/matches", exist_ok=True)
    print("Created data directory")

# Create a minimal HTML file if frontend directory doesn't exist
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY, exist_ok=True)
    print(f"Created {DIRECTORY} directory")
    
    # Create a minimal index.html file
    with open(f"{DIRECTORY}/index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BGMI Esports Coach</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
            color: #333;
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
            padding: 15px;
            background-color: #e0f7fa;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        button {
            background-color: #6200ea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin-right: 10px;
        }
        button:hover {
            background-color: #7c4dff;
        }
        .features {
            margin-top: 30px;
        }
        .feature {
            background-color: #f5f5f5;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }
        .feature h3 {
            margin-top: 0;
            color: #6200ea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BGMI Esports Coach</h1>
        <div class="status">
            <h2>Status: Ready</h2>
            <p>BGMI Esports Coach is running on port 5000</p>
        </div>
        <p>
            This app will analyze your BGMI gameplay and provide personalized coaching tips to improve your skills.
        </p>
        <div>
            <button id="startBtn">Start Recording</button>
            <button id="viewMatchesBtn">View Past Matches</button>
        </div>
        
        <div class="features">
            <h2>Features</h2>
            <div class="feature">
                <h3>Gameplay Analysis</h3>
                <p>Records your gameplay and analyzes key performance metrics to identify strengths and weaknesses.</p>
            </div>
            <div class="feature">
                <h3>Personalized Coaching</h3>
                <p>Receive tailored recommendations to improve your aim, positioning, and decision-making.</p>
            </div>
            <div class="feature">
                <h3>Performance Tracking</h3>
                <p>Track your progress over time and see how your skills improve with practice.</p>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('startBtn').addEventListener('click', function() {
            alert('Recording functionality is being implemented. Check back soon!');
        });
        
        document.getElementById('viewMatchesBtn').addEventListener('click', function() {
            alert('Match history viewing is being implemented. Check back soon!');
        });
    </script>
</body>
</html>""")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        print(f"[Web Server] {format % args}")
        
    def do_GET(self):
        # Special handling for API requests
        if self.path.startswith('/api/'):
            self.send_response(501)  # Not Implemented
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes('{"error": "API endpoint not implemented yet"}', 'utf-8'))
            return
        
        # For all other paths, use the default handler
        return super().do_GET()

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

# Main server startup with retry logic
def start_server():
    # First, wait for port to be free if it's in use
    if is_port_in_use(PORT):
        print(f"Port {PORT} is currently in use.")
        if not wait_for_port_to_be_free(PORT):
            print(f"Port {PORT} did not become free after {MAX_RETRIES} attempts.")
            print("Trying to force server to start anyway...")
    
    # Try to start the server with multiple attempts
    for attempt in range(MAX_RETRIES):
        try:
            # Use allow_reuse_address to help with "Address already in use" errors
            socketserver.TCPServer.allow_reuse_address = True
            
            with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
                print(f"BGMI Esports Coach server running at http://0.0.0.0:{PORT}")
                print(f"Serving files from {DIRECTORY}")
                httpd.serve_forever()
                
            # If we reach here, the server has shut down gracefully
            return True
        except OSError as e:
            print(f"Error starting server (attempt {attempt+1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("Maximum retry attempts reached. Server could not be started.")
                return False

if __name__ == "__main__":
    start_server()