from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.resume import Resume
from app.utils.file_extractor import extract_text_from_pdf, extract_text_from_docx
from app.services.resume_parser import ResumeParserService

resume_bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    current_user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Only PDF and DOCX are supported.'}), 400
        
    filename = file.filename.lower()
    raw_text = ""
    
    if filename.endswith('.pdf'):
        raw_text = extract_text_from_pdf(file.stream)
    elif filename.endswith('.docx'):
        raw_text = extract_text_from_docx(file.stream)
        
    if not raw_text:
        return jsonify({'error': 'Could not extract text from file'}), 500
        
    # Parse the extracted text
    parsed_json = ResumeParserService.parse_resume_text(raw_text)
    
    # Save to database
    new_resume = Resume(
        user_id=current_user_id,
        raw_text=raw_text,
        parsed_json=parsed_json
    )
    
    db.session.add(new_resume)
    db.session.commit()
    
    return jsonify({
        'message': 'Resume uploaded and parsed successfully',
        'resume_id': new_resume.id,
        'parsed_data': parsed_json
    }), 201
