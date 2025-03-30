import http.server
import socketserver

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

if __name__ == "__main__":
    PORT = 5000
    
    print(f"Starting basic server on port {PORT}...")
    
    # Create the HTTP server
    Handler = BasicHTTPRequestHandler
    httpd = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
    
    print(f"Server is running at http://0.0.0.0:{PORT}")
    
    # Start the server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()