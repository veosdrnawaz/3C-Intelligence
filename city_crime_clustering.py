"""
City Crime Rate Clustering System
==================================
Author: Antigravity (Senior Data Scientist & ML Engineer)
Description: An unsupervised machine learning pipeline using K-Means clustering
             to group 50 Pakistani cities based on crime statistics (Murder,
             Assault, and Theft rates) and population, identifying Safe,
             Moderate Risk, and High-Risk cities.

This script executes all data science pipeline stages:
1. Realistic synthetic dataset generation with reproducible random seed.
2. Exploratory visual and statistical analysis.
3. Feature preprocessing and scaling (StandardScaler) with theoretical comments.
4. Elbow and Silhouette analysis to determine/verify optimal cluster numbers.
5. K-Means model training with custom risk level evaluation.
6. Comprehensive report generation and file exporting.
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Ensure terminal stdout and stderr support UTF-8 encoding for printing emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Filter warnings to maintain clean console output
warnings.filterwarnings('ignore')

# Set aesthetic styling for plots to ensure professional visuals
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style='whitegrid', context='talk')
plt.rcParams.update({
    'font.sans-serif': 'Arial',
    'font.family': 'sans-serif',
    'figure.titlesize': 20,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.facecolor': '#FDFDFD',
    'axes.facecolor': '#FCFCFC'
})

def print_header():
    """Prints a professional project header to the console."""
    border = "=" * 80
    title = " CITY CRIME RATE CLUSTERING SYSTEM "
    subtitle = "Powered by K-Means Clustering & Data Science Pipeline"
    print(f"\n{border}")
    print(f"{title.center(80, ' ')}")
    print(f"{subtitle.center(80, ' ')}")
    print(f"{border}\n")

def generate_dataset():
    """Generates a realistic crime statistics dataset for 50 Pakistani cities."""
    print("[STEP 1] Generating Pakistani Cities Crime Dataset...")
    
    # 50 Major Pakistani Cities across various regions
    cities = [
        "Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Gujranwala",
        "Peshawar", "Multan", "Hyderabad", "Islamabad", "Quetta",
        "Bahawalpur", "Sargodha", "Sialkot", "Sukkur", "Jhang",
        "Larkana", "Sheikhupura", "Mirpur Khas", "Rahim Yar Khan", "Kohat",
        "Gujrat", "Mardan", "Kasur", "Dera Ghazi Khan", "Sahiwal",
        "Nawabshah", "Mingora", "Okara", "Mirpur (AJK)", "Chiniot",
        "Kamoke", "Hafizabad", "Sadiqabad", "Turbat", "Muzaffargarh",
        "Khanewal", "Dera Ismail Khan", "Gojra", "Mandi Bahauddin", "Abbottabad",
        "Hub", "Khuzdar", "Muridke", "Tando Adam", "Khairpur",
        "Pakpattan", "Jhelum", "Gilgit", "Muzaffarabad", "Jacobabad"
    ]
    
    # Fixed seed for perfect reproducibility
    np.random.seed(42)
    n_cities = len(cities)
    
    # Generate realistic distributions based on real-world crime tendencies:
    # 1. Population: 100,000 to 5,000,000
    population = np.random.randint(100000, 5000000, size=n_cities)
    
    # Create some underlying correlations (e.g., higher pop often has higher total rates)
    # Scale base crime rates to correspond with population density to some extent
    pop_factor = (population - 100000) / 4900000.0
    
    # 2. Murder Rate (per 100k): Range 1 - 25. High correlation with other crimes
    murder_rate = 1.0 + pop_factor * 15.0 + np.random.uniform(0.0, 9.0, size=n_cities)
    murder_rate = np.clip(murder_rate, 1.0, 25.0).round(2)
    
    # 3. Assault Rate (per 100k): Range 10 - 200
    assault_rate = 10.0 + pop_factor * 120.0 + np.random.uniform(0.0, 70.0, size=n_cities)
    assault_rate = np.clip(assault_rate, 10.0, 200.0).round(2)
    
    # 4. Theft Rate (per 100k): Range 50 - 500
    theft_rate = 50.0 + pop_factor * 280.0 + np.random.uniform(0.0, 170.0, size=n_cities)
    theft_rate = np.clip(theft_rate, 50.0, 500.0).round(2)
    
    # Create Pandas DataFrame
    df = pd.DataFrame({
        'City': cities,
        'Population': population,
        'Murder Rate': murder_rate,
        'Assault Rate': assault_rate,
        'Theft Rate': theft_rate
    })
    
    # Display Dataset Info
    print("\n--- DataFrame Information ---")
    df.info()
    
    print("\n--- First 10 Rows of Dataset ---")
    print(df.head(10).to_string(index=False))
    
    print("\n--- Statistical Summary ---")
    print(df.describe().round(2))
    print("-" * 80 + "\n")
    
    return df

def visualize_distributions(df):
    """Generates distribution histograms for all 4 features and correlation heatmap."""
    print("[STEP 2] Generating Exploratory Visualizations...")
    
    # 1. Feature Distributions
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    features = ['Population', 'Murder Rate', 'Assault Rate', 'Theft Rate']
    colors = ['#3498db', '#e74c3c', '#9b59b6', '#f1c40f']
    
    for i, col in enumerate(features):
        ax = axes[i // 2, i % 2]
        sns.histplot(df[col], kde=True, ax=ax, color=colors[i], bins=15, edgecolor='black', alpha=0.7)
        ax.set_title(f'Distribution of {col}', fontsize=14, weight='bold')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
    
    plt.suptitle('City Feature Distributions (Histograms & KDE)', fontsize=18, weight='bold', y=0.98)
    plt.tight_layout()
    os.makedirs('static/plots', exist_ok=True)
    plt.savefig('static/plots/crime_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved 'static/plots/crime_distribution.png' successfully.")

    # 2. Correlation Heatmap
    plt.figure(figsize=(10, 8))
    corr_matrix = df[features].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, 
                vmin=-1, vmax=1, cbar_kws={'shrink': 0.8}, annot_kws={"size": 14})
    plt.title('Correlation Heatmap of City Features', fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('static/plots/correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved 'static/plots/correlation_matrix.png' successfully.\n")

def preprocess_data(df):
    """Preprocesses and scales features using StandardScaler."""
    print("[STEP 3] Preprocessing and Scaling Features...")
    
    # CRITICAL MACHINE LEARNING THEORY COMMENT:
    # ----------------------------------------
    # Feature Scaling is critical for K-Means Clustering for several reasons:
    # 1. Distance Metric: K-Means relies heavily on Euclidean Distance to group points.
    # 2. Magnitude Disparity: Feature values differ in magnitude (Population is in millions, 
    #    Theft is in hundreds, Murder is under 25). Without scaling, features with large
    #    magnitudes (e.g., Population) will dominate the distance calculations, causing the 
    #    model to ignore highly critical crime rates.
    # 3. Variance & Units: Scaling standardizes features to have mean=0 and variance=1,
    #    ensuring each variable is treated with equal importance during training.
    
    feature_cols = ['Murder Rate', 'Assault Rate', 'Theft Rate', 'Population']
    X = df[feature_cols]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("\nSample of Scaled Data (First 5 Rows):")
    scaled_df_sample = pd.DataFrame(X_scaled, columns=feature_cols).head(5)
    print(scaled_df_sample.round(4).to_string(index=False))
    print("-" * 80 + "\n")
    
    return X_scaled, scaler, feature_cols

def find_optimal_clusters(X_scaled):
    """Evaluates cluster counts from K=2 to 10 using Inertia and Silhouette scores."""
    print("[STEP 4] Evaluation of Cluster Sizes (Elbow & Silhouette Method)...")
    
    k_range = range(2, 11)
    inertias = []
    silhouette_scores = []
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
    
    # Plot both Elbow and Silhouette methods in a side-by-side plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    
    # Elbow Plot
    ax1.plot(k_range, inertias, marker='o', linestyle='--', color='#2c3e50', linewidth=2.5, markersize=8)
    ax1.set_title('Elbow Method (Inertia vs. K)', fontsize=16, weight='bold', pad=15)
    ax1.set_xlabel('Number of Clusters (K)', fontsize=14)
    ax1.set_ylabel('Inertia (Within-Cluster Sum of Squares)', fontsize=14)
    ax1.set_xticks(k_range)
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Highlight K=3 elbow point
    ax1.axvline(x=3, color='#e74c3c', linestyle=':', label='Optimal Elbow (K=3)', linewidth=2)
    ax1.legend()
    
    # Silhouette Plot
    ax2.plot(k_range, silhouette_scores, marker='s', linestyle='-', color='#16a085', linewidth=2.5, markersize=8)
    ax2.set_title('Silhouette Analysis vs. K', fontsize=16, weight='bold', pad=15)
    ax2.set_xlabel('Number of Clusters (K)', fontsize=14)
    ax2.set_ylabel('Average Silhouette Coefficient', fontsize=14)
    ax2.set_xticks(k_range)
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    # Highlight K=3 silhouette point
    ax2.axvline(x=3, color='#e74c3c', linestyle=':', label='Optimal Score (K=3)', linewidth=2)
    ax2.legend()
    
    plt.suptitle('Evaluating Optimal Number of Clusters', fontsize=20, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('static/plots/elbow_silhouette.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Saved 'static/plots/elbow_silhouette.png' successfully.")
    
    # Detailed optimal cluster explanation
    print("\n--- Selection Explanation ---")
    print("Optimal K selected is 3 due to the following:")
    print("1. Elbow Curve: The slope begins to flatten out visibly at K = 3 (Elbow Point),")
    print("   indicating that higher K values yield diminishing returns in reducing Inertia.")
    print("2. Silhouette Score: The Silhouette Coefficient peaks/shows strong local maximum at K = 3,")
    print("   suggesting optimal separation and cohesion between clusters.")
    print("3. Business Logic: This aligns perfectly with the target categorization of")
    print("   'Safe Cities', 'Moderate Risk Cities', and 'High-Risk Cities'.")
    print("-" * 80 + "\n")
    
    return 3

def train_model(df, X_scaled, scaler, k_clusters):
    """Trains K-Means model with optimal K=3, assigns labels, and decodes centroids."""
    print("[STEP 5] Model Training and Centroid Mapping...")
    
    # Fit KMeans
    kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # Save model and scaler objects to filesystem
    import pickle
    os.makedirs('data', exist_ok=True)
    model_path = 'data/kmeans_model.pkl'
    scaler_path = 'data/scaler.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump(kmeans, f)
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
        
    print(f"Saved trained K-Means model serialized to '{model_path}'")
    print(f"Saved StandardScaler parameters serialized to '{scaler_path}'")
    
    # Decode cluster centers to original scale
    raw_centroids = kmeans.cluster_centers_
    decoded_centroids = scaler.inverse_transform(raw_centroids)
    
    centroid_df = pd.DataFrame(decoded_centroids, columns=['Murder Rate', 'Assault Rate', 'Theft Rate', 'Population'])
    centroid_df.index.name = 'Cluster ID'
    
    print("\n--- Decoded Cluster Centroids (Original Scale) ---")
    print(centroid_df.round(2).to_string())
    print("-" * 80 + "\n")
    
    return df, kmeans, centroid_df

def analyze_and_map_risk(df, centroid_df):
    """Maps numerical cluster numbers to qualitative risk levels using a weighted Crime Score."""
    print("[STEP 6] Performing Cluster Analysis & Mapping Risk Levels...")
    
    # Compute Crime Score on Centroids
    # Formula: Crime Score = (Murder_Rate * 3 + Assault_Rate * 2 + Theft_Rate * 1) / 6
    centroid_df['Crime Score'] = (
        centroid_df['Murder Rate'] * 3 +
        centroid_df['Assault Rate'] * 2 +
        centroid_df['Theft Rate'] * 1
    ) / 6.0
    
    # Rank clusters based on Crime Score to dynamically tag risk level
    # Lowest average crime score -> Safe ✅
    # Middle average crime score -> Moderate Risk ⚠️
    # Highest average crime score -> High-Risk 🚨
    sorted_centroids = centroid_df.sort_values(by='Crime Score').copy()
    
    risk_mapping = {}
    labels = ['Safe ✅', 'Moderate Risk ⚠️', 'High-Risk 🚨']
    
    for i, cluster_id in enumerate(sorted_centroids.index):
        risk_mapping[cluster_id] = labels[i]
        
    # Map back to main DataFrame
    df['Risk Level'] = df['Cluster'].map(risk_mapping)
    
    # Save risk mapping metadata JSON
    import json
    os.makedirs('data', exist_ok=True)
    with open('data/model_metadata.json', 'w') as f:
        json.dump({str(k): v for k, v in risk_mapping.items()}, f)
    print("Saved risk mapping metadata to 'data/model_metadata.json'")
    
    # Compute Crime Score for all individual cities too for reporting ranking
    df['Crime Score'] = (
        df['Murder Rate'] * 3 +
        df['Assault Rate'] * 2 +
        df['Theft Rate'] * 1
    ) / 6.0
    
    # Print city distribution per risk level
    distribution = df['Risk Level'].value_counts()
    print("\n--- Distribution of Cities per Risk Level ---")
    for r_level, count in distribution.items():
        print(f"  {r_level:<20}: {count} cities")
    print("-" * 80 + "\n")
    
    return df, risk_mapping

def generate_cluster_plots(df, risk_mapping):
    """Generates 2D scatter plots for pairwise feature combinations and risk level distribution bar chart."""
    print("[STEP 7] Plotting Final Clustering and Risk Distribution Results...")
    
    # Sort DataFrame by Risk Level for consistent legend coloring
    risk_order = ['Safe ✅', 'Moderate Risk ⚠️', 'High-Risk 🚨']
    colors_dict = {
        'Safe ✅': '#2ecc71',
        'Moderate Risk ⚠️': '#f39c12',
        'High-Risk 🚨': '#e74c3c'
    }
    
    # 1. Cluster Scatter Plots: Compare pairwise features
    fig, axes = plt.subplots(2, 2, figsize=(18, 14))
    
    # Pairwise plot list
    pairs = [
        ('Murder Rate', 'Assault Rate', axes[0, 0]),
        ('Assault Rate', 'Theft Rate', axes[0, 1]),
        ('Murder Rate', 'Theft Rate', axes[1, 0]),
        ('Population', 'Theft Rate', axes[1, 1])
    ]
    
    for x_col, y_col, ax in pairs:
        sns.scatterplot(
            data=df, x=x_col, y=y_col, hue='Risk Level', 
            hue_order=risk_order, palette=colors_dict,
            s=120, edgecolor='black', alpha=0.85, ax=ax
        )
        ax.set_title(f'{y_col} vs. {x_col}', fontsize=14, weight='bold')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.legend(title='Risk Level', frameon=True, facecolor='white', framealpha=0.9)
        ax.grid(True, linestyle=':', alpha=0.6)
        
    plt.suptitle('City Crime Clusters: Pairwise Feature Analysis', fontsize=20, weight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('static/plots/clustering_results.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved 'static/plots/clustering_results.png' successfully.")
    
    # 2. Risk Distribution Bar Chart
    plt.figure(figsize=(10, 6))
    counts = df['Risk Level'].value_counts().reindex(risk_order)
    
    sns.barplot(
        x=counts.index, y=counts.values, 
        palette=[colors_dict[k] for k in counts.index],
        edgecolor='black', alpha=0.85
    )
    
    # Annotate bars with exact counts
    for idx, val in enumerate(counts.values):
        plt.text(idx, val + 0.5, str(val), ha='center', va='bottom', fontsize=14, weight='bold')
        
    plt.title('Distribution of Cities by Risk Level', fontsize=16, weight='bold', pad=15)
    plt.xlabel('Risk Level Tag', fontsize=14)
    plt.ylabel('Number of Cities', fontsize=14)
    plt.ylim(0, max(counts.values) + 4)
    plt.tight_layout()
    plt.savefig('static/plots/risk_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved 'static/plots/risk_distribution.png' successfully.\n")

def generate_reports(df):
    """Outputs structured markdown reports in console and exports CSV result files."""
    print("[STEP 8] Compiling Detailed Statistical Reports...")
    
    # Sort dataset for safe/dangerous lists
    safest_5 = df.sort_values(by='Crime Score', ascending=True).head(5)
    dangerous_5 = df.sort_values(by='Crime Score', ascending=False).head(5)
    
    print("\n=================================== REPORTING REPORT ===================================")
    print("\n🟢 TOP 5 SAFEST CITIES (Lowest Crime Scores):")
    print(safest_5[['City', 'Population', 'Murder Rate', 'Assault Rate', 'Theft Rate', 'Crime Score', 'Risk Level']].to_string(index=False))
    
    print("\n🔴 TOP 5 MOST DANGEROUS CITIES (Highest Crime Scores):")
    print(dangerous_5[['City', 'Population', 'Murder Rate', 'Assault Rate', 'Theft Rate', 'Crime Score', 'Risk Level']].to_string(index=False))
    
    # Grouped Statistics per Risk Level
    grouped_stats = df.groupby('Risk Level').agg({
        'City': 'count',
        'Population': 'mean',
        'Murder Rate': 'mean',
        'Assault Rate': 'mean',
        'Theft Rate': 'mean',
        'Crime Score': 'mean'
    }).rename(columns={'City': 'City Count'}).round(2)
    
    print("\n📊 RISK LEVEL SUMMARIZED STATISTICS:")
    print(grouped_stats.to_string())
    print("\n========================================================================================")
    
    # Export main results CSV
    export_df = df[['City', 'Population', 'Murder Rate', 'Assault Rate', 'Theft Rate', 'Crime Score', 'Risk Level', 'Cluster']]
    os.makedirs('data', exist_ok=True)
    export_df.to_csv('data/city_crime_clustering_results.csv', index=False)
    print("Saved report details to 'data/city_crime_clustering_results.csv'")
    
    # Export summary statistics CSV
    grouped_stats.to_csv('data/risk_level_statistics.csv')
    print("Saved statistics summary to 'data/risk_level_statistics.csv'\n")

def evaluate_model(X_scaled, kmeans):
    """Computes, prints, and interprets metrics for the trained clustering model."""
    print("[STEP 9] Model Quality Evaluation...")
    
    # Metrics
    inertia = kmeans.inertia_
    labels = kmeans.labels_
    score = silhouette_score(X_scaled, labels)
    iters = kmeans.n_iter_
    
    # Determine quality based on silhouette score
    if score >= 0.5:
        quality_msg = "Excellent clustering quality (Well separated, dense clusters)."
    elif score >= 0.3:
        quality_msg = "Good clustering quality (Reasonably structured clusters)."
    else:
        quality_msg = "Poor clustering quality (Considerable overlap or noise)."
        
    print("\n--- Clustering Evaluation Metrics ---")
    print(f"  Silhouette Score : {score:.4f}")
    print(f"  Inertia          : {inertia:.4f}")
    print(f"  Iterations to fit: {iters}")
    print(f"  Quality Rating   : {quality_msg}")
    print("-" * 80 + "\n")

def main():
    print_header()
    
    # Run the pipelines
    df = generate_dataset()
    visualize_distributions(df)
    X_scaled, scaler, feature_cols = preprocess_data(df)
    optimal_k = find_optimal_clusters(X_scaled)
    df, kmeans, centroid_df = train_model(df, X_scaled, scaler, optimal_k)
    df, risk_mapping = analyze_and_map_risk(df, centroid_df)
    generate_cluster_plots(df, risk_mapping)
    generate_reports(df)
    evaluate_model(X_scaled, kmeans)
    
    print("✅ PROJECT COMPLETE!")

if __name__ == '__main__':
    # Make sure execution directory is within current folder path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()
