from extensions import db
from .EnrollmentModel import enrollments


class Curso(db.Model):
	__tablename__ = 'cursos'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nombre = db.Column(db.String(100), nullable=False)
	categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

	alumnos = db.relationship(
		'Alumno',
		secondary=enrollments,
		back_populates='cursos',
		lazy='select',
	)

	def to_dict(self):
		return {
			'id': self.id,
			'nombre': self.nombre,
			'categoria_id': self.categoria_id,
		}

	def __repr__(self):
		return f"<Curso id={self.id} nombre='{self.nombre}' categoria_id={self.categoria_id}>"
