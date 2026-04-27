from extensions import db


class Categoria(db.Model):
	__tablename__ = 'categorias'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	nombre = db.Column(db.String(100), nullable=False)

	cursos = db.relationship('Curso', backref='categoria', lazy=True)

	def to_dict(self):
		return {
			'id': self.id,
			'nombre': self.nombre,
		}

	def __repr__(self):
		return f"<Categoria id={self.id} nombre='{self.nombre}'>"
