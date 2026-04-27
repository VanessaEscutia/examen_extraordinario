from extensions import db
from .EnrollmentModel import enrollments


class Alumno(db.Model):
	__tablename__ = 'alumnos'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nombre = db.Column(db.String(100), nullable=False)

	cursos = db.relationship(
		'Curso',
		secondary=enrollments,
		back_populates='alumnos',
		lazy='select',
	)

	def to_dict(self):
		return {
			'id': self.id,
			'nombre': self.nombre,
		}

	def __repr__(self):
		return f"<Alumno id={self.id} nombre='{self.nombre}'>"
