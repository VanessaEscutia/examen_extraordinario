import random

from app import create_app
from extensions import db
from models import Alumno, Categoria, Curso, enrollments
from Seed.CategoriaSeed import seed_categories
from Seed.CursoSeed import seed_courses
from Seed.AlumnoSeed import seed_students


def run_all(seed_student_count=12, min_course_per_student=1, max_course_per_student=4):
	app = create_app()
	with app.app_context():
		print('Seeding categorias...')
		categorias = seed_categories()

		print('Seeding cursos...')
		cursos = seed_courses()

		print('Seeding alumnos...')
		alumnos = seed_students(count=seed_student_count)

		print('Asignando inscripciones aleatorias...')
		for alumno in alumnos:
			num = random.randint(min_course_per_student, max_course_per_student)
			asignados = random.sample(cursos, k=min(num, len(cursos)))
			for c in asignados:
				if c not in alumno.cursos:
					alumno.cursos.append(c)

		db.session.commit()

		print('Seed completo:')
		print(f'  Categorias: {len(categorias)}')
		print(f'  Cursos: {len(cursos)}')
		print(f'  Alumnos: {len(alumnos)}')


def reset_all():
	"""Elimina todas las filas de las tablas del dominio y vuelve a sembrar."""
	app = create_app()
	with app.app_context():
		print('Borrando inscripciones...')
		db.session.execute(enrollments.delete())

		print('Borrando alumnos, cursos y categorias...')
		Alumno.query.delete()
		Curso.query.delete()
		Categoria.query.delete()
		db.session.commit()

		print('Volviendo a sembrar datos...')
		run_all()


if __name__ == '__main__':
	run_all()
