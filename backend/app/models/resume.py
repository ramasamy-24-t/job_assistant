from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from app import db

class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    raw_text = db.Column(db.Text, nullable=True)
    parsed_json = db.Column(JSONB, nullable=True) # Postgres specific for storing parsed components
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship back to application history context
    applications = db.relationship('ApplicationHistory', backref='resume', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'raw_text': self.raw_text,
            'parsed_json': self.parsed_json,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
