from datetime import datetime
from .database import db

class Template(db.Model):

    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key=True)

    template_name = db.Column(db.String(200), nullable=False)

    report_type = db.Column(db.String(100))

    description = db.Column(db.String(500))

    filename = db.Column(db.String(300), nullable=False)

    placeholders = db.Column(db.Text)

    uploaded_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    active = db.Column(
        db.Boolean,
        default=True
    )