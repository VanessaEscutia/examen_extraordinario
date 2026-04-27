-- seed.sql
INSERT INTO categoria (nombre) VALUES 
('Programación'),
('Base de Datos');

INSERT INTO curso (nombre, categoria_id) VALUES 
('Python Básico', 1),
('JavaScript Essentials', 1),
('Flask API', 1),
('Django Rest Framework', 1),
('React JS', 1),
('SQLite Básico', 2),
('MySQL Completo', 2),
('PostgreSQL Avanzado', 2),
('MongoDB', 2),
('Redis', 2);

INSERT INTO alumno (nombre) VALUES 
('Juan Pérez'),
('María González'),
('Carlos López'),
('Ana Martínez'),
('Pedro Sánchez'),
('Laura Rodríguez'),
('Miguel Torres'),
('Sofia Rivera'),
('Jorge Gómez'),
('Elena Castro'),
('Roberto Díaz'),
('Carmen Ruiz');

INSERT INTO enrollment (alumno_id, curso_id) VALUES 
(1, 1), (1, 3), (1, 6),
(2, 1), (2, 2), (2, 7),
(3, 3), (3, 4), (3, 8),
(4, 1), (4, 5), (4, 9),
(5, 2), (5, 3), (5, 6),
(6, 4), (6, 7), (6, 10),
(7, 5), (7, 9), (7, 8),
(8, 1), (8, 6), (8, 7),
(9, 2), (9, 4), (9, 10),
(10, 3), (10, 5), (10, 9),
(11, 1), (11, 8),
(12, 2), (12, 6);