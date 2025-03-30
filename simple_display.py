from flask import Flask, render_template_string
import json
import time
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>BGMI Esports Coach</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; }
        .navbar { background-color: #6200ea !important; }
        .card { border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; border-radius: 10px; }
        .stat-card { height: 100%; transition: transform 0.3s; }
        .stat-card:hover { transform: translateY(-5px); }
        .stat-value { font-size: 2.5rem; font-weight: bold; }
        .rating-excellent { color: #4CAF50; }
        .rating-good { color: #2196F3; }
        .rating-average { color: #FF9800; }
        .rating-poor { color: #F44336; }
        .recommendation { border-left: 4px solid #6200ea; padding-left: 15px; }
        .priority-high { border-left-color: #F44336; }
        .priority-medium { border-left-color: #FF9800; }
        .priority-low { border-left-color: #2196F3; }
        .tab-pane { padding: 20px 0; }
        .chart-container { position: relative; height: 300px; margin-bottom: 20px; }
        .nav-tabs .nav-link.active { color: #6200ea; border-bottom: 3px solid #6200ea; }
        .nav-tabs .nav-link { color: #495057; }
        #summary-box { background-color: #6200ea; color: white; padding: 15px; border-radius: 10px; }
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
        <div class="container">
            <a class="navbar-brand" href="#">BGMI Esports Coach</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">History</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Settings</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container">
        <!-- Match Info -->
        <div class="card mb-4">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <h4>Match Analysis</h4>
                        <p class="text-muted">{{ match_info.map_name }} - {{ match_info.game_mode }}</p>
                    </div>
                    <div class="col-md-6 text-md-end">
                        <h5>Date: {{ match_info.date }}</h5>
                        <p>Duration: {{ match_info.duration }}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Navigation Tabs -->
        <ul class="nav nav-tabs mb-4" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button" role="tab">Overview</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="aim-tab" data-bs-toggle="tab" data-bs-target="#aim" type="button" role="tab">Aim Analysis</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="positioning-tab" data-bs-toggle="tab" data-bs-target="#positioning" type="button" role="tab">Positioning</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="decision-tab" data-bs-toggle="tab" data-bs-target="#decision" type="button" role="tab">Decision Making</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="recommendations-tab" data-bs-toggle="tab" data-bs-target="#recommendations" type="button" role="tab">Recommendations</button>
            </li>
        </ul>
        
        <!-- Tab Content -->
        <div class="tab-content" id="myTabContent">
            <!-- Overview Tab -->
            <div class="tab-pane fade show active" id="overview" role="tabpanel" aria-labelledby="overview-tab">
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card" id="summary-box">
                            <div class="card-body">
                                <h4 class="card-title">Analysis Summary</h4>
                                <p>{{ analysis.summary }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-4">
                    {% for category in categories %}
                    <div class="col-md-4 mb-3">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h5 class="card-title">{{ category.title }}</h5>
                                <div class="stat-value {{ category.rating_class }}">{{ category.score }}%</div>
                                <p class="card-text">{{ category.label }}</p>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Key Strengths</h5>
                                <ul class="list-group list-group-flush">
                                    {% for strength in strengths %}
                                    <li class="list-group-item">{{ strength }}</li>
                                    {% endfor %}
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Areas for Improvement</h5>
                                <ul class="list-group list-group-flush">
                                    {% for improvement in improvements %}
                                    <li class="list-group-item">{{ improvement }}</li>
                                    {% endfor %}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Aim Analysis Tab -->
            <div class="tab-pane fade" id="aim" role="tabpanel" aria-labelledby="aim-tab">
                <div class="row">
                    {% for aim_metric in aim_metrics %}
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h5 class="card-title">{{ aim_metric.title }}</h5>
                                <div class="stat-value {{ aim_metric.rating_class }}">{{ aim_metric.value }}%</div>
                                <p class="card-text">{{ aim_metric.description }}</p>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Weapon Performance</h5>
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Weapon</th>
                                        <th>Accuracy</th>
                                        <th>Headshot %</th>
                                        <th>Recoil Control</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for weapon in weapons %}
                                    <tr>
                                        <td>{{ weapon.name }}</td>
                                        <td>{{ weapon.accuracy }}%</td>
                                        <td>{{ weapon.headshot }}%</td>
                                        <td>{{ weapon.recoil }}%</td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Positioning Tab -->
            <div class="tab-pane fade" id="positioning" role="tabpanel" aria-labelledby="positioning-tab">
                <div class="row">
                    {% for pos_metric in positioning_metrics %}
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h5 class="card-title">{{ pos_metric.title }}</h5>
                                <div class="stat-value {{ pos_metric.rating_class }}">{{ pos_metric.value }}%</div>
                                <p class="card-text">{{ pos_metric.description }}</p>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Positioning Analysis</h5>
                        <p>Your positioning shows good awareness of zone movements. You effectively used terrain for cover during rotations, but could improve on selecting engagement spots with better escape routes.</p>
                        <p>On Erangel, your familiarity with compound layouts is evident, but you sometimes exposed yourself to multiple angles when taking fights in open areas.</p>
                    </div>
                </div>
            </div>
            
            <!-- Decision Making Tab -->
            <div class="tab-pane fade" id="decision" role="tabpanel" aria-labelledby="decision-tab">
                <div class="row">
                    {% for decision_metric in decision_metrics %}
                    <div class="col-md-6 col-lg-3 mb-4">
                        <div class="card stat-card">
                            <div class="card-body text-center">
                                <h5 class="card-title">{{ decision_metric.title }}</h5>
                                <div class="stat-value {{ decision_metric.rating_class }}">{{ decision_metric.value }}%</div>
                                <p class="card-text">{{ decision_metric.description }}</p>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Decision Making Patterns</h5>
                        <p>Your decision-making process shows good tactical planning but could improve on item management. You prioritized position over loot in late game, which is optimal for Battle Royale mode.</p>
                        <p>Work on timing your engagements better - several fights were initiated without full team coordination, leading to disadvantageous situations.</p>
                    </div>
                </div>
            </div>
            
            <!-- Recommendations Tab -->
            <div class="tab-pane fade" id="recommendations" role="tabpanel" aria-labelledby="recommendations-tab">
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title mb-4">Personalized Recommendations</h5>
                        
                        {% for recommendation in recommendations %}
                        <div class="recommendation mb-4 priority-{{ recommendation.priority }}">
                            <h5>{{ recommendation.title }}</h5>
                            <div class="d-flex align-items-center mb-2">
                                <span class="badge bg-{{ recommendation.badge_color }} me-2">{{ recommendation.priority|capitalize }}</span>
                                <span class="badge bg-secondary">{{ recommendation.category }}</span>
                            </div>
                            <p>{{ recommendation.description }}</p>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-light py-4 mt-5">
        <div class="container text-center">
            <p class="mb-0">© 2025 BGMI Esports Coach | Powered by AI</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def index():
    # Generate mock data for the demo
    match_info = {
        "map_name": "Erangel",
        "game_mode": "Battle Royale - Squad",
        "date": time.strftime("%B %d, %Y"),
        "duration": "24:38"
    }
    
    # Main category metrics
    categories = [
        {
            "title": "Aim",
            "score": 65,
            "label": "Above Average",
            "rating_class": "rating-good"
        },
        {
            "title": "Positioning",
            "score": 83,
            "label": "Excellent",
            "rating_class": "rating-excellent"
        },
        {
            "title": "Decision Making",
            "score": 58,
            "label": "Average",
            "rating_class": "rating-average"
        }
    ]
    
    # Analysis data
    analysis = {
        "summary": "Your gameplay shows Positioning as your strongest skill area with excellent zone awareness and rotation timing. Focus on improving your Decision Making which needs the most attention, particularly in item management and team coordination. For Battle Royale, prioritize positioning and zone awareness over aggressive engagements. On Erangel, use natural terrain for cover during zone rotations."
    }
    
    # Strengths and improvements
    strengths = [
        "Effective use of terrain for cover",
        "Excellent zone rotation timing",
        "Good tactical planning for late-game scenarios",
        "Above-average accuracy with DMRs"
    ]
    
    improvements = [
        "Recoil control with assault rifles",
        "Item management efficiency",
        "Team coordination during engagements",
        "Selecting engagement locations with better cover"
    ]
    
    # Aim metrics
    aim_metrics = [
        {
            "title": "Accuracy",
            "value": 75,
            "description": "Overall shooting accuracy",
            "rating_class": "rating-good"
        },
        {
            "title": "Headshot %",
            "value": 42,
            "description": "Percentage of headshots",
            "rating_class": "rating-average"
        },
        {
            "title": "Reaction Time",
            "value": 84,
            "description": "Speed of target acquisition",
            "rating_class": "rating-excellent"
        },
        {
            "title": "Recoil Control",
            "value": 58,
            "description": "Weapon stability management",
            "rating_class": "rating-average"
        }
    ]
    
    # Weapon performance
    weapons = [
        {
            "name": "M416",
            "accuracy": 68,
            "headshot": 38,
            "recoil": 62
        },
        {
            "name": "AKM",
            "accuracy": 55,
            "headshot": 45,
            "recoil": 48
        },
        {
            "name": "SLR",
            "accuracy": 82,
            "headshot": 52,
            "recoil": 74
        },
        {
            "name": "M24",
            "accuracy": 90,
            "headshot": 75,
            "recoil": 95
        }
    ]
    
    # Positioning metrics
    positioning_metrics = [
        {
            "title": "Cover Usage",
            "value": 81,
            "description": "Effective use of cover",
            "rating_class": "rating-excellent"
        },
        {
            "title": "Movement",
            "value": 77,
            "description": "Efficient movement patterns",
            "rating_class": "rating-good"
        },
        {
            "title": "Zone Awareness",
            "value": 88,
            "description": "Zone prediction and positioning",
            "rating_class": "rating-excellent"
        },
        {
            "title": "Rotation Timing",
            "value": 85,
            "description": "Timing of zone rotations",
            "rating_class": "rating-excellent"
        }
    ]
    
    # Decision making metrics
    decision_metrics = [
        {
            "title": "Engagements",
            "value": 69,
            "description": "When to take fights",
            "rating_class": "rating-good"
        },
        {
            "title": "Item Management",
            "value": 48,
            "description": "Looting efficiency",
            "rating_class": "rating-average"
        },
        {
            "title": "Tactical Planning",
            "value": 74,
            "description": "Strategy development",
            "rating_class": "rating-good"
        },
        {
            "title": "Team Coordination",
            "value": 42,
            "description": "Synchronization with team",
            "rating_class": "rating-average"
        }
    ]
    
    # Recommendations
    recommendations = [
        {
            "title": "Enhance Recoil Control",
            "priority": "medium",
            "badge_color": "warning",
            "category": "Aim",
            "description": "Practice spray patterns with AR and SMG weapons on static targets. Focus on pulling down gradually and learning the specific recoil pattern of each weapon, particularly the M416 and AKM."
        },
        {
            "title": "Utilize Cover Better",
            "priority": "high",
            "badge_color": "danger",
            "category": "Positioning",
            "description": "Always prioritize moving between cover points rather than open areas. When engaging, ensure you have at least two escape routes and never expose yourself to multiple angles simultaneously."
        },
        {
            "title": "Improve Zone Management",
            "priority": "medium",
            "badge_color": "warning",
            "category": "Positioning",
            "description": "Plan your movements based on zone predictions earlier in the match. Secure a central position in the 3rd and 4th zones to minimize rotation distance in late game."
        },
        {
            "title": "Optimize Item Management",
            "priority": "low",
            "badge_color": "info",
            "category": "Decision Making",
            "description": "Prioritize picking up essential healing items and ammo before looting other items. Aim to complete looting within 45 seconds per building to maintain movement efficiency."
        },
        {
            "title": "Enhance Team Communication",
            "priority": "high",
            "badge_color": "danger",
            "category": "Decision Making",
            "description": "Develop clear callouts for locations and enemies. Verbalize your tactical decisions to teammates before executing them, and ensure all team members confirm understanding."
        },
        {
            "title": "Consistent Practice Schedule",
            "priority": "medium",
            "badge_color": "warning",
            "category": "General",
            "description": "Set aside 30 minutes daily for targeted practice in areas needing improvement. Use training mode for recoil control practice, and dedicate time to reviewing your match recordings to identify positioning errors."
        }
    ]
    
    # Return the template with data
    return render_template_string(
        HTML,
        match_info=match_info,
        categories=categories,
        analysis=analysis,
        strengths=strengths,
        improvements=improvements,
        aim_metrics=aim_metrics,
        weapons=weapons,
        positioning_metrics=positioning_metrics,
        decision_metrics=decision_metrics,
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)