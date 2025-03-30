# BGMI Esports Coach

An AI-powered analytics platform for BGMI (Battlegrounds Mobile India) players that provides personalized coaching and improvement tips based on gameplay analysis.

## Features

- **Real-time Gameplay Analysis**: Captures and analyzes gameplay in real-time
- **Performance Metrics**: Measures key metrics across aim, positioning, and decision-making
- **Personalized Recommendations**: Provides customized improvement suggestions
- **Visual Dashboard**: Interactive UI to explore performance data
- **Low Performance Impact**: Designed to run in the background without affecting gameplay

## Deployment Options

This project can be deployed on several platforms:

### Railway

1. Create a new project on Railway
2. Link this repository
3. Railway will automatically detect and deploy the app using the `railway.toml` configuration

### Render

1. Create a new Web Service on Render
2. Link this repository
3. Render will use the `render.yaml` configuration to deploy the app

### Heroku

1. Create a new app on Heroku
2. Link this repository
3. The included `Procfile` will instruct Heroku on how to run the application

## Deploying Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/bgmi-esports-coach.git
cd bgmi-esports-coach

# Install dependencies
pip install flask pyngrok opencv-python pillow numpy mss

# Run the application
python dashboard_server.py
```

Then visit `http://localhost:5000` in your browser.

## Architecture

The application consists of three main components:

1. **Screen Capture Module**: Captures gameplay footage with minimal performance impact
2. **Analysis Engine**: Processes footage to extract gameplay metrics
3. **Coaching Interface**: Displays insights and recommendations through a web dashboard

## Technologies Used

- Python (Flask for web server)
- OpenCV for image analysis
- Lightweight screen capture using MSS
- Chart.js for visualization
- Bootstrap for responsive UI

## Future Development

- ML-based weapon detection and recoil analysis
- Team coordination metrics
- Comparative analysis with pro players
- Mobile app integration