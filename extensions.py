from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class _NoopExtension:
	def init_app(self, app, db=None):
		return None


db = SQLAlchemy()
migrate = Migrate()
seeder = _NoopExtension()
