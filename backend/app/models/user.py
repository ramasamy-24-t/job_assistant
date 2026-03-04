from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    preferred_locations = db.Column(db.ARRAY(db.String), nullable=True) # Postgres specific
    actively_looking = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade="all, delete-orphan")
    applications = db.relationship('ApplicationHistory', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'preferred_locations': self.preferred_locations,
            'actively_looking': self.actively_looking,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
