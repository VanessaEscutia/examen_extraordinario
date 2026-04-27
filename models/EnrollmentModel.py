from extensions import db


enrollments = db.Table(
    'enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('alumnos.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True),
)