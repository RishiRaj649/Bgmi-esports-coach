from flask import Flask, render_template_string

app = Flask(__name__)

# Simple HTML template with basic styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BGMI Coach Demo</title>
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
        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
            background-color: #f9f9f9;
        }
        button {
            background-color: #6200ea;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BGMI Esports Coach Demo</h1>
        <p>Welcome to the BGMI Esports Coach demo. This application will help you improve your gameplay skills.</p>
        
        <div class="card">
            <h2>Demo Features</h2>
            <ul>
                <li>Record gameplay footage</li>
                <li>Analyze player performance</li>
                <li>Provide personalized recommendations</li>
            </ul>
            <button onclick="alert('This is a demo. Recording functionality will be implemented soon.')">Start Demo</button>
        </div>
        
        <div class="card">
            <h2>Server Status</h2>
            <p>✅ Server is running correctly</p>
            <p>✅ Application is ready for development</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return {"status": "healthy", "message": "Server is running correctly"}

if __name__ == '__main__':
    print("Starting BGMI Coach Demo App...")
    app.run(host='0.0.0.0', port=5000, debug=True)