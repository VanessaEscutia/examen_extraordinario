from flask import Blueprint, request, jsonify

from extensions import db
from models import Categoria, Curso


courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


@courses_bp.route('/', methods=['GET'])
def get_all():
	"""Obtener todos los cursos"""
	courses = Curso.query.order_by(Curso.id.asc()).all()
	return jsonify({'data': [course.to_dict() for course in courses]}), 200


@courses_bp.route('/<int:id>', methods=['GET'])
def get_one(id):
	"""Obtener un curso por ID"""
	course = Curso.query.get(id)
	if not course:
		return jsonify({'error': 'Curso no encontrado'}), 404

	return jsonify({'data': course.to_dict()}), 200


@courses_bp.route('/', methods=['POST'])
def create():
	"""Crear un curso"""
	data = request.get_json(silent=True) or {}
	nombre = (data.get('nombre') or '').strip()
	categoria_id = data.get('categoria_id')

	if not nombre:
		return jsonify({'error': 'El campo nombre es obligatorio'}), 400
	if categoria_id is None:
		return jsonify({'error': 'El campo categoria_id es obligatorio'}), 400

	category = Categoria.query.get(categoria_id)
	if not category:
		return jsonify({'error': 'Categoria no encontrada'}), 404

	course = Curso(nombre=nombre, categoria_id=category.id)
	db.session.add(course)
	db.session.commit()

	return jsonify({'message': 'Curso creado exitosamente', 'data': course.to_dict()}), 201


@courses_bp.route('/<int:id>', methods=['PUT'])
def update(id):
	"""Actualizar un curso"""
	course = Curso.query.get(id)
	if not course:
		return jsonify({'error': 'Curso no encontrado'}), 404

	data = request.get_json(silent=True) or {}
	nombre = (data.get('nombre') or '').strip()
	categoria_id = data.get('categoria_id')

	if not nombre:
		return jsonify({'error': 'El campo nombre es obligatorio'}), 400
	if categoria_id is None:
		return jsonify({'error': 'El campo categoria_id es obligatorio'}), 400

	category = Categoria.query.get(categoria_id)
	if not category:
		return jsonify({'error': 'Categoria no encontrada'}), 404

	course.nombre = nombre
	course.categoria_id = category.id
	db.session.commit()

	return jsonify({'message': 'Curso actualizado', 'data': course.to_dict()}), 200


@courses_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
	"""Eliminar un curso"""
	course = Curso.query.get(id)
	if not course:
		return jsonify({'error': 'Curso no encontrado'}), 404

	db.session.delete(course)
	db.session.commit()

	return jsonify({'message': 'Curso eliminado'}), 200


@courses_bp.route('/<int:id>/students', methods=['GET'])
def get_students_by_course(id):
	"""Obtener alumnos inscritos en un curso"""
	course = Curso.query.get(id)
	if not course:
		return jsonify({'error': 'Curso no encontrado'}), 404

	students = sorted(course.alumnos, key=lambda student: student.id)
	return jsonify({'data': [student.to_dict() for student in students]}), 200
