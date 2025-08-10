from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
def create_report_pdf(farmer_name, indices, advisory_text, save_path):
    doc = SimpleDocTemplate(save_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    elements.append(Paragraph(f"<b>Farm Health Report</b>", styles['Title']))
    elements.append(Paragraph(f"Farmer: {farmer_name}", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Indices table
    indices_data = [
        ['Index', 'Value', 'Interpretation'],
        ['NDVI', indices.get('NDVI', 'N/A'), get_ndvi_interpretation(indices.get('NDVI'))],
        ['NDRE', indices.get('NDRE', 'N/A'), get_ndre_interpretation(indices.get('NDRE'))],
        ['GNDVI', indices.get('GNDVI', 'N/A'), get_gndvi_interpretation(indices.get('GNDVI'))],
        ['MSI', indices.get('MSI', 'N/A'), get_msi_interpretation(indices.get('MSI'))]
    ]
    
    table = Table(indices_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgreen),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.grey)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 30))
    
    # AI Advisory
    elements.append(Paragraph("<b>AI Advisory</b>", styles['Heading2']))
    elements.append(Paragraph(advisory_text, styles['BodyText']))
    
    # Footer
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Italic']))
    
    doc.build(elements)

# Helper functions for interpretations
def get_ndvi_interpretation(value):
    if value is None: return 'N/A'
    if value > 0.7: return 'Excellent health'
    if value > 0.5: return 'Good health'
    if value > 0.3: return 'Moderate health'
    return 'Poor health'

def get_ndre_interpretation(value):
    if not value: return 'N/A'
    if value > 0.4: return 'Adequate nitrogen'
    if value > 0.3: return 'Moderate nitrogen'
    return 'Nitrogen deficient'

def get_gndvi_interpretation(value):
    if not value: return 'N/A'
    if value > 0.6: return 'High chlorophyll'
    if value > 0.4: return 'Moderate chlorophyll'
    return 'Low chlorophyll'

def get_msi_interpretation(value):
    if not value: return 'N/A'
    if value < 0.7: return 'Low water stress'
    if value < 0.9: return 'Moderate water stress'
    return 'High water stress'