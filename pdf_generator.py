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
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*cm, bottomMargin=1*cm)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=colors.HexColor('#FF0000')
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor('#FF0000')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Build content
    content = []
    
    # Header with SENAI logo (using SVG as text since we can't load actual image)
    header_data = [
        [
            Paragraph('<b>SENAI</b><br/>Serviço Nacional de<br/>Aprendizagem Industrial', header_style),
            Paragraph('<b>BOLETIM ESCOLAR</b><br/>SENAI Morvan Figueiredo', title_style)
        ]
    ]
    
    header_table = Table(header_data, colWidths=[3*inch, 4*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#FF0000')),
    ]))
    
    content.append(header_table)
    content.append(Spacer(1, 20))
    
    # Student information
    student_info = [
        ['<b>Nome do Aluno:</b>', student.name],
        ['<b>Matrícula:</b>', student.registration_number],
        ['<b>Curso:</b>', student.course],
        ['<b>Data de Emissão:</b>', datetime.now().strftime('%d/%m/%Y')]
    ]
    
    student_table = Table(student_info, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
    ]))
    
    content.append(student_table)
    content.append(Spacer(1, 20))
    
    # Grades table
    content.append(Paragraph('<b>NOTAS E FREQUÊNCIA</b>', header_style))
    content.append(Spacer(1, 10))
    
    # Table headers
    grade_data = [
        ['Disciplina', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota Final', 'Faltas', 'Situação']
    ]
    
    # Add grade rows
    for grade in grades:
        grade_data.append([
            grade.subject.name,
            f"{grade.grade_1:.1f}" if grade.grade_1 is not None else "-",
            f"{grade.grade_2:.1f}" if grade.grade_2 is not None else "-",
            f"{grade.grade_3:.1f}" if grade.grade_3 is not None else "-",
            f"{grade.final_grade:.1f}" if grade.final_grade is not None else "-",
            str(grade.absences),
            grade.status
        ])
    
    grade_table = Table(grade_data, colWidths=[2.5*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.8*inch, 0.6*inch, 1*inch])
    grade_table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F8F8')]),
        
        # Subject name alignment
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
    ]))
    
    content.append(grade_table)
    content.append(Spacer(1, 30))
    
    # Legend
    legend_data = [
        ['<b>LEGENDA:</b>'],
        ['• Aprovado: Nota Final ≥ 50 e Faltas ≤ 20'],
        ['• Reprovado: Nota Final < 50 ou Faltas > 20'],
        ['• Pendente: Aguardando lançamento da nota final']
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
