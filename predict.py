#!/usr/bin/env python
"""
3C Intelligence - Standalone Predict CLI
========================================
Author: Antigravity (University Submission Expert)
Description: A professional command-line utility to run inference on crime and demographic statistics.
             Loads serialized pre-trained Standard Scaler and K-Means clustering models.
"""

import os
import sys
import json
import pickle
import argparse
import warnings
import numpy as np

# Suppress sklearn feature names warning
warnings.filterwarnings('ignore')

# Ensure terminal stdout and stderr support UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Folder Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCALER_PATH = os.path.join(SCRIPT_DIR, 'models', 'scaler.pkl')
MODEL_PATH = os.path.join(SCRIPT_DIR, 'models', 'kmeans_model.pkl')
META_PATH = os.path.join(SCRIPT_DIR, 'models', 'model_metadata.json')

def load_ml_assets():
    """Loads scaler, model, and metadata. Prompts if missing."""
    if not (os.path.exists(SCALER_PATH) and os.path.exists(MODEL_PATH) and os.path.exists(META_PATH)):
        print("\n[ERROR] Model assets missing from 'models/' folder!")
        print("Please train the model first by running: python train.py\n")
        sys.exit(1)
        
    try:
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        with open(MODEL_PATH, 'rb') as f:
            kmeans = pickle.load(f)
        with open(META_PATH, 'r') as f:
            risk_mapping = json.load(f)
        return scaler, kmeans, risk_mapping
    except Exception as e:
        print(f"[ERROR] Failed to load model assets: {str(e)}")
        sys.exit(1)

def calculate_crime_score(murder, assault, theft):
    """Calculates severity-weighted crime index score."""
    # Weightings: Murder=3, Assault=2, Theft=1 (normalized by divisor 6)
    return (murder * 3.0 + assault * 2.0 + theft * 1.0) / 6.0

def run_prediction(city_name, population, murder, assault, theft):
    """Runs data preprocessing, fits model, and returns formatted prediction results."""
    scaler, kmeans, risk_mapping = load_ml_assets()
    
    # Preprocess & Scale features (Ordering: Murder Rate, Assault Rate, Theft Rate, Population)
    features = np.array([[murder, assault, theft, population]])
    scaled_features = scaler.transform(features)
    
    # Predict Cluster ID
    cluster_id = int(kmeans.predict(scaled_features)[0])
    
    # Map to qualitative Risk Level
    risk_level = risk_mapping.get(str(cluster_id), 'Unknown Risk Status')
    
    # Calculate Crime Score
    crime_score = calculate_crime_score(murder, assault, theft)
    
    # Display Results beautifully
    border = "=" * 60
    print(f"\n{border}")
    print(f" 🛡️  3C INTELLIGENCE - MODEL INFERENCE REPORT".center(60))
    print(f"{border}")
    print(f"  Target Jurisdiction  : {city_name}")
    print(f"  Municipal Population : {population:,}")
    print(f"------------------------------------------------------------")
    print(f"  Crime Indicators (per 100,000 population):")
    print(f"    - Murder Rate      : {murder:.2f}")
    print(f"    - Assault Rate     : {assault:.2f}")
    print(f"    - Theft Rate       : {theft:.2f}")
    print(f"------------------------------------------------------------")
    print(f"  Unsupervised Machine Learning Output:")
    print(f"    - Weighted Crime Score: {crime_score:.4f}")
    print(f"    - Assigned Cluster ID : {cluster_id}")
    print(f"    - Evaluated Risk Cohort: {risk_level}")
    print(f"{border}\n")

def main():
    parser = argparse.ArgumentParser(description="Predict urban risk cohort using K-Means Clustering.")
    parser.add_argument('--city', type=str, help="Name of the city/jurisdiction")
    parser.add_argument('--population', type=int, help="Population size")
    parser.add_argument('--murder', type=float, help="Murder rate per 100k")
    parser.add_argument('--assault', type=float, help="Assault rate per 100k")
    parser.add_argument('--theft', type=float, help="Theft rate per 100k")
    parser.add_argument('--interactive', action='store_true', help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # If no arguments provided or interactive flag set, prompt user
    if args.interactive or (args.city is None and args.population is None and args.murder is None and args.assault is None and args.theft is None):
        print("\n--- 3C Intelligence Interactive Inference Prompt ---")
        try:
            city = input("City Name             : ").strip() or "Evaluated City"
            population = int(input("Population            : ") or 1000000)
            murder = float(input("Murder Rate (per 100k): ") or 10.0)
            assault = float(input("Assault Rate (per 100k): ") or 120.0)
            theft = float(input("Theft Rate (per 100k) : ") or 250.0)
            run_prediction(city, population, murder, assault, theft)
        except ValueError as e:
            print(f"\n[INPUT ERROR] Invalid numerical inputs. Please try again. ({str(e)})\n")
    else:
        # Validate CLI parameters
        if None in (args.city, args.population, args.murder, args.assault, args.theft):
            print("\n[ERROR] Missing required arguments! Either provide all arguments or run interactive mode.")
            print("Usage: python predict.py --city \"CityName\" --population 1200000 --murder 15 --assault 110 --theft 220")
            print("Or run: python predict.py (to run in interactive mode)\n")
            sys.exit(1)
        run_prediction(args.city, args.population, args.murder, args.assault, args.theft)

if __name__ == '__main__':
    main()
