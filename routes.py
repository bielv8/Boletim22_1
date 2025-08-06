from flask import render_template, request, redirect, url_for, flash, send_file
from app import app, db
from models import Student, Subject, Grade
from forms import StudentForm, SubjectForm, GradeForm
from pdf_generator import generate_bulletin_pdf
import io

@app.route('/')
def index():
    """Dashboard with statistics"""
    total_students = Student.query.count()
    total_subjects = Subject.query.count()
    total_grades = Grade.query.count()
    
    # Approved students count
    approved_grades = Grade.query.filter(
        Grade.final_grade >= 50, 
        Grade.absences <= 20,
        Grade.final_grade.isnot(None)
    ).count()
    
    return render_template('index.html', 
                         total_students=total_students,
                         total_subjects=total_subjects, 
                         total_grades=total_grades,
                         approved_grades=approved_grades)

# Student routes
@app.route('/students')
def students():
    """List all students"""
    search = request.args.get('search', '')
    if search:
        students = Student.query.filter(
            Student.name.contains(search) | 
            Student.registration_number.contains(search)
        ).order_by(Student.name).all()
    else:
        students = Student.query.order_by(Student.name).all()
    
    return render_template('students.html', students=students, search=search)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    """Add new student"""
    form = StudentForm()
    if form.validate_on_submit():
        # Check if registration number already exists
        existing = Student.query.filter_by(registration_number=form.registration_number.data).first()
        if existing:
            flash('Número de matrícula já existe!', 'error')
            return render_template('add_student.html', form=form)
        
        student = Student()
        student.name = form.name.data
        student.registration_number = form.registration_number.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.course = form.course.data
        db.session.add(student)
        db.session.commit()
        flash('Aluno adicionado com sucesso!', 'success')
        return redirect(url_for('students'))
    
    return render_template('add_student.html', form=form)

@app.route('/students/<int:id>/delete', methods=['POST'])
def delete_student(id):
    """Delete student"""
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Aluno removido com sucesso!', 'success')
    return redirect(url_for('students'))

# Subject routes
@app.route('/subjects')
def subjects():
    """List all subjects"""
    subjects = Subject.query.order_by(Subject.name).all()
    return render_template('subjects.html', subjects=subjects)

@app.route('/subjects/add', methods=['GET', 'POST'])
def add_subject():
    """Add new subject"""
    form = SubjectForm()
    if form.validate_on_submit():
        # Check if code already exists
        existing = Subject.query.filter_by(code=form.code.data).first()
        if existing:
            flash('Código da disciplina já existe!', 'error')
            return render_template('add_subject.html', form=form)
        
        subject = Subject()
        subject.name = form.name.data
        subject.code = form.code.data
        subject.workload = form.workload.data
        subject.teacher_name = form.teacher_name.data
        db.session.add(subject)
        db.session.commit()
        flash('Disciplina adicionada com sucesso!', 'success')
        return redirect(url_for('subjects'))
    
    return render_template('add_subject.html', form=form)

@app.route('/subjects/<int:id>/delete', methods=['POST'])
def delete_subject(id):
    """Delete subject"""
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('Disciplina removida com sucesso!', 'success')
    return redirect(url_for('subjects'))

# Grade routes
@app.route('/grades')
def grades():
    """List all grades"""
    student_filter = request.args.get('student_id', type=int)
    subject_filter = request.args.get('subject_id', type=int)
    
    query = Grade.query
    if student_filter:
        query = query.filter_by(student_id=student_filter)
    if subject_filter:
        query = query.filter_by(subject_id=subject_filter)
    
    grades = query.order_by(Grade.student_id, Grade.subject_id).all()
    students = Student.query.order_by(Student.name).all()
    subjects = Subject.query.order_by(Subject.name).all()
    
    return render_template('grades.html', 
                         grades=grades, 
                         students=students, 
                         subjects=subjects,
                         student_filter=student_filter,
                         subject_filter=subject_filter)

