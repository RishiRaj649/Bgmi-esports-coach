from flask import Flask, jsonify, request, render_template_string
import os
import json
import uuid
import random
import time
from datetime import datetime

# Import from backend modules
from backend.analyzer import GameplayAnalyzer

app = Flask(__name__)

# In-memory storage for demo
MATCHES = {}
DATA_DIR = "data/matches"
os.makedirs(DATA_DIR, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BGMI Coach Demo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: #f8f9fa; 
            color: #333; 
        }
        .container { 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        header {
            background: #6200ea;
            color: white;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        header h1 {
            margin: 0;
        }
        .card { 
            background: white; 
            border-radius: 8px; 
            padding: 20px; 
            margin-bottom: 20px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .stat-box {
            background: #f2f2f2;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }
        .stat-box h3 {
            margin-top: 0;
            font-size: 14px;
            text-transform: uppercase;
            color: #666;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #6200ea;
            margin: 10px 0;
        }
        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 5px;
        }
        .badge-success { background: #28a745; color: white; }
        .badge-warning { background: #ffc107; color: black; }
        .badge-danger { background: #dc3545; color: white; }
        .badge-primary { background: #6200ea; color: white; }
        .badge-info { background: #17a2b8; color: white; }
        
        .recommendations {
            margin-top: 20px;
        }
        .recommendation {
            background: #f8f9fa;
            border-left: 4px solid #6200ea;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 0 4px 4px 0;
        }
        .recommendation.high {
            border-left-color: #dc3545;
        }
        .recommendation.medium {
            border-left-color: #ffc107;
        }
        .recommendation.low {
            border-left-color: #28a745;
        }
        .recommendation h4 {
            margin-top: 0;
            display: flex;
            align-items: center;
        }
        .recommendation p {
            margin-bottom: 0;
            color: #666;
        }
        
        button {
            background: #6200ea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        button:hover {
            background: #5000ca;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .tabs {
            display: flex;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 3px solid transparent;
        }
        .tab.active {
            border-bottom-color: #6200ea;
            font-weight: bold;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        
        .summary {
            white-space: pre-line;
            line-height: 1.5;
        }
        
        .actions {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .charts {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .chart {
            background: white;
            padding: 15px;
            border-radius: 8px;
            min-height: 300px;
        }
        
        @media (max-width: 768px) {
            .stat-grid {
                grid-template-columns: 1fr 1fr;
            }
            .charts {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>BGMI Esports Coach</h1>
        </div>
    </header>
    
    <div class="container">
        <div class="actions">
            <button id="simulateMatchBtn">Simulate Match Analysis</button>
            <button id="clearMatchesBtn">Clear All Matches</button>
        </div>
        
        <div class="card" id="matchStatus">
            <h2>Demo Status</h2>
            <p>Use the "Simulate Match Analysis" button to generate analysis data for a demo match.</p>
        </div>
        
        <div class="card" id="dashboard">
            <div class="tabs">
                <div class="tab active" data-tab="overview">Overview</div>
                <div class="tab" data-tab="aim">Aim Analysis</div>
                <div class="tab" data-tab="positioning">Positioning</div>
                <div class="tab" data-tab="decisions">Decision Making</div>
                <div class="tab" data-tab="recommendations">Recommendations</div>
            </div>
            
            <div class="tab-content active" id="overview-tab">
                <h2>Performance Overview</h2>
                <div id="overview-content">
                    <p>No match analysis data available yet. Please simulate a match first.</p>
                </div>
            </div>
            
            <div class="tab-content" id="aim-tab">
                <h2>Aim Analysis</h2>
                <div id="aim-content">
                    <p>No aim analysis data available yet. Please simulate a match first.</p>
                </div>
            </div>
            
            <div class="tab-content" id="positioning-tab">
                <h2>Positioning Analysis</h2>
                <div id="positioning-content">
                    <p>No positioning analysis data available yet. Please simulate a match first.</p>
                </div>
            </div>
            
            <div class="tab-content" id="decisions-tab">
                <h2>Decision Making Analysis</h2>
                <div id="decisions-content">
                    <p>No decision making analysis data available yet. Please simulate a match first.</p>
                </div>
            </div>
            
            <div class="tab-content" id="recommendations-tab">
                <h2>Improvement Recommendations</h2>
                <div id="recommendations-content">
                    <p>No recommendations available yet. Please simulate a match first.</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Tab navigation
            document.querySelectorAll('.tab').forEach(tab => {
                tab.addEventListener('click', function() {
                    // Remove active class from all tabs and content
                    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                    
                    // Add active class to clicked tab
                    this.classList.add('active');
                    
                    // Show corresponding content
                    const tabId = this.getAttribute('data-tab');
                    document.getElementById(tabId + '-tab').classList.add('active');
                });
            });
            
            // Simulate match button
            document.getElementById('simulateMatchBtn').addEventListener('click', async function() {
                this.disabled = true;
                this.textContent = 'Analyzing...';
                
                try {
                    const response = await fetch('/api/simulate-match', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            game_mode: 'Squad',
                            map_name: 'Erangel'
                        })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        document.getElementById('matchStatus').innerHTML = `
                            <h2>Match Analysis Complete</h2>
                            <p>Analysis generated for match ID: ${result.match_id}</p>
                            <p>Overall score: <b>${Math.round(result.overall_score * 100) / 100}/1.0</b></p>
                        `;
                        
                        // Load the analysis data
                        loadAnalysisData(result.match_id);
                    } else {
                        document.getElementById('matchStatus').innerHTML = `
                            <h2>Error</h2>
                            <p>Failed to simulate match analysis.</p>
                        `;
                    }
                } catch (error) {
                    console.error('Error:', error);
                    document.getElementById('matchStatus').innerHTML = `
                        <h2>Error</h2>
                        <p>An unexpected error occurred: ${error.message}</p>
                    `;
                } finally {
                    this.disabled = false;
                    this.textContent = 'Simulate Match Analysis';
                }
            });
            
            // Clear matches button
            document.getElementById('clearMatchesBtn').addEventListener('click', async function() {
                if (confirm('Are you sure you want to clear all match data?')) {
                    const response = await fetch('/api/clear-matches', { method: 'POST' });
                    if (response.ok) {
                        document.getElementById('matchStatus').innerHTML = `
                            <h2>Demo Status</h2>
                            <p>All match data cleared. Use the "Simulate Match Analysis" button to generate new analysis data.</p>
                        `;
                        
                        // Reset all tabs
                        document.getElementById('overview-content').innerHTML = '<p>No match analysis data available yet. Please simulate a match first.</p>';
                        document.getElementById('aim-content').innerHTML = '<p>No aim analysis data available yet. Please simulate a match first.</p>';
                        document.getElementById('positioning-content').innerHTML = '<p>No positioning analysis data available yet. Please simulate a match first.</p>';
                        document.getElementById('decisions-content').innerHTML = '<p>No decision making analysis data available yet. Please simulate a match first.</p>';
                        document.getElementById('recommendations-content').innerHTML = '<p>No recommendations available yet. Please simulate a match first.</p>';
                    }
                }
            });
            
            // Function to load analysis data
            async function loadAnalysisData(matchId) {
                try {
                    const response = await fetch(`/api/analysis/${matchId}`);
                    if (response.ok) {
                        const analysis = await response.json();
                        
                        // Update overview tab
                        let overviewHtml = `
                            <div class="summary">${analysis.summary}</div>
                            <h3>Performance Metrics</h3>
                            <div class="stat-grid">
                        `;
                        
                        // Calculate overall score for each category
                        const aimMetrics = analysis.metrics.aim;
                        const positioningMetrics = analysis.metrics.positioning;
                        const decisionMetrics = analysis.metrics.decision_making;
                        
                        const aimScore = Object.values(aimMetrics).reduce((sum, val) => sum + val, 0) / Object.values(aimMetrics).length;
                        const positioningScore = Object.values(positioningMetrics).reduce((sum, val) => sum + val, 0) / Object.values(positioningMetrics).length;
                        const decisionScore = Object.values(decisionMetrics).reduce((sum, val) => sum + val, 0) / Object.values(decisionMetrics).length;
                        
                        // Add overall stats
                        overviewHtml += createStatBox('Aim Overall', Math.round(aimScore * 100) / 100, getRatingClass(aimScore));
                        overviewHtml += createStatBox('Positioning Overall', Math.round(positioningScore * 100) / 100, getRatingClass(positioningScore));
                        overviewHtml += createStatBox('Decision Making Overall', Math.round(decisionScore * 100) / 100, getRatingClass(decisionScore));
                        
                        overviewHtml += `</div>`;
                        document.getElementById('overview-content').innerHTML = overviewHtml;
                        
                        // Update aim tab
                        let aimHtml = `<h3>Aim Performance</h3><div class="stat-grid">`;
                        for (const [key, value] of Object.entries(aimMetrics)) {
                            aimHtml += createStatBox(formatMetricName(key), Math.round(value * 100) / 100, getRatingClass(value));
                        }
                        aimHtml += `</div>`;
                        document.getElementById('aim-content').innerHTML = aimHtml;
                        
                        // Update positioning tab
                        let positioningHtml = `<h3>Positioning Performance</h3><div class="stat-grid">`;
                        for (const [key, value] of Object.entries(positioningMetrics)) {
                            positioningHtml += createStatBox(formatMetricName(key), Math.round(value * 100) / 100, getRatingClass(value));
                        }
                        positioningHtml += `</div>`;
                        document.getElementById('positioning-content').innerHTML = positioningHtml;
                        
                        // Update decisions tab
                        let decisionsHtml = `<h3>Decision Making Performance</h3><div class="stat-grid">`;
                        for (const [key, value] of Object.entries(decisionMetrics)) {
                            decisionsHtml += createStatBox(formatMetricName(key), Math.round(value * 100) / 100, getRatingClass(value));
                        }
                        decisionsHtml += `</div>`;
                        document.getElementById('decisions-content').innerHTML = decisionsHtml;
                        
                        // Update recommendations tab
                        let recommendationsHtml = `<div class="recommendations">`;
                        
                        // Group recommendations by priority
                        const highPriority = analysis.recommendations.filter(r => r.priority === 'high');
                        const mediumPriority = analysis.recommendations.filter(r => r.priority === 'medium');
                        const lowPriority = analysis.recommendations.filter(r => r.priority === 'low');
                        
                        if (highPriority.length > 0) {
                            recommendationsHtml += `<h3>High Priority</h3>`;
                            highPriority.forEach(rec => {
                                recommendationsHtml += createRecommendation(rec);
                            });
                        }
                        
                        if (mediumPriority.length > 0) {
                            recommendationsHtml += `<h3>Medium Priority</h3>`;
                            mediumPriority.forEach(rec => {
                                recommendationsHtml += createRecommendation(rec);
                            });
                        }
                        
                        if (lowPriority.length > 0) {
                            recommendationsHtml += `<h3>Low Priority</h3>`;
                            lowPriority.forEach(rec => {
                                recommendationsHtml += createRecommendation(rec);
                            });
                        }
                        
                        recommendationsHtml += `</div>`;
                        document.getElementById('recommendations-content').innerHTML = recommendationsHtml;
                        
                    } else {
                        console.error('Failed to load analysis data');
                    }
                } catch (error) {
                    console.error('Error loading analysis data:', error);
                }
            }
            
            // Helper function to create a stat box
            function createStatBox(name, value, ratingClass) {
                return `
                    <div class="stat-box">
                        <h3>${name}</h3>
                        <div class="stat-value">${value}</div>
                        <span class="badge ${ratingClass}">${getRatingText(ratingClass)}</span>
                    </div>
                `;
            }
            
            // Helper function to create a recommendation
            function createRecommendation(rec) {
                return `
                    <div class="recommendation ${rec.priority}">
                        <h4>
                            <span class="badge badge-${rec.priority === 'high' ? 'danger' : rec.priority === 'medium' ? 'warning' : 'success'}">
                                ${rec.category.toUpperCase()}
                            </span>
                            ${rec.title}
                        </h4>
                        <p>${rec.description}</p>
                    </div>
                `;
            }
            
            // Helper function to get rating class
            function getRatingClass(value) {
                if (value < 0.4) return 'badge-danger';
                if (value < 0.6) return 'badge-warning';
                if (value < 0.8) return 'badge-info';
                return 'badge-success';
            }
            
            // Helper function to get rating text
            function getRatingText(ratingClass) {
                if (ratingClass === 'badge-danger') return 'Poor';
                if (ratingClass === 'badge-warning') return 'Average';
                if (ratingClass === 'badge-info') return 'Good';
                return 'Excellent';
            }
            
            // Helper function to format metric name
            function formatMetricName(name) {
                return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "message": "BGMI Esports Coach API is running",
        "match_count": len(MATCHES)
    })

@app.route('/api/simulate-match', methods=['POST'])
def simulate_match():
    """Simulate a match analysis for demo purposes"""
    data = request.json
    
    # Create match ID
    match_id = f"demo_{int(time.time())}_{str(uuid.uuid4())[:8]}"
    
    # Create match directory
    match_dir = os.path.join(DATA_DIR, match_id)
    os.makedirs(match_dir, exist_ok=True)
    os.makedirs(os.path.join(match_dir, "frames"), exist_ok=True)
    
    # Create metadata
    metadata = {
        "match_id": match_id,
        "game_mode": data.get("game_mode", "Solo"),
        "map_name": data.get("map_name", "Erangel"),
        "start_time": datetime.now().isoformat(),
        "end_time": datetime.now().isoformat(),
        "duration": random.randint(600, 1800),  # 10-30 minutes
        "resolution": "1920x1080",
        "fps": 10,
        "frames": []
    }
    
    # Save metadata
    with open(os.path.join(match_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f)
    
    # Run analyzer
    analyzer = GameplayAnalyzer(match_dir)
    analysis_results = analyzer.analyze()
    
    # Calculate overall score
    aim_metrics = analysis_results["metrics"]["aim"]
    positioning_metrics = analysis_results["metrics"]["positioning"]
    decision_metrics = analysis_results["metrics"]["decision_making"]
    
    aim_score = sum(aim_metrics.values()) / len(aim_metrics)
    positioning_score = sum(positioning_metrics.values()) / len(positioning_metrics)
    decision_score = sum(decision_metrics.values()) / len(decision_metrics)
    overall_score = (aim_score + positioning_score + decision_score) / 3
    
    # Save analysis
    analysis_file = os.path.join(match_dir, "analysis.json")
    with open(analysis_file, "w") as f:
        json.dump(analysis_results, f)
    
    # Store in memory
    MATCHES[match_id] = {
        "id": match_id,
        "game_mode": data.get("game_mode", "Solo"),
        "map_name": data.get("map_name", "Erangel"),
        "created_at": datetime.now().isoformat(),
        "analysis_file": analysis_file
    }
    
    return jsonify({
        "success": True,
        "match_id": match_id,
        "overall_score": overall_score
    })

@app.route('/api/analysis/<match_id>')
def get_analysis(match_id):
    """Get analysis results for a match"""
    if match_id not in MATCHES:
        return jsonify({"error": "Match not found"}), 404
    
    try:
        with open(MATCHES[match_id]["analysis_file"], "r") as f:
            analysis = json.load(f)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": f"Failed to load analysis: {str(e)}"}), 500

@app.route('/api/clear-matches', methods=['POST'])
def clear_matches():
    """Clear all match data"""
    global MATCHES
    MATCHES = {}
    return jsonify({"success": True})

@app.route('/api/matches')
def list_matches():
    """List all matches"""
    return jsonify(list(MATCHES.values()))

if __name__ == '__main__':
    print("Starting BGMI Esports Coach app on port 5000...")
    app.run(host='0.0.0.0', port=5000)