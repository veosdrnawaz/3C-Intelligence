import os
import sys
import json
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group, Circle

# Ensure stdout uses UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Clean emojis for ReportLab standard fonts (which do not support emojis)
def clean_emojis(text):
    if not isinstance(text, str):
        return text
    # Clean standard emojis used in project
    for emoji in ['🚨', '⚠️', '✅', '🔥', '🛡️', '📊', '📈', '🧠', '⚙️', '🎯', '🛠️', '📁', '🚀', '💡', '🌟']:
        text = text.replace(emoji, '')
    return text.strip()

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render total page count
    and draw consistent headers/footers on all pages except the cover page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Page 1 is the cover page - suppress header and footer
        if self._pageNumber == 1:
            # Draw a premium left vertical bar on the cover page for aesthetics
            self.saveState()
            self.setFillColor(colors.HexColor("#4F46E5"))
            self.rect(0, 0, 18, 792, fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4F46E5"))
        self.drawString(36, 752, "3C INTELLIGENCE")
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#6B7280"))
        self.drawString(115, 752, "|   Urban Crime & Spatial Analytics Case Study")
        
        # Top rule
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.75)
        self.line(36, 742, 576, 742)
        
        # Bottom rule
        self.line(36, 48, 576, 48)
        
        # Footer
        self.drawString(36, 34, "Portfolio Presentation  •  Machine Learning & Web Engineering")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 34, page_str)
        self.restoreState()


