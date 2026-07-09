import os
import sys
import warnings
import pandas as pd
from flask import Flask, jsonify, render_template, send_from_directory

# Suppress sklearn feature names warning
warnings.filterwarnings('ignore')

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
        scaler_path = os.path.join(SCRIPT_DIR, 'models', 'scaler.pkl')
        model_path = os.path.join(SCRIPT_DIR, 'models', 'kmeans_model.pkl')
        meta_path = os.path.join(SCRIPT_DIR, 'models', 'model_metadata.json')
        
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

@app.route('/api/download-pdf')
def download_pdf():
    """Triggers generation of the portfolio PDF and serves it for download."""
    pdf_filename = '3C_Intelligence_Portfolio_Case_Study.pdf'
    pdf_dir = os.path.join(SCRIPT_DIR, 'portfolio')
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    try:
        from portfolio.generate_portfolio_pdf import build_pdf
        # Re-build PDF to ensure all local updates are compiled
        success = build_pdf(pdf_path)
        if success and os.path.exists(pdf_path):
            return send_from_directory(pdf_dir, pdf_filename, as_attachment=True)
        else:
            return jsonify({'error': 'PDF file generation failed on the server.'}), 500
    except Exception as e:
        return jsonify({'error': f'PDF Generation Exception: {str(e)}'}), 500

@app.route('/api/download-preview')
def download_preview():
    """Generates a PDF preview of the front-end dashboard and serves it for download."""
    pdf_filename = '3C_Intelligence_Dashboard_Preview.pdf'
    pdf_dir = os.path.join(SCRIPT_DIR, 'portfolio')
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    html_path = os.path.join(SCRIPT_DIR, 'templates', 'index.html')
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if not os.path.exists(chrome_path):
        # Fallback to secondary location
        chrome_path_x86 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(chrome_path_x86):
            chrome_path = chrome_path_x86
            
    try:
        import subprocess
        # Run headless Chrome to print the HTML directly to PDF
        r = subprocess.run([
            chrome_path,
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--no-pdf-header-footer',
            '--enable-background-graphics',
            f'--print-to-pdf={pdf_path}',
            file_url
        ], capture_output=True, text=True, timeout=15)
        
        if os.path.exists(pdf_path):
            return send_from_directory(pdf_dir, pdf_filename, as_attachment=True)
        else:
            return jsonify({
                'error': 'Failed to compile dashboard preview PDF.',
                'details': r.stderr
            }), 500
    except Exception as e:
        return jsonify({'error': f'Preview Generation Exception: {str(e)}'}), 500

@app.route('/api/download-showcase')
def download_showcase():
    """Triggers generation of the Fiverr 2-page showcase PDF and serves it for download."""
    pdf_filename = '3C_Intelligence_Project_Showcase.pdf'
    pdf_dir = os.path.join(SCRIPT_DIR, 'portfolio')
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    try:
        from portfolio.generate_showcase_pdf import build_showcase_pdf
        # Re-build PDF to ensure all local updates are compiled
        success = build_showcase_pdf(pdf_path)
        if success and os.path.exists(pdf_path):
            return send_from_directory(pdf_dir, pdf_filename, as_attachment=True)
        else:
            return jsonify({'error': 'Project showcase PDF file generation failed on the server.'}), 500
    except Exception as e:
        return jsonify({'error': f'Project Showcase PDF Generation Exception: {str(e)}'}), 500

@app.route('/api/download-visual')
def download_visual():
    """Triggers generation of the Fiverr 1024x768 visual showcase PDF and serves it for download."""
    pdf_filename = '3C_Intelligence_Visual_Showcase.pdf'
    pdf_dir = os.path.join(SCRIPT_DIR, 'portfolio')
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    try:
        # Dynamic screenshot regeneration via headless Chrome before compilation
        dashboard_img = os.path.join(pdf_dir, 'dashboard_screenshot.png')
        html_path = os.path.join(SCRIPT_DIR, 'templates', 'index.html')
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if not os.path.exists(chrome_path):
            chrome_path_x86 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            if os.path.exists(chrome_path_x86):
                chrome_path = chrome_path_x86
                
        import subprocess
        subprocess.run([
            chrome_path,
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            f'--screenshot={dashboard_img}',
            '--window-size=1280,960',
            file_url
        ], capture_output=True, timeout=15)
        
        from portfolio.generate_images_pdf import build_images_pdf
        # Re-build PDF to ensure all local updates are compiled
        success = build_images_pdf(pdf_path)
        if success and os.path.exists(pdf_path):
            return send_from_directory(pdf_dir, pdf_filename, as_attachment=True)
        else:
            return jsonify({'error': 'Visual showcase PDF generation failed on the server.'}), 500
    except Exception as e:
        return jsonify({'error': f'Visual Showcase PDF Generation Exception: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Premium AI Crime Intelligence Dashboard Server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(host='127.0.0.1', port=5000, debug=True)
