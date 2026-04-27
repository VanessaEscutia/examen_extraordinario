from extensions import db
from models import Curso, Categoria


def seed_courses():
	"""Crea 10 cursos distribuidos en las categorias existentes."""
	cursos_por_crear = [
		'Introduccion a Python', 'Flask Web', 'Bases de Datos', 'Algoritmos', 'Estructuras de Datos',
		'Algebra Lineal', 'Calculo I', 'Probabilidades', 'Estadistica', 'Aprendizaje Automatico'
	]

	categorias = Categoria.query.order_by(Categoria.id.asc()).all()
	if not categorias:
		raise RuntimeError('No hay categorias. Ejecuta seed de categorias primero.')

	created = []
	# repartir cursos entre las dos categorias
	for idx, nombre in enumerate(cursos_por_crear):
		categoria = categorias[idx % len(categorias)]
		curso = Curso.query.filter_by(nombre=nombre).first()
		if not curso:
			curso = Curso(nombre=nombre, categoria_id=categoria.id)
			db.session.add(curso)
			db.session.flush()
		created.append(curso)

	db.session.commit()
	return created


if __name__ == '__main__':
	print('Ejecutar d:\\estra\\Seed\\AllSeed.py para poblar la BD de forma completa')
