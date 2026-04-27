from extensions import db
from models import Categoria


def seed_categories():
	"""Crea 2 categorias si no existen y devuelve la lista creada/consultada."""
	nombres = ['Programacion', 'Matematicas']
	categorias = []

	for nombre in nombres:
		cat = Categoria.query.filter_by(nombre=nombre).first()
		if not cat:
			cat = Categoria(nombre=nombre)
			db.session.add(cat)
			db.session.flush()
		categorias.append(cat)

	db.session.commit()
	return categorias


if __name__ == '__main__':
	# Ejecutar desde AllSeed preferiblemente
	print('Ejecutar d:\\estra\\Seed\\AllSeed.py para poblar la BD de forma completa')