@app.route('/grades/add', methods=['GET', 'POST'])
def add_grade():
    """Add new grade"""
    form = GradeForm()
    if form.validate_on_submit():
        # Check if grade already exists for this student-subject
        existing = Grade.query.filter_by(
            student_id=form.student_id.data,
            subject_id=form.subject_id.data
        ).first()
        
        if existing:
            flash('Nota já existe para este aluno e disciplina!', 'error')
            return render_template('add_grade.html', form=form)
        
        grade = Grade()
        grade.student_id = form.student_id.data
        grade.subject_id = form.subject_id.data
        grade.grade_1 = form.grade_1.data
        grade.grade_2 = form.grade_2.data
        grade.grade_3 = form.grade_3.data
        grade.final_grade = None  # Will be calculated automatically
        grade.absences = form.absences.data
        db.session.add(grade)
        db.session.commit()
        flash('Nota adicionada com sucesso!', 'success')
        return redirect(url_for('grades'))
    
    return render_template('add_grade.html', form=form)

@app.route('/grades/<int:id>/edit', methods=['GET', 'POST'])
def edit_grade(id):
    """Edit existing grade"""
    grade = Grade.query.get_or_404(id)
    form = GradeForm(obj=grade)
    
    if form.validate_on_submit():
        grade.grade_1 = form.grade_1.data
        grade.grade_2 = form.grade_2.data
        grade.grade_3 = form.grade_3.data
        grade.final_grade = None  # Will be calculated automatically
        grade.absences = form.absences.data
        db.session.commit()
        flash('Nota atualizada com sucesso!', 'success')
        return redirect(url_for('grades'))
    
    # Pre-populate form with current values
    form.student_id.data = grade.student_id
    form.subject_id.data = grade.subject_id
    
    return render_template('add_grade.html', form=form, grade=grade)

@app.route('/grades/<int:id>/delete', methods=['POST'])
def delete_grade(id):
    """Delete grade"""
    grade = Grade.query.get_or_404(id)
    db.session.delete(grade)
    db.session.commit()
    flash('Nota removida com sucesso!', 'success')
    return redirect(url_for('grades'))

# Bulletin routes
@app.route('/bulletin/<int:student_id>')
def view_bulletin(student_id):
    """View student bulletin"""
    student = Student.query.get_or_404(student_id)
    grades = Grade.query.filter_by(student_id=student_id).order_by(Grade.subject_id).all()
    
    return render_template('bulletin.html', student=student, grades=grades)

@app.route('/bulletin/<int:student_id>/pdf')
def download_bulletin_pdf(student_id):
    """Download bulletin as PDF"""
    student = Student.query.get_or_404(student_id)
    grades = Grade.query.filter_by(student_id=student_id).order_by(Grade.subject_id).all()
    
    pdf_buffer = generate_bulletin_pdf(student, grades)
    
    return send_file(
        io.BytesIO(pdf_buffer),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'boletim_{student.registration_number}_{student.name.replace(" ", "_")}.pdf'
    )

# Initialize default subjects
def create_default_subjects():
    """Create default subjects if they don't exist"""
    default_subjects = [
        {'name': 'Matemática', 'code': 'MAT001', 'workload': 80},
        {'name': 'Português', 'code': 'POR001', 'workload': 60},
        {'name': 'Biologia', 'code': 'BIO001', 'workload': 60},
        {'name': 'Programação', 'code': 'PRG001', 'workload': 120},
        {'name': 'Banco de Dados', 'code': 'BDA001', 'workload': 80},
        {'name': 'Análise de Sistemas', 'code': 'ANA001', 'workload': 100},
    ]
    
    for subject_data in default_subjects:
        existing = Subject.query.filter_by(code=subject_data['code']).first()
        if not existing:
            subject = Subject()
            subject.name = subject_data['name']
            subject.code = subject_data['code']
            subject.workload = subject_data['workload']
            subject.teacher_name = None
            db.session.add(subject)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default subjects: {e}")
