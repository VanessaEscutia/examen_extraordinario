from flask import Blueprint, request, jsonify

from extensions import db
from models import Categoria, Curso


categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@categories_bp.route('/', methods=['GET'])
def get_all():
	"""Obtener todas las categorias"""
	categories = Categoria.query.order_by(Categoria.id.asc()).all()
	return jsonify({'data': [category.to_dict() for category in categories]}), 200


@categories_bp.route('/<int:id>', methods=['GET'])
def get_one(id):
	"""Obtener una categoria por ID"""
	category = Categoria.query.get(id)
	if not category:
		return jsonify({'error': 'Categoria no encontrada'}), 404

	return jsonify({'data': category.to_dict()}), 200


@categories_bp.route('/', methods=['POST'])
def create():
	"""Crear una categoria"""
	data = request.get_json(silent=True) or {}
	nombre = (data.get('nombre') or '').strip()

	if not nombre:
		return jsonify({'error': 'El campo nombre es obligatorio'}), 400

	category = Categoria(nombre=nombre)
	db.session.add(category)
	db.session.commit()

	return jsonify({'message': 'Categoria creada exitosamente', 'data': category.to_dict()}), 201


@categories_bp.route('/<int:id>', methods=['PUT'])
def update(id):
	"""Actualizar una categoria"""
	category = Categoria.query.get(id)
	if not category:
		return jsonify({'error': 'Categoria no encontrada'}), 404

	data = request.get_json(silent=True) or {}
	nombre = (data.get('nombre') or '').strip()

	if not nombre:
		return jsonify({'error': 'El campo nombre es obligatorio'}), 400

	category.nombre = nombre
	db.session.commit()

	return jsonify({'message': 'Categoria actualizada', 'data': category.to_dict()}), 200


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
	"""Eliminar una categoria"""
	category = Categoria.query.get(id)
	if not category:
		return jsonify({'error': 'Categoria no encontrada'}), 404

	has_courses = Curso.query.filter_by(categoria_id=id).first() is not None
	if has_courses:
		return jsonify({'error': 'No se puede eliminar la categoria porque tiene cursos asociados'}), 409

	db.session.delete(category)
	db.session.commit()

	return jsonify({'message': 'Categoria eliminada'}), 200


@categories_bp.route('/<int:id>/courses', methods=['GET'])
def get_courses_by_category(id):
	"""Obtener cursos de una categoria"""
	category = Categoria.query.get(id)
	if not category:
		return jsonify({'error': 'Categoria no encontrada'}), 404

	courses = Curso.query.filter_by(categoria_id=id).order_by(Curso.id.asc()).all()
	return jsonify({'data': [course.to_dict() for course in courses]}), 200


@categories_bp.route('/<int:id>/courses/count', methods=['GET'])
def count_courses_by_category(id):
	"""Contar cursos de una categoria"""
	category = Categoria.query.get(id)
	if not category:
		return jsonify({'error': 'Categoria no encontrada'}), 404

	total = Curso.query.filter_by(categoria_id=id).count()
	return jsonify({'data': {'categoria_id': id, 'courses_count': total}}), 200
