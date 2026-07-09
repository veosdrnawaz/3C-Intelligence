import os
import sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle

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

class ShowcaseCanvas(canvas.Canvas):
    """
    Sleek custom canvas for the Fiverr portfolio PDF showcase.
    Draws modern borders, headers, and page numbering on a 2-page layout.
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        
        # Primary palette color
        c_indigo = colors.HexColor("#4F46E5")
        c_gray = colors.HexColor("#9CA3AF")
        
        # Sleek top header bar on both pages
        self.setFillColor(c_indigo)
        self.rect(36, 756, 540, 4, fill=True, stroke=False)
        
        # Header text
        self.setFont("Helvetica-Bold", 8)
        self.drawString(36, 764, "PORTFOLIO SHOWCASE")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        self.drawString(155, 764, "|   3C Intelligence  •  Data Science & Full-Stack Application")
        
        # Bottom rule
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)
        
        # Footer text
        self.setFont("Helvetica", 7.5)
        self.setFillColor(c_gray)
        self.drawString(36, 30, "Developed by Professional Full-Stack AI Engineer")
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        
        self.restoreState()


def build_showcase_pdf(output_filename="portfolio/3C_Intelligence_Project_Showcase.pdf"):
    print("[PORTFOLIO PDF] Initializing Showcase PDF Generation...")
    
    # Paths (two dirnames up because the script will be in portfolio/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    plots_dir = os.path.join(base_dir, 'static', 'plots')
    
    results_csv = os.path.join(data_dir, 'city_crime_clustering_results.csv')
    stats_csv = os.path.join(data_dir, 'risk_level_statistics.csv')
    
    if not (os.path.exists(results_csv) and os.path.exists(stats_csv)):
        print("[ERROR] CSV data files not found in data/. Run city_crime_clustering.py first!")
        return False

    # Initialize Document (Letter size, 0.5-inch margins, top/bottom adjusted for showcase headers)
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_indigo = colors.HexColor("#4F46E5")
    c_cyan = colors.HexColor("#06B6D4")
    c_dark = colors.HexColor("#111827")
    c_gray = colors.HexColor("#374151")
    c_light_bg = colors.HexColor("#F9FAFB")
    c_border = colors.HexColor("#E5E7EB")
    
    # Styles for portfolio flyer
    title_style = ParagraphStyle(
        'ShowcaseTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_indigo,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'ShowcaseSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-BoldOblique',
        fontSize=11,
        leading=14,
        textColor=c_gray,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'ShowcaseH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_indigo,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ShowcaseBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_gray,
        spaceAfter=8
    )
    
    caption_style = ParagraphStyle(
        'ShowcaseCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#4B5563"),
        alignment=1,
        spaceBefore=3,
        spaceAfter=8
    )

    story = []

    # ==========================================
    # PAGE 1: CASE STUDY OVERVIEW & SOLUTION
    # ==========================================
    
    # Header Logo Graphic
    logo = Drawing(60, 24)
    logo.add(Rect(0, 0, 60, 24, fillColor=None, strokeColor=None))
    logo.add(Line(10, 12, 30, 12, strokeColor=colors.HexColor("#C7D2FE"), strokeWidth=2))
    logo.add(Line(30, 12, 50, 12, strokeColor=colors.HexColor("#A7F3D0"), strokeWidth=2))
    logo.add(Circle(10, 12, 5, fillColor=c_indigo, strokeColor=None))
    logo.add(Circle(30, 12, 5, fillColor=colors.HexColor("#10B981"), strokeColor=None))
    logo.add(Circle(50, 12, 5, fillColor=colors.HexColor("#EF4444"), strokeColor=None))
    story.append(logo)
    
    story.append(Paragraph("3C INTELLIGENCE", title_style))
    story.append(Paragraph("AI-Powered Urban Risk Engine &amp; Interactive SaaS Dashboard", subtitle_style))
    
    # 2-Column Overview Layout (Goals, Challenges vs Tech Stack, Stats)
    overview_text_left = []
    
    overview_text_left.append(Paragraph("<b>🎯 Project Goals</b>", h1_style))
    overview_text_left.append(Paragraph(
        "To build a reproducible data pipeline and unsupervised machine learning clustering model "
        "that partitions 50 municipal jurisdictions into distinct risk cohorts based on crime rates "
        "and population, providing policy-makers with an actionable risk assessment tool.", body_style
    ))
    
    overview_text_left.append(Paragraph("<b>⚡ Key Challenges</b>", h1_style))
    overview_text_left.append(Paragraph(
        "Raw municipal demographics differed by magnitudes (millions vs units). Furthermore, "
        "standard clustering groups are mathematical and require severity-weighted labels "
        "without human intervention or bias.", body_style
    ))
    
    overview_text_left.append(Paragraph("<b>🛠️ Engineering Solutions</b>", h1_style))
    overview_text_left.append(Paragraph(
        "Applied Z-score normalization (<code>StandardScaler</code>) before fitting a <code>K-Means</code> model. "
        "Identified the optimal cluster count (K=3) via Elbow and Silhouette verification scans, "
        "and implemented a custom crime severity score index to map clusters to <b>Safe</b>, "
        "<b>Moderate Risk</b>, and <b>High-Risk</b> categories. The model and scales are serialized to "
        "disk for instantaneous, production-ready Flask API serving.", body_style
    ))
    
    # Right Column: Tech Stack & Key Metrics Card
    tech_metrics_right = []
    
    # Styled Tech Stack box
    tech_table_data = [
        [Paragraph("<b>CORE TECH STACK</b>", ParagraphStyle('TechTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=1))],
        [Paragraph("• <b>Machine Learning:</b> Python, Scikit-Learn, NumPy, Pandas", ParagraphStyle('TechCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_gray))],
        [Paragraph("• <b>Backend Framework:</b> Flask API, Python Server, Pickle serialization", ParagraphStyle('TechCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_gray))],
        [Paragraph("• <b>Visualizations:</b> Matplotlib, Seaborn Pipeline Plots", ParagraphStyle('TechCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_gray))],
        [Paragraph("• <b>Dashboard UI:</b> HTML5, Custom Vanilla CSS Grid/Flexbox, JavaScript", ParagraphStyle('TechCell', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=c_gray))]
    ]
    t_tech = Table(tech_table_data, colWidths=[240])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_indigo),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,1), (-1,-1), c_light_bg),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    
    tech_metrics_right.append(t_tech)
    tech_metrics_right.append(Spacer(1, 15))
    
    # Styled Stats Card
    stats_table_data = [
        [Paragraph("<b>PROJECT PERFORMANCE METRICS</b>", ParagraphStyle('StatsTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=1))],
        [Paragraph("<b>50</b><br/><font size=7 color='#6B7280'>CITIES ANALYZED</font>", ParagraphStyle('StatNum', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=14, alignment=1, textColor=c_dark))],
        [Paragraph("<b>0.74</b><br/><font size=7 color='#6B7280'>SILHOUETTE SCORE</font>", ParagraphStyle('StatNum', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=14, alignment=1, textColor=colors.HexColor("#059669")))],
        [Paragraph("<b>K = 3</b><br/><font size=7 color='#6B7280'>OPTIMAL CLUSTERS</font>", ParagraphStyle('StatNum', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=14, alignment=1, textColor=c_indigo))],
        [Paragraph("<b>&lt;10ms</b><br/><font size=7 color='#6B7280'>API LATENCY</font>", ParagraphStyle('StatNum', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=14, alignment=1, textColor=colors.HexColor("#DC2626")))]
    ]
    t_stats = Table(stats_table_data, colWidths=[240])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_indigo),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('ALIGN', (0,1), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
    ]))
    
    tech_metrics_right.append(t_stats)

    # Place in a master 2-column layout
    master_columns = [
        [overview_text_left, tech_metrics_right]
    ]
    t_master = Table(master_columns, colWidths=[280, 260])
    t_master.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(t_master)
    story.append(PageBreak())

    # ==========================================
    # PAGE 2: VISUAL RESULTS & CALL TO ACTION
    # ==========================================
    story.append(Paragraph("Visual Diagnostics &amp; Business Outcomes", title_style))
    story.append(Paragraph("Below are key plots exported from our offline data science training pipeline, alongside aggregated statistical groupings that populate our real-time database.", subtitle_style))
    
    # 2-Column Plots Layout
    plots_row = []
    
    # Left Plot
    plot_left = []
    img_path_1 = os.path.join(plots_dir, "clustering_results.png")
    if os.path.exists(img_path_1):
        plot_left.append(Image(img_path_1, width=2.9*inch, height=2.175*inch))
        plot_left.append(Paragraph("Figure 1: K-Means cluster separation showing clear risk cohort boundaries.", caption_style))
    else:
        plot_left.append(Paragraph("[Clustering results plot missing]", caption_style))
        
    # Right Plot
    plot_right = []
    img_path_2 = os.path.join(plots_dir, "risk_distribution.png")
    if os.path.exists(img_path_2):
        plot_right.append(Image(img_path_2, width=2.9*inch, height=2.175*inch))
        plot_right.append(Paragraph("Figure 2: Distribution of jurisdictions inside the Safe, Moderate, and High-Risk categories.", caption_style))
    else:
        plot_right.append(Paragraph("[Risk distribution plot missing]", caption_style))
        
    t_plots = Table([[plot_left, plot_right]], colWidths=[270, 270])
    t_plots.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_plots)
    story.append(Spacer(1, 5))

    # Aggregated Stats Table
    story.append(Paragraph("<b>Aggregated Risk Level Statistics:</b>", h1_style))
    try:
        df_stats = pd.read_csv(stats_csv)
        stats_data = [["Cohort", "Cities", "Avg Population", "Avg Murder", "Avg Assault", "Avg Theft", "Avg Crime Index"]]
        for _, row in df_stats.iterrows():
            stats_data.append([
                clean_emojis(row.iloc[0]),
                str(int(row['City Count'])),
                f"{row['Population']:,.0f}",
                f"{row['Murder Rate']:.1f}",
                f"{row['Assault Rate']:.1f}",
                f"{row['Theft Rate']:.1f}",
                f"{row['Crime Score']:.1f}"
            ])
            
        t_summary = Table(stats_data, colWidths=[100, 45, 85, 75, 75, 75, 85])
        t_summary.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), c_indigo),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 8.5),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BACKGROUND', (0,1), (-1,-1), c_light_bg),
            ('GRID', (0,0), (-1,-1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light_bg]),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_summary)
    except Exception as e:
        story.append(Paragraph(f"Error loading summary table: {str(e)}", body_style))

    story.append(Spacer(1, 10))

    # Hire Me Callout Box (Beautifully styled)
    callout_data = [
        [
            Paragraph(
                "<b>💡 HIRE ME FOR YOUR PROJECT!</b><br/>"
                "Are you looking to integrate advanced machine learning models into interactive full-stack dashboards? "
                "I specialize in building end-to-end data analytics applications, custom prediction APIs, and beautiful "
                "responsive dashboards (Light/Dark themes). I guarantee high performance, pixel-perfect design, clean code, "
                "and production-ready deployable applications.<br/>"
                "<b>Contact me today to discuss your project requirements!</b>",
                ParagraphStyle('CalloutText', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13.5, textColor=c_gray)
            )
        ]
    ]
    t_callout = Table(callout_data, colWidths=[540])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2F6")),
        ('BORDER', (0,0), (-1,-1), 1.5, c_indigo),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    
    story.append(KeepTogether(t_callout))

    # Compile PDF
    try:
        doc.build(story, canvasmaker=ShowcaseCanvas)
        print(f"[SUCCESS] Fiverr Portfolio Showcase PDF generated at: {output_filename}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to compile Fiverr PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    build_showcase_pdf()
