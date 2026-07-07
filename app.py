import os
import sys
import pandas as pd
from flask import Flask, jsonify, render_template, send_from_directory

# Ensure stdout/stderr handle UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Configure folder paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_CSV = os.path.join(SCRIPT_DIR, 'data', 'city_crime_clustering_results.csv')
STATS_CSV = os.path.join(SCRIPT_DIR, 'data', 'risk_level_statistics.csv')

@app.route('/')
def home():
    """Serves the main dashboard HTML."""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """Returns the parsed city crime clustering results as JSON."""
    if not os.path.exists(RESULTS_CSV):
        return jsonify({'error': 'Results file not found. Run city_crime_clustering.py first.'}), 404
    try:
        df = pd.read_csv(RESULTS_CSV)
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Returns the risk level summary statistics as JSON."""
    if not os.path.exists(STATS_CSV):
        return jsonify({'error': 'Statistics file not found. Run city_crime_clustering.py first.'}), 404
    try:
        df = pd.read_csv(STATS_CSV)
        # Rename the first column if it's named 'Risk Level' or unnamed
        if df.columns[0] != 'Risk Level':
            df.rename(columns={df.columns[0]: 'Risk Level'}, inplace=True)
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plots/<filename>')
def get_plot(filename):
    """Serves the generated visualization PNG plots."""
    allowed_plots = ['crime_distribution.png', 'correlation_matrix.png', 'elbow_silhouette.png', 'clustering_results.png', 'risk_distribution.png']
    if filename not in allowed_plots:
        return jsonify({'error': 'Unauthorized file request.'}), 403
    plots_dir = os.path.join(SCRIPT_DIR, 'static', 'plots')
    if not os.path.exists(os.path.join(plots_dir, filename)):
        return jsonify({'error': f'Plot file {filename} not found.'}), 404
    return send_from_directory(plots_dir, filename)

@app.route('/api/predict', methods=['GET', 'POST'])
def predict():
    """Predicts risk cohort for a single city's statistics."""
    from flask import request
    try:
        if request.method == 'POST':
            # Check for JSON payload
            req_data = request.get_json() or {}
        else:
            req_data = request.args
            
        population = float(req_data.get('population', req_data.get('Population', 1000000)))
        murder_rate = float(req_data.get('murder', req_data.get('Murder Rate', 12.0)))
        assault_rate = float(req_data.get('assault', req_data.get('Assault Rate', 100.0)))
        theft_rate = float(req_data.get('theft', req_data.get('Theft Rate', 250.0)))
        city_name = req_data.get('city', req_data.get('City', 'Evaluated Jurisdiction'))
        
        # Load scaler and model
        scaler_path = os.path.join(SCRIPT_DIR, 'data', 'scaler.pkl')
        model_path = os.path.join(SCRIPT_DIR, 'data', 'kmeans_model.pkl')
        meta_path = os.path.join(SCRIPT_DIR, 'data', 'model_metadata.json')
        
        if not (os.path.exists(scaler_path) and os.path.exists(model_path) and os.path.exists(meta_path)):
            return jsonify({'error': 'Pre-trained models are missing. Train the model first.'}), 500
            
        with open(scaler_path, 'rb') as f:
            import pickle
            scaler = pickle.load(f)
        with open(model_path, 'rb') as f:
            kmeans = pickle.load(f)
        with open(meta_path, 'r') as f:
            import json
            risk_mapping = json.load(f)
            
        # Standardize features (Ordering: Murder Rate, Assault Rate, Theft Rate, Population)
        scaled_features = scaler.transform([[murder_rate, assault_rate, theft_rate, population]])
        
        # Predict cluster ID
        cluster_id = int(kmeans.predict(scaled_features)[0])
        
        # Map to risk level
        risk_level = risk_mapping.get(str(cluster_id), 'Unknown')
        
        # Calculate severity-weighted crime score
        crime_score = (murder_rate * 3.0 + assault_rate * 2.0 + theft_rate * 1.0) / 6.0
        
        return jsonify({
            'City': city_name,
            'Population': int(population),
            'Murder Rate': murder_rate,
            'Assault Rate': assault_rate,
            'Theft Rate': theft_rate,
            'Crime Score': round(crime_score, 4),
            'Cluster': cluster_id,
            'Risk Level': risk_level
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("Starting Premium AI Crime Intelligence Dashboard Server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(host='127.0.0.1', port=5000, debug=True)
