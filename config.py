import os


class Config:

	DB_USER = os.getenv('DB_USER', 'root')
	DB_PASS = os.getenv('DB_PASS', '')
	DB_HOST = os.getenv('DB_HOST', 'localhost')
	DB_PORT = os.getenv('DB_PORT', '3306')
	DB_NAME = os.getenv('DB_NAME', 'estra')

	SQLALCHEMY_DATABASE_URI = os.getenv(
		'DATABASE_URL',
		f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4",
	)

	SQLALCHEMY_TRACK_MODIFICATIONS = False
