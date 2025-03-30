from flask import Flask, send_file, jsonify, request
import json
import os
import time
import uuid
from pyngrok import ngrok
import atexit

# Initialize Flask app
app = Flask(__name__)

# Data storage for matches
matches_dir = "data/standalone_matches"
os.makedirs(matches_dir, exist_ok=True)

# Store active matches
active_matches = {}

class SimpleAnalyzer:
    def __init__(self, match_id, game_mode, map_name):
        self.match_id = match_id
        self.game_mode = game_mode
        self.map_name = map_name
        self.metrics = {}
        self.recommendations = []
        self.summary = ""
        
    def analyze(self):
        """Analyze the gameplay (simulation)"""
        # Simulate metrics for aim
        self.metrics["aim"] = {
            "accuracy": self._simulate_score(0.5, 0.95),
            "reaction_time": self._simulate_score(0.4, 0.9),
            "recoil_control": self._simulate_score(0.3, 0.85),
            "headshot_percentage": self._simulate_score(0.1, 0.6)
        }
        
        # Simulate metrics for positioning
        self.metrics["positioning"] = {
            "cover_usage": self._simulate_score(0.4, 0.9),
            "movement_efficiency": self._simulate_score(0.3, 0.85),
            "zone_awareness": self._simulate_score(0.5, 0.95),
            "rotation_timing": self._simulate_score(0.4, 0.9)
        }
        
        # Simulate metrics for decision making
        self.metrics["decision_making"] = {
            "engagement_choices": self._simulate_score(0.3, 0.8),
            "item_management": self._simulate_score(0.4, 0.9),
            "tactical_planning": self._simulate_score(0.3, 0.85),
            "team_coordination": self._simulate_score(0.2, 0.7)
        }
        
        # Generate recommendations based on metrics
        self._generate_recommendations()
        
        # Generate overall summary
        self._generate_summary()
        
        # Prepare and return analysis results
        result = {
            "match_id": self.match_id,
            "analysis_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metrics": self.metrics,
            "recommendations": self.recommendations,
            "summary": self.summary
        }
        
        # Save analysis to a file
        match_dir = os.path.join(matches_dir, self.match_id)
        os.makedirs(match_dir, exist_ok=True)
        with open(os.path.join(match_dir, "analysis.json"), "w") as f:
            json.dump(result, f, indent=2)
            
        return result
    
    def _simulate_score(self, min_val, max_val):
        """Simulate a performance score"""
        import random
        return round(random.uniform(min_val, max_val), 2)
    
    def _generate_recommendations(self):
        """Generate recommendations based on metrics"""
        # Check aim metrics
        if self.metrics["aim"]["accuracy"] < 0.7:
            self.recommendations.append({
                "category": "aim",
                "title": "Improve Aim Accuracy",
                "description": "Practice target tracking in training mode for 15 minutes daily.",
                "priority": "high"
            })
        
        if self.metrics["aim"]["recoil_control"] < 0.6:
            self.recommendations.append({
                "category": "aim",
                "title": "Enhance Recoil Control",
                "description": "Practice spray patterns with AR and SMG weapons on static targets.",
                "priority": "medium"
            })
            
        # Check positioning metrics
        if self.metrics["positioning"]["cover_usage"] < 0.6:
            self.recommendations.append({
                "category": "positioning",
                "title": "Utilize Cover Better",
                "description": "Always prioritize moving between cover points rather than open areas.",
                "priority": "high"
            })
            
        if self.metrics["positioning"]["zone_awareness"] < 0.7:
            self.recommendations.append({
                "category": "positioning",
                "title": "Improve Zone Management",
                "description": "Plan your movements based on zone predictions earlier in the match.",
                "priority": "medium"
            })
            
        # Check decision making metrics
        if self.metrics["decision_making"]["engagement_choices"] < 0.6:
            self.recommendations.append({
                "category": "decision_making",
                "title": "Better Engagement Decisions",
                "description": "Only take fights when you have a positional or equipment advantage.",
                "priority": "high"
            })
            
        if self.metrics["decision_making"]["item_management"] < 0.7:
            self.recommendations.append({
                "category": "decision_making",
                "title": "Optimize Item Management",
                "description": "Prioritize picking up essential healing items and ammo before looting other items.",
                "priority": "low"
            })
            
        # Add general recommendations
        self.recommendations.append({
            "category": "general",
            "title": "Consistent Practice Schedule",
            "description": "Set aside 30 minutes daily for targeted practice in areas needing improvement.",
            "priority": "medium"
        })
        
    def _generate_summary(self):
        """Generate an overall summary"""
        # Calculate average scores
        aim_avg = sum(self.metrics["aim"].values()) / len(self.metrics["aim"])
        positioning_avg = sum(self.metrics["positioning"].values()) / len(self.metrics["positioning"])
        decision_avg = sum(self.metrics["decision_making"].values()) / len(self.metrics["decision_making"])
        
        # Determine strongest and weakest areas
        averages = {
            "Aim": aim_avg,
            "Positioning": positioning_avg,
            "Decision Making": decision_avg
        }
        
        strongest = max(averages, key=averages.get)
        weakest = min(averages, key=averages.get)
        
        # Generate the summary
        self.summary = f"Your gameplay shows {strongest} as your strongest skill area. Focus on improving your {weakest} which needs the most attention. "
        
        # Add specific advice based on the map
        if self.game_mode.lower() == "battle royale":
            self.summary += "For Battle Royale, prioritize positioning and zone awareness over aggressive engagements. "
        elif self.game_mode.lower() == "team deathmatch":
            self.summary += "In Team Deathmatch, work on quicker reaction times and maintaining high ground control. "
            
        # Add map-specific advice
        if "erangel" in self.map_name.lower():
            self.summary += "On Erangel, use natural terrain for cover during zone rotations."
        elif "miramar" in self.map_name.lower():
            self.summary += "On Miramar, high ground control is essential for spotting enemies at long distances."
        elif "sanhok" in self.map_name.lower():
            self.summary += "On Sanhok, quick reflexes and close-combat skills are more important than long-range engagements."

