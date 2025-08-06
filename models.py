from app import db
from datetime import datetime
from sqlalchemy import func

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    registration_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    course = db.Column(db.String(100), nullable=False, default="Técnico em Desenvolvimento de Sistemas")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with grades
    grades = db.relationship('Grade', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.name}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    workload = db.Column(db.Integer, nullable=False, default=60)  # Hours
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with grades
    grades = db.relationship('Grade', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.name}>'

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    
    # Grades
    grade_1 = db.Column(db.Float, nullable=True)
    grade_2 = db.Column(db.Float, nullable=True)
    grade_3 = db.Column(db.Float, nullable=True)
    final_grade = db.Column(db.Float, nullable=True)
    
    # Attendance
    absences = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint to prevent duplicate grades for same student-subject
    __table_args__ = (db.UniqueConstraint('student_id', 'subject_id', name='unique_student_subject'),)
    
    @property
    def is_approved(self):
        """Check if student is approved (final grade >= 50 and absences <= 20)"""
        if self.final_grade is None:
            return False
        return self.final_grade >= 50 and self.absences <= 20
    
    @property
    def status(self):
        """Get approval status as string"""
        if self.final_grade is None:
            return "Pendente"
        elif self.is_approved:
            return "Aprovado"
        else:
            reasons = []
            if self.final_grade < 50:
                reasons.append("Nota insuficiente")
            if self.absences > 20:
                reasons.append("Excesso de faltas")
            return f"Reprovado ({', '.join(reasons)})"
    
    def __repr__(self):
        return f'<Grade {self.id}>'
