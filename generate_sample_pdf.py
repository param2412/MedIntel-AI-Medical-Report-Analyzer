"""Generate a sample medical PDF for testing and demonstration."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os


def create_sample_medical_pdf(output_path: str = "data/uploaded_reports/sample_report.pdf") -> str:
    """
    Create a sample medical report PDF for testing extraction and parsing.
    
    Args:
        output_path: Path where the PDF will be saved
        
    Returns:
        Path to the created PDF file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        alignment=1  # Center
    )
    story.append(Paragraph("MEDICAL LABORATORY REPORT", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Patient info
    patient_info = [
        ['Patient Name:', 'John Doe'],
        ['Date of Birth:', '01/15/1985'],
        ['Patient ID:', 'MED-2026-12345'],
        ['Report Date:', datetime.now().strftime("%m/%d/%Y")],
        ['Ordering Physician:', 'Dr. Jane Smith, MD'],
    ]
    
    t = Table(patient_info, colWidths=[2*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#003366')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*inch))
    
    # Blood work results
    story.append(Paragraph("COMPLETE BLOOD COUNT (CBC)", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))
    
    cbc_data = [
        ['Test', 'Value', 'Reference Range', 'Unit', 'Flag'],
        ['Hemoglobin', '10.5', '13.5-17.5', 'g/dL', 'L'],
        ['Hematocrit', '31.2', '41-53', '%', 'L'],
        ['WBC (White Blood Cell Count)', '14000', '4500-11000', '/µL', 'H'],
        ['RBC (Red Blood Cell Count)', '4.2', '4.5-5.9', 'M/µL', 'L'],
        ['Platelet Count', '450000', '150000-400000', '/µL', 'H'],
        ['MCV (Mean Corpuscular Volume)', '72', '80-100', 'fL', 'L'],
    ]
    
    t2 = Table(cbc_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 0.8*inch, 0.5*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.3*inch))
    
    # Metabolic panel
    story.append(Paragraph("COMPREHENSIVE METABOLIC PANEL (CMP)", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))
    
    cmp_data = [
        ['Test', 'Value', 'Reference Range', 'Unit', 'Flag'],
        ['Glucose', '105', '70-100', 'mg/dL', 'H'],
        ['BUN (Blood Urea Nitrogen)', '22', '7-20', 'mg/dL', 'H'],
        ['Creatinine', '1.1', '0.7-1.3', 'mg/dL', ''],
        ['Sodium', '138', '135-145', 'mEq/L', ''],
        ['Potassium', '4.2', '3.5-5.0', 'mEq/L', ''],
        ['Chloride', '102', '98-107', 'mEq/L', ''],
    ]
    
    t3 = Table(cmp_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 0.8*inch, 0.5*inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    story.append(t3)
    story.append(Spacer(1, 0.3*inch))
    
    # Clinical notes
    story.append(Paragraph("CLINICAL NOTES", styles['Heading2']))
    story.append(Spacer(1, 0.15*inch))
    notes = """
    Patient presents with symptoms of anemia and elevated white blood cell count. 
    Hemoglobin and hematocrit levels are below normal range, indicating possible iron deficiency anemia. 
    WBC count is elevated, suggesting possible infection or inflammatory response. 
    Glucose level is mildly elevated; recommend dietary modifications and follow-up testing in 2 weeks.
    """
    story.append(Paragraph(notes, styles['BodyText']))
    
    doc.build(story)
    return output_path


if __name__ == "__main__":
    pdf_path = create_sample_medical_pdf()
    print(f"✓ Sample medical PDF created at: {pdf_path}")
