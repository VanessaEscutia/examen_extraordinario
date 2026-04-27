from extensions import db

from .CategoriaModel import Categoria
from .CursoMode import Curso
from .AlumnoModel import Alumno
from .EnrollmentModel import enrollments

__all__ = ['db', 'Categoria', 'Curso', 'Alumno', 'enrollments']
