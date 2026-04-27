from flask import Flask, jsonify
import sqlite3
from flasgger import Swagger

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs" 
}

swagger = Swagger(app, config=swagger_config)

def get_db():
    conn = sqlite3.connect('examen.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """
    Ruta de inicio
    ---
    responses:
      200:
        description: API Operativa
    """
    return jsonify({"message": "API running"})

@app.route('/categories', methods=['GET'])
def get_categories():
    """
    Lista todas las categorías
    ---
    responses:
      200:
        description: Lista de categorías
    """
    conn = get_db()
    data = conn.execute('SELECT * FROM categoria').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/categories/<int:id>/courses', methods=['GET'])
def get_courses_by_category(id):
    """
    Devuelve los cursos de una categoría
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cursos encontrados
    """
    conn = get_db()
    data = conn.execute('SELECT * FROM curso WHERE categoria_id = ?', (id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/categories/<int:id>/courses/count', methods=['GET'])
def get_courses_count(id):
    """
    Devuelve cuántos cursos tiene una categoría
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Conteo de cursos
    """
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) as total FROM curso WHERE categoria_id = ?', (id,)).fetchone()
    conn.close()
    return jsonify({'count': count['total']})

@app.route('/courses', methods=['GET'])
def get_courses():
    """
    Lista todos los cursos
    ---
    responses:
      200:
        description: Lista de todos los cursos
    """
    conn = get_db()
    data = conn.execute('SELECT c.id, c.nombre, cat.nombre as categoria FROM curso c JOIN categoria cat ON c.categoria_id = cat.id').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/courses/<int:id>/students', methods=['GET'])
def get_students_by_course(id):
    """
    Lista los alumnos inscritos en un curso
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de alumnos
    """
    conn = get_db()
    data = conn.execute('SELECT a.* FROM alumno a JOIN enrollment e ON a.id = e.alumno_id WHERE e.curso_id = ?', (id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/students', methods=['GET'])
def get_students():
    """
    Lista todos los alumnos
    ---
    responses:
      200:
        description: Lista de alumnos
    """
    conn = get_db()
    data = conn.execute('SELECT * FROM alumno').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/students/<int:id>/courses', methods=['GET'])
def get_courses_by_student(id):
    """
    Lista los cursos en los que está inscrito un alumno
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Cursos del alumno
    """
    conn = get_db()
    data = conn.execute('SELECT c.* FROM curso c JOIN enrollment e ON c.id = e.curso_id WHERE e.alumno_id = ?', (id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

@app.route('/enrollments', methods=['GET'])
def get_enrollments():
    """
    Estructura de alumnos y sus cursos
    ---
    responses:
      200:
        description: Inscripciones detalladas
    """
    conn = get_db()
    estudiantes = conn.execute('SELECT * FROM alumno').fetchall()
    result = []
    for est in estudiantes:
        cursos = conn.execute('SELECT c.nombre FROM curso c JOIN enrollment e ON c.id = e.curso_id WHERE e.alumno_id = ?', (est['id'],)).fetchall()
        result.append({
            'student': est['nombre'],
            'courses': [c['nombre'] for c in cursos]
        })
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)