from flask import Blueprint, request, jsonify

from extensions import db
from models import Alumno, Curso


students_bp = Blueprint('students', __name__, url_prefix='/api/students')
enrollments_bp = Blueprint('enrollments', __name__, url_prefix='/api/enrollments')


@students_bp.route('/', methods=['GET'])
def get_all():
	"""Obtener todos los alumnos"""
	students = Alumno.query.order_by(Alumno.id.asc()).all()
	return jsonify({'data': [student.to_dict() for student in students]}), 200


@students_bp.route('/<int:id>', methods=['GET'])
def get_one(id):
	"""Obtener un alumno por ID"""
	student = Alumno.query.get(id)
	if not student:
		return jsonify({'error': 'Alumno no encontrado'}), 404

	return jsonify({'data': student.to_dict()}), 200


@students_bp.route('/', methods=['POST'])
def create():
	"""Crear un alumno"""
	data = request.get_json(silent=True) or {}
	nombre = (data.get('nombre') or '').strip()

	if not nombre:
		return jsonify({'error': 'El campo nombre es obligatorio'}), 400

	student = Alumno(nombre=nombre)
	db.session.add(student)
	db.session.commit()

	return jsonify({'message': 'Alumno creado exitosamente', 'data': student.to_dict()}), 201


@students_bp.route('/<int:id>', methods=['PUT'])
def update(id):
	"""Actualizar un alumno"""
	student = Alumno.query.get(id)
	if not student:
		return jsonify({'error': 'Alumno no encontrado'}), 404

	data = request.get_json(silent=True) or {}
	nombre = (data.get('nombre') or '').strip()

	if not nombre:
		return jsonify({'error': 'El campo nombre es obligatorio'}), 400

	student.nombre = nombre
	db.session.commit()

	return jsonify({'message': 'Alumno actualizado', 'data': student.to_dict()}), 200


@students_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
	"""Eliminar un alumno"""
	student = Alumno.query.get(id)
	if not student:
		return jsonify({'error': 'Alumno no encontrado'}), 404

	db.session.delete(student)
	db.session.commit()

	return jsonify({'message': 'Alumno eliminado'}), 200


@students_bp.route('/<int:id>/courses', methods=['GET'])
def get_courses_by_student(id):
	"""Obtener cursos de un alumno"""
	student = Alumno.query.get(id)
	if not student:
		return jsonify({'error': 'Alumno no encontrado'}), 404

	courses = sorted(student.cursos, key=lambda course: course.id)
	return jsonify({'data': [course.to_dict() for course in courses]}), 200


@enrollments_bp.route('/', methods=['GET'])
def get_enrollments():
	"""Obtener lista de inscripciones agrupadas por alumno"""
	students = Alumno.query.order_by(Alumno.id.asc()).all()
	data = []

	for student in students:
		courses = sorted(student.cursos, key=lambda course: course.id)
		data.append(
			{
				'alumno': student.to_dict(),
				'cursos': [course.to_dict() for course in courses],
			}
		)

	return jsonify({'data': data}), 200


@enrollments_bp.route('/', methods=['POST'])
def create_enrollment():
	"""Crear inscripcion alumno-curso"""
	data = request.get_json(silent=True) or {}
	student_id = data.get('student_id')
	course_id = data.get('course_id')

	if student_id is None or course_id is None:
		return jsonify({'error': 'Los campos student_id y course_id son obligatorios'}), 400

	student = Alumno.query.get(student_id)
	if not student:
		return jsonify({'error': 'Alumno no encontrado'}), 404

	course = Curso.query.get(course_id)
	if not course:
		return jsonify({'error': 'Curso no encontrado'}), 404

	already_enrolled = any(existing_course.id == course.id for existing_course in student.cursos)
	if already_enrolled:
		return jsonify({'error': 'El alumno ya esta inscrito en este curso'}), 409

	student.cursos.append(course)
	db.session.commit()

	return jsonify({'message': 'Inscripcion creada exitosamente'}), 201


@enrollments_bp.route('/<int:student_id>/<int:course_id>', methods=['DELETE'])
def delete_enrollment(student_id, course_id):
	"""Eliminar inscripcion alumno-curso"""
	student = Alumno.query.get(student_id)
	if not student:
		return jsonify({'error': 'Alumno no encontrado'}), 404

	course = Curso.query.get(course_id)
	if not course:
		return jsonify({'error': 'Curso no encontrado'}), 404

	target_course = next((existing_course for existing_course in student.cursos if existing_course.id == course.id), None)
	if not target_course:
		return jsonify({'error': 'Inscripcion no encontrada'}), 404

	student.cursos.remove(target_course)
	db.session.commit()

	return jsonify({'message': 'Inscripcion eliminada'}), 200
