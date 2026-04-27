import sys
import os
import json

from flask import Flask, jsonify
import flask.json as flask_json

if not hasattr(flask_json, 'JSONEncoder'):
	flask_json.JSONEncoder = json.JSONEncoder

from flask_cors import CORS
try:
	from flasgger import Swagger
except ModuleNotFoundError:
	Swagger = None
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config
from extensions import db, migrate, seeder


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)


	CORS(app)
	db.init_app(app)
	migrate.init_app(app, db)
	seeder.init_app(app, db)

	@app.route('/apispec_1.json')
	def swagger_spec():
		return jsonify(
			{
				'swagger': '2.0',
				'info': {
					'title': 'Estra API by Vanessa <3',
					'version': '1.0.0',
					'description': 'Documentacion de la API de cursos, categorias, alumnos e inscripciones',
				},
				'basePath': '/',
				'schemes': ['http', 'https'],
				'consumes': ['application/json'],
				'produces': ['application/json'],
				'paths': {
					'/api/categories/': {
						'get': {'summary': 'Obtener todas las categorias', 'responses': {'200': {'description': 'OK'}}},
						'post': {'summary': 'Crear una categoria', 'responses': {'201': {'description': 'Created'}}},
					},
					'/api/categories/{id}': {
						'get': {'summary': 'Obtener una categoria por ID', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
						'put': {'summary': 'Actualizar una categoria', 'responses': {'200': {'description': 'OK'}, '400': {'description': 'Bad Request'}, '404': {'description': 'Not Found'}}},
						'delete': {'summary': 'Eliminar una categoria', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}, '409': {'description': 'Conflict'}}},
					},
					'/api/categories/{id}/courses': {
						'get': {'summary': 'Obtener cursos de una categoria', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
					},
					'/api/categories/{id}/courses/count': {
						'get': {'summary': 'Contar cursos de una categoria', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
					},
					'/api/courses/': {
						'get': {'summary': 'Obtener todos los cursos', 'responses': {'200': {'description': 'OK'}}},
						'post': {'summary': 'Crear un curso', 'responses': {'201': {'description': 'Created'}}},
					},
					'/api/courses/{id}': {
						'get': {'summary': 'Obtener un curso por ID', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
						'put': {'summary': 'Actualizar un curso', 'responses': {'200': {'description': 'OK'}, '400': {'description': 'Bad Request'}, '404': {'description': 'Not Found'}}},
						'delete': {'summary': 'Eliminar un curso', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
					},
					'/api/courses/{id}/students': {
						'get': {'summary': 'Obtener alumnos inscritos en un curso', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
					},
					'/api/students/': {
						'get': {'summary': 'Obtener todos los alumnos', 'responses': {'200': {'description': 'OK'}}},
						'post': {'summary': 'Crear un alumno', 'responses': {'201': {'description': 'Created'}}},
					},
					'/api/students/{id}': {
						'get': {'summary': 'Obtener un alumno por ID', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
						'put': {'summary': 'Actualizar un alumno', 'responses': {'200': {'description': 'OK'}, '400': {'description': 'Bad Request'}, '404': {'description': 'Not Found'}}},
						'delete': {'summary': 'Eliminar un alumno', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
					},
					'/api/students/{id}/courses': {
						'get': {'summary': 'Obtener cursos de un alumno', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
					},
					'/api/enrollments/': {
						'get': {'summary': 'Obtener inscripciones agrupadas por alumno', 'responses': {'200': {'description': 'OK'}}},
						'post': {'summary': 'Crear inscripcion alumno-curso', 'responses': {'201': {'description': 'Created'}, '400': {'description': 'Bad Request'}, '404': {'description': 'Not Found'}, '409': {'description': 'Conflict'}}},
					},
					'/api/enrollments/{student_id}/{course_id}': {
						'delete': {'summary': 'Eliminar inscripcion alumno-curso', 'responses': {'200': {'description': 'OK'}, '404': {'description': 'Not Found'}}},
					},
				},
			}
		)

	if Swagger is not None:
		Swagger(app)

	SWAGGER_URL = '/docs'
	API_URL = '/apispec_1.json'
	swaggerui_bp = get_swaggerui_blueprint(
		SWAGGER_URL,
		API_URL,
		config={
			'app_name': 'Estra API'
		}
	)
	app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

	from controllers.CategoriaController import categories_bp
	from controllers.CursosController import courses_bp
	from controllers.AlumnoController import students_bp, enrollments_bp

	app.register_blueprint(categories_bp)
	app.register_blueprint(courses_bp)
	app.register_blueprint(students_bp)
	app.register_blueprint(enrollments_bp)

	@app.route('/')
	def index():
		return jsonify(
			{
				'message': 'API de Cursos',
				'version': '1.0.0',
				'endpoints': {
					'categorias': '/api/categories',
					'cursos': '/api/courses',
					'alumnos': '/api/students',
					'inscripciones': '/api/enrollments',
					'documentaciónSwagger': '/docs'
				},
			}
		)

	@app.cli.group('seed')
	def seed_group():
		"""Comandos para poblar la base de datos."""
		pass

	@seed_group.command('run')
	def seed_run():
		"""Ejecuta todos los seeders."""
		from Seed.AllSeed import run_all

		run_all()

	@seed_group.command('reset')
	def seed_reset():
		"""Elimina y vuelve a sembrar todos los datos."""
		from Seed.AllSeed import reset_all

		reset_all()

	return app


if __name__ == '__main__':
	app = create_app()
	with app.app_context():
		db.create_all()
	app.run(debug=True, host='0.0.0.0', port=5000)
