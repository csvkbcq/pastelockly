from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Snippet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    encrypted_content = db.Column(db.LargeBinary, nullable=True)
    secret_key = db.Column(db.String(44), nullable=True)
