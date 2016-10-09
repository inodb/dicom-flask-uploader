from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Photo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(120))

	def __init__(self, filename):
		self.filename = filename
