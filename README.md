# City Crime Rate Clustering System

An unsupervised machine learning system designed to group major cities based on crime statistics (Murder, Assault, Theft rates) and Population, classifying them into Safe, Moderate Risk, and High-Risk categories.

## 🎯 Project Objective
The goal is to provide a reproducible, automated unsupervised learning pipeline using **K-Means Clustering** to partition 50 Pakistani cities based on their crime rates. We map the resulting clusters to qualitative risk levels:
- **Safe Cities** ✅ (Lowest overall crime score)
- **Moderate Risk Cities** ⚠️ (Moderate overall crime score)
- **High-Risk Cities** 🚨 (Highest overall crime score)

The crime score is calculated using the following weighted formula:
$$\text{Crime Score} = \frac{\text{Murder Rate} \times 3 + \text{Assault Rate} \times 2 + \text{Theft Rate} \times 1}{6}$$

---

## 🛠️ Tech Stack & Requirements
This project is written in Python and utilizes standard data science libraries.
- **Languages**: Python 3.8+
- **Key Libraries**:
  - `numpy` (Reproducible dataset generation)
  - `pandas` (Data manipulation and reporting)
  - `scikit-learn` (StandardScaler, KMeans, Silhouette analysis)
  - `matplotlib` (Static visualizations)
  - `seaborn` (Professional statistical graphics)

To install dependencies, run:
```bash
pip install numpy pandas scikit-learn matplotlib seaborn
```

---

## 📁 File Structure
```
city_crime_clustering/
│
├── city_crime_clustering.py     # Main executable python script containing the end-to-end pipeline
├── app.py                      # Flask server defining the API endpoints and serving the UI
├── kmeans_model.pkl            # Serialized trained K-Means model object (pickle)
├── scaler.pkl                  # Serialized fit StandardScaler parameter instance (pickle)
├── city_crime_clustering_results.csv # Exported raw details per city (cluster labels, crime score, risk tag)
├── risk_level_statistics.csv    # Summary statistics grouped by assigned risk levels
│
# Saved High-Resolution Visualizations:
├── crime_distribution.png       # Histograms and kernel density estimates for all input variables
├── correlation_matrix.png       # Pairwise correlation heatmap of statistics
├── elbow_silhouette.png         # Elbow Curve & Silhouette Analysis curves (K=2 to 10)
├── clustering_results.png       # Multi-panel pairwise cluster scatter plots
└── risk_distribution.png        # Bar chart showing city count per risk category
```

---

## 🚀 How to Run
Execute the main script via terminal:
```bash
python city_crime_clustering.py
```

Upon execution, the script will:
1. Print a professional project header.
2. Generate a synthetic yet realistic dataset of 50 Pakistani cities.
3. Preprocess and scale the features, printing scaled sample data.
4. Calculate and plot clustering metrics (Inertia, Silhouette score) across $K \in [2, 10]$ to confirm $K=3$ as the optimal choice.
5. Train K-Means ($K=3$), assign labels, and decode cluster centroids.
6. Group clusters by crime score to assign risk labels: Safe ✅, Moderate Risk ⚠️, High-Risk 🚨.
7. Print descriptive reports of the Top 5 Safest and Top 5 Most Dangerous cities, along with risk summaries.
8. Output K-Means evaluation metrics (Silhouette score, Inertia, Iterations).
9. Automatically export the data CSVs and visual plots into the workspace folder.
10. End with `✅ PROJECT COMPLETE!`.
