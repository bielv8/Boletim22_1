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
    
    # Red header banner like in the image
    header_style_white = ParagraphStyle(
        'HeaderWhite',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        alignment=1  # Center
    )
    
    header_style_white_small = ParagraphStyle(
        'HeaderWhiteSmall',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        textColor=colors.white,
        alignment=1  # Center
    )
    
    # Create SENAI logo text with horizontal lines (similar to image)
    logo_text = Paragraph(
        '<font size="16"><b>═══ SENAI ═══</b></font><br/>'
        '<font size="10">Serviço Nacional de Aprendizagem<br/>Industrial</font><br/>'
        '<font size="14"><b>BOLETIM ESCOLAR</b></font><br/>'
        '<font size="12">SENAI Morvan Figueiredo</font>',
        header_style_white
    )
    
    # Date in top right
    date_text = Paragraph(
        f'<font size="12">{datetime.now().strftime("%d/%m/%Y")}</font>',
        header_style_white
    )
    
    # Red header table
    header_data = [[logo_text, date_text]]
    header_table = Table(header_data, colWidths=[14*cm, 3*cm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FF0000')),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
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
