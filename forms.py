from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, NumberRange, Length
from models import Student, Subject

class StudentForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)])
    registration_number = StringField('Número de Matrícula', validators=[DataRequired(), Length(min=1, max=20)])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    course = StringField('Curso', validators=[DataRequired(), Length(max=100)], 
                        default="Técnico em Desenvolvimento de Sistemas")
    submit = SubmitField('Salvar')

class SubjectForm(FlaskForm):
    name = StringField('Nome da Disciplina', validators=[DataRequired(), Length(min=2, max=100)])
    code = StringField('Código', validators=[DataRequired(), Length(min=1, max=20)])
    workload = IntegerField('Carga Horária (horas)', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    teacher_name = StringField('Professor', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Salvar')

class GradeForm(FlaskForm):
    student_id = SelectField('Aluno', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Disciplina', coerce=int, validators=[DataRequired()])
    grade_1 = FloatField('Nota 1', validators=[Optional(), NumberRange(min=0, max=100)])
    grade_2 = FloatField('Nota 2', validators=[Optional(), NumberRange(min=0, max=100)])
    grade_3 = FloatField('Nota 3', validators=[Optional(), NumberRange(min=0, max=100)])
    absences = IntegerField('Faltas', validators=[Optional(), NumberRange(min=0, max=200)], default=0)
    submit = SubmitField('Salvar')
    
    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        self.student_id.choices = [(s.id, s.name) for s in Student.query.order_by(Student.name).all()]
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.order_by(Subject.name).all()]

class ExcelUploadForm(FlaskForm):
    excel_file = FileField('Planilha Excel', validators=[
        FileRequired('Selecione um arquivo'),
        FileAllowed(['xls', 'xlsx'], 'Apenas arquivos Excel (.xls, .xlsx) são permitidos')
    ])
    course = StringField('Curso', validators=[DataRequired(), Length(max=100)], 
                        default="Técnico em Desenvolvimento de Sistemas")
    submit = SubmitField('Importar Alunos')
