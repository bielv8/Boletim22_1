from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch, cm
from datetime import datetime
import io
import os

def generate_bulletin_pdf(student, grades):
    """Generate PDF bulletin for a student"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        topMargin=1.5*cm, 
        bottomMargin=1.5*cm,
        leftMargin=2*cm, 
        rightMargin=2*cm
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=10,
        alignment=1,  # Center
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.HexColor('#FF0000'),
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # Build content
    content = []
    
    # Professional SENAI header styles
    logo_style = ParagraphStyle(
        'LogoStyle',
        parent=styles['Normal'],
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        alignment=1,  # Center
        leading=18
    )
    
    center_title_style = ParagraphStyle(
        'CenterTitleStyle',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        alignment=1,  # Center
        leading=16
    )
    
    center_subtitle_style = ParagraphStyle(
        'CenterSubtitleStyle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica',
        textColor=colors.white,
        alignment=1,  # Center
        leading=13
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        alignment=2,  # Right
        leading=16
    )
    
    # Create three-column layout: Logo | Center Content | Date
    # Real SENAI logo (left)
    try:
        logo_path = os.path.join('static', 'images', 'logo-senai.png')
        if os.path.exists(logo_path):
            logo_img = Image(logo_path, width=3*cm, height=0.8*cm)
            logo_content = logo_img
        else:
            # Fallback to text logo if image not found
            logo_content = Paragraph(
                '<font size="14"><b>███ SENAI ███</b></font>',
                logo_style
            )
    except Exception:
        # Fallback to text logo if there's any error
        logo_content = Paragraph(
            '<font size="14"><b>███ SENAI ███</b></font>',
            logo_style
        )
    
    # Center content with proper spacing and hierarchy
    center_content = Paragraph(
        '<font size="12"><b>Serviço Nacional de Aprendizagem</b></font><br/>'
        '<font size="12"><b>Industrial</b></font><br/>'
        '<br/>'
        '<font size="18"><b>BOLETIM ESCOLAR</b></font><br/>'
        '<font size="14"><b>SENAI Morvan Figueiredo</b></font>',
        center_title_style
    )
    
    # Date (right) - simplified format
    date_content = Paragraph(
        f'<font size="16"><b>{datetime.now().strftime("%d/%m/")}</b></font><br/>'
        f'<font size="16"><b>{datetime.now().strftime("%Y")}</b></font>',
        date_style
    )
    
    # Create header table with balanced three columns optimized for logo
    header_data = [[logo_content, center_content, date_content]]
    header_table = Table(header_data, colWidths=[4*cm, 9*cm, 4*cm])
    
    # Determine if we're using image or text logo for styling
    logo_valign = 'MIDDLE'
    logo_padding = 15
    if isinstance(logo_content, Image):
        logo_valign = 'MIDDLE'
        logo_padding = 20
    
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FF0000')),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),     # Logo left aligned in its cell
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),   # Center content centered
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),    # Date right aligned in its cell
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 25),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 25),
        ('LEFTPADDING', (0, 0), (0, 0), logo_padding),    # Logo padding
        ('LEFTPADDING', (1, 0), (1, 0), 15),              # Center padding
        ('LEFTPADDING', (2, 0), (2, 0), 15),              # Date padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    
    content.append(header_table)
    content.append(Spacer(1, 25))
    
    # Student information in clean table format like the image
    student_info_style = ParagraphStyle(
        'StudentInfo',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica',
        leftIndent=10,
        rightIndent=10
    )
    
    student_label_style = ParagraphStyle(
        'StudentLabel',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        leftIndent=10,
        rightIndent=10
    )
    
    student_info = [
        [Paragraph('<b>Nome do Aluno:</b>', student_label_style), Paragraph(student.name, student_info_style)],
        [Paragraph('<b>Matrícula:</b>', student_label_style), Paragraph(student.registration_number, student_info_style)],
        [Paragraph('<b>Curso:</b>', student_label_style), Paragraph(student.course, student_info_style)],
        [Paragraph('<b>Data de Emissão:</b>', student_label_style), Paragraph(datetime.now().strftime('%d/%m/%Y'), student_info_style)]
    ]
    
    student_table = Table(student_info, colWidths=[4.5*cm, 12.5*cm])
    student_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F8F8')),
    ]))
    
    content.append(student_table)
    content.append(Spacer(1, 25))
    
    # Section title with red icon like in the image
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#FF0000'),
        spaceAfter=15
    )
    
    content.append(Paragraph('📋 Notas e Frequência', section_title_style))
    
    # Table headers
    grade_data = [
        ['Disciplina', 'Professor', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota Final', 'Faltas (%)', 'Situação']
    ]
    
    # Add grade rows with calculated final grade and updated criteria
    for grade in grades:
        # Calculate final grade as average
        final_grade = grade.calculated_final_grade
        
        # Calculate absence percentage
        absence_percentage = (grade.absences / grade.subject.workload) * 100 if grade.subject.workload > 0 else 0
        
        # Determine status with new criteria - simpler format for PDF
        if final_grade is None:
            status = "Pendente"
        elif final_grade >= 50 and absence_percentage <= 25:
            status = "Aprovado"
        else:
            status = "Reprovado"
        
        grade_data.append([
            grade.subject.name,
            grade.subject.teacher_name or "-",
            f"{grade.grade_1:.1f}" if grade.grade_1 is not None else "-",
            f"{grade.grade_2:.1f}" if grade.grade_2 is not None else "-",
            f"{grade.grade_3:.1f}" if grade.grade_3 is not None else "-",
            f"{final_grade:.1f}" if final_grade is not None else "-",
            f"{grade.absences} ({absence_percentage:.0f}%)",
            status
        ])
    
    grade_table = Table(grade_data, colWidths=[4*cm, 3*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.8*cm, 2*cm, 2.2*cm])
    
    # Apply styles to make it look like the image
    table_style = [
        # Header style - clean white background with black text
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F0F0F0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        
        # Subject name alignment
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
    ]
    
    # Apply conditional formatting for approved status (green background)
    for i, row in enumerate(grade_data[1:], 1):
        if len(row) > 7 and row[7] == "Aprovado":
            table_style.append(('BACKGROUND', (7, i), (7, i), colors.HexColor('#4CAF50')))
            table_style.append(('TEXTCOLOR', (7, i), (7, i), colors.white))
    
    grade_table.setStyle(TableStyle(table_style))
    
    content.append(grade_table)
    content.append(Spacer(1, 30))
    
    # Legend
    legend_data = [
        ['<b>LEGENDA:</b>'],
        ['• <b>Aprovado:</b> Nota Final ≥ 50 (média das 3 notas) e Faltas ≤ 25% da carga horária'],
        ['• <b>Reprovado:</b> Nota Final < 50 ou Faltas > 25% da carga horária'],
        ['• <b>Pendente:</b> Aguardando lançamento das 3 notas parciais'],
        [''],
        ['<b>OBSERVAÇÕES:</b>'],
        ['• Nota Final = (Nota 1 + Nota 2 + Nota 3) ÷ 3'],
        ['• Percentual de faltas calculado sobre a carga horária total da disciplina']
    ]
    
    for item in legend_data:
        content.append(Paragraph(item[0], normal_style))
    
    content.append(Spacer(1, 30))
    
    # Footer
    footer_data = [
        [
            Paragraph('_' * 30 + '<br/>Assinatura do Responsável', normal_style),
            Paragraph('_' * 30 + '<br/>Carimbo da Instituição', normal_style)
        ]
    ]
    
    footer_table = Table(footer_data, colWidths=[3*inch, 3*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    content.append(footer_table)
    
    # Build PDF
    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()
