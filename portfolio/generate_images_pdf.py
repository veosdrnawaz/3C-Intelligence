import os
import sys
from reportlab.lib import colors
from reportlab.pdfgen import canvas

# Ensure stdout uses UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def build_images_pdf(output_filename="portfolio/3C_Intelligence_Visual_Showcase.pdf"):
    print("[VISUAL PDF] Starting compilation of Visual Preview PDF via Canvas...")
    
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plots_dir = os.path.join(base_dir, 'static', 'plots')
    portfolio_dir = os.path.join(base_dir, 'portfolio')
    
    dashboard_img = os.path.join(portfolio_dir, 'dashboard_screenshot.png')
    
    # List of images to include in the visual showcase
    images_list = [
        # Image path, Background Color
        (dashboard_img, colors.HexColor("#F8FAFC")), # Light background for the dashboard
        (os.path.join(plots_dir, 'clustering_results.png'), colors.HexColor("#FDFDFD")),
        (os.path.join(plots_dir, 'crime_distribution.png'), colors.HexColor("#FDFDFD")),
        (os.path.join(plots_dir, 'correlation_matrix.png'), colors.HexColor("#FDFDFD")),
        (os.path.join(plots_dir, 'risk_distribution.png'), colors.HexColor("#FDFDFD"))
    ]
    
    # Custom Page size: 1024 x 768 points (Fiverr's recommended 4:3 size)
    c = canvas.Canvas(output_filename, pagesize=(1024, 768))
    
    pages_created = 0
    for img_path, bg_color in images_list:
        if not os.path.exists(img_path):
            print(f"[WARNING] Image not found: {img_path}")
            continue
            
        # Draw background color
        c.setFillColor(bg_color)
        c.rect(0, 0, 1024, 768, fill=True, stroke=False)
        
        # Draw image centered
        try:
            if "dashboard_screenshot" in img_path:
                # Full bleed layout for the dashboard preview
                c.drawImage(img_path, 0, 0, width=1024, height=768)
            else:
                # Centered layout with nice padding for the plots
                c.drawImage(img_path, 32, 24, width=960, height=720)
                
            c.showPage()
            pages_created += 1
            print(f"[PORTFOLIO PDF] Added page {pages_created}: {os.path.basename(img_path)}")
        except Exception as e:
            print(f"[ERROR] Failed to draw image {os.path.basename(img_path)}: {str(e)}")
            
    # Save PDF
    try:
        c.save()
        print(f"[SUCCESS] Visual Showcase PDF generated at: {output_filename} ({pages_created} pages)")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save canvas PDF: {str(e)}")
        return False

if __name__ == "__main__":
    build_images_pdf()
