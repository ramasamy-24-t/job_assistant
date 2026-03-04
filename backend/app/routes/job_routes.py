from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.resume import Resume
from app.models.user import User
from app.services.job_service import JobService

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/ranked', methods=['GET'])
@jwt_required()
def get_ranked_jobs():
    current_user_id = get_jwt_identity()
    
    # Get the user's most recent resume
    latest_resume = Resume.query.filter_by(user_id=current_user_id).order_by(Resume.uploaded_at.desc()).first()
    
    if not latest_resume:
        return jsonify({'error': 'No resume found for this user. Please upload a resume first.'}), 404
        
    role = request.args.get('role', 'Developer')
    provider = request.args.get('provider', 'rapidapi')
    
    # Get the user to get their locations
    user = User.query.get(current_user_id)
    locations = user.preferred_locations if user else ["Remote"]
    
    try:
        ranked_jobs = JobService.fetch_and_rank_jobs(
            resume_text=latest_resume.raw_text,
            parsed_json=latest_resume.parsed_json,
            role=role,
            locations=locations,
            provider=provider
        )
        
        return jsonify({
            'message': 'Jobs ranked successfully',
            'jobs': ranked_jobs
        }), 200
    except Exception as e:
        return jsonify({'error': f'An error occurred while ranking jobs: {str(e)}'}), 500
