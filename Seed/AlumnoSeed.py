from extensions import db
from models import Alumno


def seed_students(count=12):
	"""Crea al menos `count` alumnos si no existen y devuelve la lista."""
	nombres = [
		'Ana', 'Luis', 'Carla', 'Miguel', 'Sofia', 'Diego', 'Mariana', 'Javier', 'Lucia', 'Pablo', 'Marta', 'Andres'
	]

	created = []
	for i in range(min(count, len(nombres))):
		nombre = nombres[i]
		student = Alumno.query.filter_by(nombre=nombre).first()
		if not student:
			student = Alumno(nombre=nombre)
			db.session.add(student)
			db.session.flush()
		created.append(student)

	db.session.commit()
	return created


if __name__ == '__main__':
	print('Ejecutar d:\\estra\\Seed\\AllSeed.py para poblar la BD de forma completa')