# Routes
@app.route('/')
def index():
    return send_file('static_demo.html')

@app.route('/status')
def status():
    return jsonify({
        "status": "ok",
        "active_matches": len(active_matches)
    })

@app.route('/api/simulate-match', methods=['POST'])
def simulate_match():
    """Simulate a match analysis for demo purposes"""
    data = request.json or {}
    game_mode = data.get('game_mode', 'Battle Royale')
    map_name = data.get('map_name', 'Erangel')
    
    # Generate a unique match ID
    match_id = f"demo_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    
    # Create an analyzer and run analysis
    analyzer = SimpleAnalyzer(match_id, game_mode, map_name)
    analysis = analyzer.analyze()
    
    # Store match in active matches
    active_matches[match_id] = {
        "id": match_id,
        "game_mode": game_mode,
        "map_name": map_name,
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "completed"
    }
    
    return jsonify({
        "match_id": match_id,
        "status": "completed",
        "message": "Match analysis completed"
    })

@app.route('/api/analysis/<match_id>')
def get_analysis(match_id):
    """Get analysis results for a match"""
    analysis_file = os.path.join(matches_dir, match_id, "analysis.json")
    
    if not os.path.exists(analysis_file):
        return jsonify({
            "error": "Analysis not found",
            "match_id": match_id
        }), 404
        
    with open(analysis_file, 'r') as f:
        analysis = json.load(f)
        
    return jsonify(analysis)

@app.route('/api/matches/clear', methods=['POST'])
def clear_matches():
    """Clear all match data"""
    active_matches.clear()
    return jsonify({"status": "success", "message": "All matches cleared"})

@app.route('/api/matches')
def list_matches():
    """List all matches"""
    return jsonify(list(active_matches.values()))

def cleanup():
    # Close the ngrok tunnel when the script exits
    ngrok.kill()

# Set up ngrok tunnel
def setup_ngrok():
    # Open an HTTP tunnel on the default port
    public_url = ngrok.connect(5000).public_url
    print(f"* Ngrok tunnel established at: {public_url}")
    app.config["BASE_URL"] = public_url
    return public_url

if __name__ == '__main__':
    # Register cleanup function to run on exit
    atexit.register(cleanup)
    
    # Set up ngrok tunnel
    ngrok_url = setup_ngrok()
    print(f"* Access the application externally at: {ngrok_url}")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)