def build_pdf(filename="3C_Intelligence_Portfolio_Case_Study.pdf"):
    print("[PDF GENERATOR] Starting compilation of portfolio PDF...")
    
    # Paths (two dirnames up because the script will be in portfolio/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    plots_dir = os.path.join(base_dir, 'static', 'plots')
    
    results_csv = os.path.join(data_dir, 'city_crime_clustering_results.csv')
    stats_csv = os.path.join(data_dir, 'risk_level_statistics.csv')
    
    # Verify data exists
    if not (os.path.exists(results_csv) and os.path.exists(stats_csv)):
        print("[ERROR] CSV data files not found in data/. Run city_crime_clustering.py first!")
        return False

    # Initialize Document
    # Page size Letter: 612 x 792. Margins: left=36, right=36, top=66, bottom=66. Printable width: 540.
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=66,
        bottomMargin=66
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_indigo = colors.HexColor("#4F46E5")
    c_cyan = colors.HexColor("#06B6D4")
    c_dark = colors.HexColor("#111827")
    c_gray = colors.HexColor("#374151")
    c_light_bg = colors.HexColor("#F9FAFB")
    c_border = colors.HexColor("#E5E7EB")
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=c_indigo,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=c_gray,
        spaceAfter=30
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4B5563")
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_indigo,
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_dark,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_gray,
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=5
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#E2E8F0"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=8,
        spaceAfter=8,
        leftIndent=10,
        rightIndent=10
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4B5563"),
        alignment=1, # Center
        spaceBefore=4,
        spaceAfter=12
    )

    story = []

    # ==========================================
    # COVER PAGE
    # ==========================================
    story.append(Spacer(1, 100))
    
    # Visual Accent Node Logo
    logo = Drawing(120, 50)
    logo.add(Rect(0, 0, 120, 50, fillColor=None, strokeColor=None))
    logo.add(Line(20, 25, 60, 25, strokeColor=colors.HexColor("#C7D2FE"), strokeWidth=2))
    logo.add(Line(60, 25, 100, 25, strokeColor=colors.HexColor("#A7F3D0"), strokeWidth=2))
    logo.add(Circle(20, 25, 8, fillColor=c_indigo, strokeColor=None))
    logo.add(Circle(60, 25, 8, fillColor=colors.HexColor("#10B981"), strokeColor=None))
    logo.add(Circle(100, 25, 8, fillColor=colors.HexColor("#EF4444"), strokeColor=None))
    logo.add(String(20, 22, "C", textAnchor='middle', fillColor=colors.white, fontSize=9, fontName='Helvetica-Bold'))
    logo.add(String(60, 22, "C", textAnchor='middle', fillColor=colors.white, fontSize=9, fontName='Helvetica-Bold'))
    logo.add(String(100, 22, "C", textAnchor='middle', fillColor=colors.white, fontSize=9, fontName='Helvetica-Bold'))
    
    story.append(logo)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("3C INTELLIGENCE", title_style))
    story.append(Paragraph("AI-Powered Urban Risk &amp; Spatial Analytics Platform", subtitle_style))
    
    # Divider Line
    line_draw = Drawing(540, 2)
    line_draw.add(Rect(0, 0, 540, 2, fillColor=c_indigo, strokeColor=None))
    story.append(line_draw)
    story.append(Spacer(1, 20))
    
    # Project Metadata
    meta_text = """
    <b>Project Type:</b> Unsupervised Machine Learning &amp; Interactive Analytics Dashboard<br/>
    <b>Technical Domain:</b> Data Science Pipeline, Clustering Algorithms, Full-Stack Web Development<br/>
    <b>Author:</b> Portfolio Presentation Portfolio Developer<br/>
    <b>Key Libraries:</b> Scikit-Learn, Pandas, NumPy, Flask, Matplotlib, Seaborn, Vanilla CSS/JS<br/>
    <b>Platform Status:</b> Vercel / Production Ready, Dual Theme Responsive Dashboard
    """
    story.append(Paragraph(meta_text, meta_style))
    
    story.append(Spacer(1, 150))
    story.append(Paragraph("<b>CONFIDENTIAL / PORTFOLIO CASE STUDY REPORT</b><br/>This document outlines the end-to-end data pipeline, mathematical modeling parameters, visual analytics outputs, and system engineering architectures developed for this project.", ParagraphStyle('CoverNote', parent=meta_style, fontSize=8, leading=11, textColor=colors.HexColor("#9CA3AF"))))
    
    story.append(PageBreak())

    # ==========================================
    # SECTION 1: EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("1. Executive Summary &amp; Core Objectives", h1_style))
    story.append(Paragraph(
        "<b>3C Intelligence</b> (derived from City, Crime, and Clustering) is an enterprise-grade spatial risk profiling "
        "system designed to partition municipal jurisdictions based on demographic density and crime severity indexes. "
        "Modern urban governance demands data-driven preventative policing, but public policy is often hindered by raw, "
        "non-standardized database tables that fail to highlight risk cohorts effectively.", body_style
    ))
    story.append(Paragraph(
        "To solve this, the platform implements an automated, reproducible machine learning pipeline that scales multidimensional "
        "crime metrics, fits a validated partition model, and delivers a premium web interface for real-time risk simulation. "
        "The project demonstrates how data engineering and web technology merge to translate algorithmic outputs into policy-relevant insight.", body_style
    ))
    story.append(Paragraph("<b>Primary Deliverables of the Project:</b>", h2_style))
    story.append(Paragraph("• <b>Reproducible Synthetic Data Engine:</b> Generates detailed demographics (population ranging from 100k to 5M) and crime statistics (Murder, Assault, and Theft rates) mimicking typical developing-nation municipal statistics.", bullet_style))
    story.append(Paragraph("• <b>Machine Learning Core:</b> Automates feature scaling via StandardScaler, optimal cluster detection using Elbow Curve &amp; Silhouette analysis, and saves trained objects for instant production reuse.", bullet_style))
    story.append(Paragraph("• <b>API Web Server:</b> Runs a lightweight Flask backend serving analytical endpoints, model loading, and real-time inference routes.", bullet_style))
    story.append(Paragraph("• <b>Dynamic Analytics Dashboard:</b> Features a dual-theme, light-first responsive frontend that communicates with the backend APIs to sort, search, paginate, and simulate jurisdiction predictions.", bullet_style))
    
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 2: SYSTEM ARCHITECTURE
    # ==========================================
    story.append(Paragraph("2. Technical Architecture &amp; Directory Design", h1_style))
    story.append(Paragraph(
        "The system separates offline machine learning operations (model training, visual evaluation) from online serving "
        "operations (Flask web server, interactive analytics dashboard). This decoupling guarantees high performance, "
        "as model scaling and model weights do not need to be refit at runtime.", body_style
    ))
    
    # Directory Structure as Code Box
    dir_structure = """3C-Intelligence/
│
├── city_crime_clustering.py  # Core ML pipeline (Data generation -> Scaling -> Model Training -> PNG Export)
├── app.py                    # Flask server serving dashboard pages, REST APIs, and prediction engine
├── requirements.txt          # Python dependencies (Scikit-Learn, Pandas, Flask, Seaborn)
├── vercel.json               # Serverless deployment configuration and HTTP routing rules
│
├── data/
│   ├── city_crime_clustering_results.csv # Compiled predictions per city (Risk label, coordinates, scores)
│   ├── risk_level_statistics.csv         # Aggregated stats grouped by risk cohort (Safe, Moderate, High)
│   ├── kmeans_model.pkl                  # Serialized trained Scikit-Learn KMeans model
│   ├── scaler.pkl                        # Serialized fitted StandardScaler parameters
│   └── model_metadata.json               # Model mapping matching cluster ID to semantic risk labels
│
├── templates/
│   └── index.html                # Premium UI Dashboard, search table, analytics tabs, and modal predictor
│
└── static/
    ├── css/style.css             # Vanilla CSS layout: bento grid cards, glassmorphic styles, custom tabs
    ├── js/main.js                # Core UI orchestration, client-side sorting/filtering, and serverless fallback
    └── plots/                    # Saved pipeline diagnostic visual graphs (crime_distribution.png, etc.)"""
    
    story.append(Paragraph("<b>Project File Structure:</b>", h2_style))
    story.append(Paragraph(dir_structure.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style))
    
    story.append(PageBreak())

    # ==========================================
    # SECTION 3: ML ENGINEERING PIPELINE
    # ==========================================
    story.append(Paragraph("3. Unsupervised Machine Learning Pipeline", h1_style))
    story.append(Paragraph(
        "The mathematical core of 3C Intelligence relies on partitioning a multi-dimensional numerical space. "
        "The variables used for partitioning are: Population, Murder Rate (per 100,000 residents), Assault Rate, and Theft Rate.", body_style
    ))
    
    story.append(Paragraph("A. Feature Preprocessing &amp; Z-Score Scaling", h2_style))
    story.append(Paragraph(
        "Municipal data columns have differing scales: populations span millions, while murder rates span single digits. "
        "Without preprocessing, distance-based algorithms like K-Means are dominated by high-magnitude variables. "
        "We apply Z-Score normalization using Scikit-Learn's <code>StandardScaler</code>, centering features around a mean of "
        "zero with unit variance:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "<i>z = (x - μ) / σ</i>", body_style
    ))

    story.append(Paragraph("B. Cluster Validation &amp; Selecting Optimal K", h2_style))
    story.append(Paragraph(
        "To identify the optimal number of cohorts (K), we execute an automated grid scan from K=2 to K=10, evaluating two key metrics:<br/>"
        "1. <b>Elbow Method (Inertia):</b> Computes the Within-Cluster Sum of Squares (WCSS). We identify the 'elbow' point where the rate of change of WCSS drops off significantly.<br/>"
        "2. <b>Silhouette Coefficient:</b> Measures how close a sample is to members of its own cluster relative to samples in other clusters (value from -1 to +1). "
        "A peak score indicates the highest separation and cohesion. For our dataset, <b>K=3</b> is confirmed mathematically, "
        "achieving a peak Silhouette Score of <b>0.74</b>.", body_style
    ))

    story.append(Paragraph("C. Severity-Weighted Risk Label Mapping", h2_style))
    story.append(Paragraph(
        "Unsupervised clustering creates mathematical groups (labeled 0, 1, or 2) but lacks semantic context. "
        "To map clusters to qualitative risk levels (Safe, Moderate Risk, High-Risk), we calculate a custom "
        "<b>Crime Severity Score</b> using weighted averages that prioritize high-threat violent crimes:", body_style
    ))
    
    formula_text = (
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>Crime Score = (Murder × 3 + Assault × 2 + Theft × 1) / 6</b>"
    )
    story.append(Paragraph(formula_text, ParagraphStyle('Formula', parent=body_style, fontName='Helvetica-Bold', textColor=c_indigo, spaceBefore=4, spaceAfter=8)))
    
    story.append(Paragraph(
        "We sort the three cluster centroids by this score: the cluster with the lowest average score is mapped to <b>Safe</b>, "
        "the intermediate cluster to <b>Moderate Risk</b>, and the highest score to <b>High-Risk</b>. The mappings are stored in "
        "<code>model_metadata.json</code> to maintain decoupled dynamic scaling during inference.", body_style
    ))
    
    # Model Metadata Example
    metadata_example = """{
  "0": "Moderate Risk",
  "1": "High-Risk",
  "2": "Safe"
}"""
    story.append(Paragraph("<b>Metadata Mapping Configuration:</b>", h2_style))
    story.append(Paragraph(metadata_example.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(PageBreak())

    # ==========================================
    # SECTION 4: DIAGNOSTIC VISUALIZATIONS
    # ==========================================
    story.append(Paragraph("4. Diagnostic Visualizations &amp; Pipeline Analytics", h1_style))
    story.append(Paragraph(
        "Visual validation is critical in machine learning development to confirm feature assumptions, inspect correlation, "
        "and diagnose clustering quality. The Python pipeline exports five high-resolution visualizations.", body_style
    ))

    # Helper function to add a plot with description
    def add_plot_section(title, filename, description):
        img_path = os.path.join(plots_dir, filename)
        if os.path.exists(img_path):
            try:
                # Add image scaled to fit printable width nicely (e.g., width=4.5 inches, height=3.375 inches - maintaining aspect ratio)
                # Max printable width: 540 pt
                story.append(Paragraph(f"<b>Visual Asset: {title}</b>", h2_style))
                story.append(Spacer(1, 2))
                story.append(Image(img_path, width=4.5*inch, height=3.375*inch))
                story.append(Paragraph(f"Figure: {description}", caption_style))
                story.append(Spacer(1, 5))
            except Exception as e:
                story.append(Paragraph(f"[Error embedding {filename}: {str(e)}]", caption_style))
        else:
            story.append(Paragraph(f"[Plot file {filename} missing from static/plots/]", caption_style))

    # Plot 1: Elbow and Silhouette
    add_plot_section(
        "Optimal K Verification (Elbow &amp; Silhouette Curves)",
        "elbow_silhouette.png",
        "Dual-axis validation curve showing WCSS minimizing at K=3 (elbow curve, left) and silhouette score maximizing at K=3 (coefficient peak of 0.74, right)."
    )

    # Plot 2: Correlation Matrix
    add_plot_section(
        "Pairwise Correlation Matrix (Pearson Heatmap)",
        "correlation_matrix.png",
        "Heatmap showing strong positive covariance between murder and assault rates, validating the clustering weights."
    )

    story.append(PageBreak())

    # Plot 3: Feature Distribution
    add_plot_section(
        "Feature Distributions (Kernel Density Plots)",
        "crime_distribution.png",
        "Probability density and histogram curves for input features (Population, Murder, Assault, Theft) confirming standard scaling eligibility."
    )

    # Plot 4: Clustering Results
    add_plot_section(
        "Dimensional Clustering Results (K-Means 3D Projections)",
        "clustering_results.png",
        "Pairwise scatter plots representing nodes colored by cohort. It confirms clean separations with tight cluster density."
    )
    
    # Plot 5: Risk Distribution
    add_plot_section(
        "Risk Cohort Distribution",
        "risk_distribution.png",
        "Bar chart showing the census of cities falling into Safe, Moderate Risk, and High-Risk categories."
    )

    story.append(PageBreak())

    # ==========================================
    # SECTION 5: STATISTICAL SUMMARIES & DATA MATRIX
    # ==========================================
    story.append(Paragraph("5. Municipal Risk Analytics Matrix", h1_style))
    story.append(Paragraph(
        "Below are the aggregated cohort summaries and the complete dataset of 50 Pakistani cities sorted by "
        "their calculated Crime Severity Index Score. This table is dynamically parsed and served via the dashboard's REST APIs.", body_style
    ))
    
    # 5A: Aggregated Stats Table
    story.append(Paragraph("<b>Cohort Summary Statistics (Risk Group Averages):</b>", h2_style))
    
    try:
        df_stats = pd.read_csv(stats_csv)
        stats_data = [["Risk Cohort", "City Count", "Avg Pop", "Avg Murder", "Avg Assault", "Avg Theft", "Avg Score"]]
        for _, row in df_stats.iterrows():
            stats_data.append([
                clean_emojis(row.iloc[0]),
                str(int(row['City Count'])),
                f"{row['Population']:,.1f}",
                f"{row['Murder Rate']:.2f}",
                f"{row['Assault Rate']:.2f}",
                f"{row['Theft Rate']:.2f}",
                f"{row['Crime Score']:.2f}"
            ])
            
        t_stats = Table(stats_data, colWidths=[100, 60, 80, 75, 75, 75, 75])
        t_stats.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), c_indigo),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BACKGROUND', (0,1), (-1,-1), c_light_bg),
            ('GRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 8.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_stats)
    except Exception as e:
        story.append(Paragraph(f"Error loading summary statistics table: {str(e)}", body_style))
        
    story.append(Spacer(1, 15))

    # 5B: Full Cities Table (Grouped or ordered by Crime Score descending)
    story.append(Paragraph("<b>Detailed Jurisdiction Database (N=50):</b>", h2_style))
    
    try:
        df_cities = pd.read_csv(results_csv)
        # Sort by Crime Score descending
        df_cities = df_cities.sort_values(by='Crime Score', ascending=False)
        
        # Col widths sum to 540
        # City (100), Population (75), Murder (65), Assault (65), Theft (65), Crime Score (75), Cohort (95)
        cities_data = [["City Name", "Population", "Murder Rate", "Assault Rate", "Theft Rate", "Crime Score", "Cohort Label"]]
        
        for _, row in df_cities.iterrows():
            cohort_name = clean_emojis(row['Risk Level'])
            cities_data.append([
                row['City'],
                f"{int(row['Population']):,}",
                f"{row['Murder Rate']:.2f}",
                f"{row['Assault Rate']:.2f}",
                f"{row['Theft Rate']:.2f}",
                f"{row['Crime Score']:.2f}",
                cohort_name
            ])
            
        t_cities = Table(cities_data, colWidths=[100, 75, 65, 65, 65, 75, 95], repeatRows=1)
        
        # Setup specific styles for cells to color code the cohort labels
        t_styles = [
            ('BACKGROUND', (0,0), (-1,0), c_indigo),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('ALIGN', (0,0), (-1,0), 'CENTER'),
            ('ALIGN', (0,1), (0,-1), 'LEFT'), # Left align city name
            ('ALIGN', (1,1), (-1,-1), 'CENTER'), # Center other data
            ('GRID', (0,0), (-1,-1), 0.5, c_border),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
        ]
        
        # Dynamically color the Cohort cells (column index 6, row index starting from 1)
        for i in range(1, len(cities_data)):
            cohort = cities_data[i][6]
            if "High-Risk" in cohort:
                t_styles.append(('TEXTCOLOR', (6, i), (6, i), colors.HexColor("#B91C1C"))) # Red
                t_styles.append(('FONTNAME', (6, i), (6, i), 'Helvetica-Bold'))
            elif "Moderate" in cohort:
                t_styles.append(('TEXTCOLOR', (6, i), (6, i), colors.HexColor("#D97706"))) # Amber
                t_styles.append(('FONTNAME', (6, i), (6, i), 'Helvetica-Bold'))
            elif "Safe" in cohort:
                t_styles.append(('TEXTCOLOR', (6, i), (6, i), colors.HexColor("#047857"))) # Green
                t_styles.append(('FONTNAME', (6, i), (6, i), 'Helvetica-Bold'))
                
        t_cities.setStyle(TableStyle(t_styles))
        story.append(t_cities)
    except Exception as e:
        story.append(Paragraph(f"Error loading cities database table: {str(e)}", body_style))

    story.append(PageBreak())

    # ==========================================
    # SECTION 6: Q&A DEFENSE
    # ==========================================
    story.append(Paragraph("6. Project Defense &amp; Interview talking points", h1_style))
    story.append(Paragraph(
        "Below are key developer QA talking points designed to help present this project to hiring managers, "
        "senior engineers, or academic reviewers, demonstrating both ML engineering and design systems proficiency.", body_style
    ))
    
    qa_list = [
        ("Why use K-Means clustering instead of an alternative algorithm like DBSCAN?",
         "K-Means is selected because it is computationally efficient (O(n*k*d)) and generates convex, spherical partitioning boundaries, which align perfectly with quantitative policy benchmarks (like classification into High, Moderate, and Low tiers). DBSCAN, while excellent for spatial cluster maps with density anomalies, handles high-density differences and boundary noise unpredictably, often labeling cities as outliers rather than assigning a risk bucket."),
         
        ("What is the engineering importance of serialization (.pkl) files?",
         "In a production system, running StandardScaler scaling fits or model fittings on every HTTP request is highly inefficient. We fit the data transformers and models once offline, serialize them using Python's <code>pickle</code> package to disk (<code>scaler.pkl</code>, <code>kmeans_model.pkl</code>), and load them instantly into memory in the web backend. This decouples the training pipeline from the serving pipeline, reducing inference overhead from milliseconds to microseconds."),
         
        ("Explain the custom crime index score and why it is calculated.",
         "Unsupervised clustering creates mathematical groups (labeled 0, 1, 2) but lacks semantic context. To map numerical clusters (0, 1, 2) to qualitative indicators (Safe, Moderate, High), we compute a severity-weighted score where Murder carries 3x weight, Assault 2x weight, and Theft 1x weight. We calculate this index for the cluster centroids and rank them, assigning labels systematically and removing human bias from category mapping."),
         
        ("How does the dashboard support an 'Offline Mode'?",
         "The dashboard is built to function serverless and static. If Flask is not running, the JavaScript framework (<code>main.js</code>) intercepts failures, falling back to a static embedded dataset copy. It supports search queries, sort indicators, and table pagination completely client-side in the browser, ensuring the portfolio project remains presentable even when hosted as a static GitHub Pages site without a Python runtime backend."),
         
        ("How was UI contrast and design system premium look achieved?",
         "The platform adheres to corporate SaaS layout guides (Microsoft Fabric, Datadog). We avoided standard CSS frameworks like Bootstrap in favor of custom Vanilla CSS. We styled subtle card background colors, custom SVG logos, glassmorphic bento blocks, and clean typography layouts (using Google Fonts Space Grotesk and Inter). Dark/Light toggle utilizes CSS custom property tokens, preserving user preference and maximizing visual accessibility.")
    ]
    
    for q, a in qa_list:
        story.append(Paragraph(f"<b>Q: {q}</b>", h2_style))
        story.append(Paragraph(f"<i>A:</i> {a}", body_style))
        story.append(Spacer(1, 6))
        
    # Build the document
    try:
        doc.build(story, canvasmaker=NumberedCanvas)
        print("[SUCCESS] PDF compiled successfully at: 3C_Intelligence_Portfolio_Case_Study.pdf")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to compile PDF document: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    build_pdf()
