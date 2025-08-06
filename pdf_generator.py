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
    
    # Header with improved layout - logo on left, info centered
    header_data = [
        [
            # Logo placeholder (left)
            Paragraph(
                '<b><font color="white" backColor="#FF0000" size="14">&nbsp;SENAI&nbsp;</font></b><br/>'
                '<font size="8">Serviço Nacional de<br/>Aprendizagem Industrial</font>',
                normal_style
            ),
            # Center content
            Paragraph(
                '<b>BOLETIM ESCOLAR</b><br/>'
                'SENAI Morvan Figueiredo<br/>'
                '<font size="8">Sistema de Avaliação Acadêmica</font>',
                title_style
            ),
            # Date (right)
            Paragraph(
                f'<font size="10"><b>Data:</b><br/>{datetime.now().strftime("%d/%m/%Y")}</font>',
                normal_style
            )
        ]
    ]
    
    header_table = Table(header_data, colWidths=[5*cm, 9*cm, 3*cm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),    # Logo left
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Title center
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),   # Date right
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#FF0000')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#FF0000')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
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
        ['Disciplina', 'Professor', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota Final', 'Faltas (%)', 'Situação']
    ]
    
    # Add grade rows with calculated final grade and updated criteria
    for grade in grades:
        # Calculate final grade as average
        final_grade = grade.calculated_final_grade
        
        # Calculate absence percentage
        absence_percentage = (grade.absences / grade.subject.workload) * 100 if grade.subject.workload > 0 else 0
        
        # Determine status with new criteria
        if final_grade is None:
            status = "Pendente"
        elif final_grade >= 50 and absence_percentage <= 25:
            status = "Aprovado"
        else:
            reasons = []
            if final_grade < 50:
                reasons.append("Nota")
            if absence_percentage > 25:
                reasons.append("Faltas")
            status = f"Reprovado ({', '.join(reasons)})"
        
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
    
    grade_table = Table(grade_data, colWidths=[2.2*inch, 1.2*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.7*inch, 0.9*inch, 0.8*inch])
    grade_table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        
        # Data rows
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Alternating row colors
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F8F8')]),
        
        # Subject and teacher name alignment
        ('ALIGN', (0, 1), (1, -1), 'LEFT'),
    ]))
    
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
