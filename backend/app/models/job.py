from datetime import datetime
from app import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('ApplicationHistory', backref='job', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'description': self.description,
            'requirements': self.requirements,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None
        }
