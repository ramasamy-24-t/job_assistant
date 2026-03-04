from datetime import datetime
from app import db

class ApplicationHistory(db.Model):
    __tablename__ = 'application_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    
    ats_score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), default='pending') # e.g., pending, applied, rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'resume_id': self.resume_id,
            'ats_score': self.ats_score,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None
        }
