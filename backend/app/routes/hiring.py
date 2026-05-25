from flask import Blueprint, request, jsonify
from ..models.user import User, DeveloperProfile, Skill, dev_skills
from .. import db

hiring_bp = Blueprint('hiring', __name__)

@hiring_bp.route('/search', methods=['GET'])
def search_developers():
    query_str = request.args.get('q', '')
    location = request.args.get('location', '')
    min_score = request.args.get('min_score', 0, type=float)
    
    query = db.session.query(User, DeveloperProfile).join(DeveloperProfile)
    
    if query_str:
        # Full-text search or keyword search
        query = query.filter(
            (User.full_name.ilike(f'%{query_str}%')) | 
            (DeveloperProfile.bio.ilike(f'%{query_str}%'))
        )
    
    if location:
        query = query.filter(DeveloperProfile.location.ilike(f'%{location}%'))
        
    if min_score > 0:
        query = query.filter(DeveloperProfile.overall_score >= min_score)
        
    results = query.all()
    
    output = []
    for user, profile in results:
        output.append({
            "id": user.id,
            "full_name": user.full_name,
            "github_username": user.github_username,
            "avatar_url": user.avatar_url,
            "location": profile.location,
            "overall_score": profile.overall_score,
            "bio": profile.bio
        })
        
    return jsonify(output), 200
