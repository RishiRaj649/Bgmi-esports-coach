#!/usr/bin/env python3
import os
import sys
import subprocess
import webbrowser
import time
import threading
import signal
import shutil

# Configuration
BACKEND_PORT = 8000
FRONTEND_PORT = 5000

def run_backend():
    """Run the FastAPI backend server"""
    print("Starting backend server...")
    original_dir = os.getcwd()
    
    # Make sure backend directory exists
    if not os.path.exists("backend"):
        print("Error: Backend directory not found!")
        return
        
    os.chdir("backend")
    print(f"Changed to directory: {os.getcwd()}")
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except Exception as e:
        print(f"Error running backend: {str(e)}")
    finally:
        os.chdir(original_dir)

def run_frontend():
    """Run the React frontend development server"""
    print("Starting frontend server...")
    original_dir = os.getcwd()
    
    # Check if frontend directory exists
    if not os.path.exists("frontend"):
        print("Frontend directory not found! Creating minimal frontend...")
        os.makedirs("frontend/public", exist_ok=True)
        
        # Create a minimal index.html file
        with open("frontend/public/index.html", "w") as f:
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
        }
        button:hover {
            background-color: #7c4dff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BGMI Esports Coach</h1>
        <div class="status">
            <h2>Status: Ready</h2>
            <p>Backend API is running on port 8000</p>
        </div>
        <p>
            This app will analyze your BGMI gameplay and provide personalized coaching tips to improve your skills.
        </p>
        <button id="startBtn">Start Recording</button>
    </div>

    <script>
        document.getElementById('startBtn').addEventListener('click', function() {
            alert('Recording functionality is being implemented. Check back soon!');
        });
    </script>
</body>
</html>""")
    
    try:
        # Change to frontend directory
        try:
            os.chdir("frontend")
            print(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            print(f"Error changing to frontend directory: {str(e)}")
            return
            
        # Ensure we're serving from the correct directory
        if os.path.exists("build"):
            # Serve from build if it exists
            serve_dir = "build"
        else:
            # Otherwise serve from public which has the basic HTML
            serve_dir = "public"
        
        print(f"Serving frontend from directory: {serve_dir}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Contents of {serve_dir}: {os.listdir(serve_dir)}")
            
        # Use a simple HTTP server to serve the frontend
        subprocess.run([
            sys.executable, "-m", "http.server", str(FRONTEND_PORT),
            "--bind", "0.0.0.0", "--directory", serve_dir
        ])
    except Exception as e:
        print(f"Error in frontend server: {str(e)}")
    finally:
        try:
            os.chdir(original_dir)
        except:
            pass

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(2)  # Wait for servers to start
    webbrowser.open(f"http://localhost:{FRONTEND_PORT}")

def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully shut down"""
    print("\nShutting down BGMI Esports Coach...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("Starting BGMI Esports Coach...")
    
    # Check if data directory exists, create if it doesn't
    if not os.path.exists("data"):
        os.makedirs("data/matches", exist_ok=True)
        print("Created data directory")
    
    # Start the backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    print(f"Backend starting on http://localhost:{BACKEND_PORT}")
    
    # Start the frontend in a separate thread
    frontend_thread = threading.Thread(target=run_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()
    print(f"Frontend starting on http://localhost:{FRONTEND_PORT}")
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("BGMI Esports Coach is running!")
    print("Press Ctrl+C to quit")
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down BGMI Esports Coach...")
        sys.exit(0)
