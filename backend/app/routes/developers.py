from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User, DeveloperProfile
from ..services.github_service import GitHubService
from .. import db

dev_bp = Blueprint('developers', __name__)

@dev_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    profile = DeveloperProfile.query.filter_by(user_id=user_id).first()
    
    return jsonify({
        "full_name": user.full_name,
        "github_username": user.github_username,
        "avatar_url": user.avatar_url,
        "bio": profile.bio,
        "scores": {
            "overall": profile.overall_score,
            "project": profile.project_score,
            "trust": profile.trust_score,
            "consistency": profile.consistency_score,
            "team": profile.team_score
        },
        "stats": {
            "stars": profile.total_stars,
            "forks": profile.total_forks,
            "repos": profile.public_repos
        }
    }), 200

@dev_bp.route('/sync-github', methods=['POST'])
@jwt_required()
def sync_github():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    github_username = data.get('github_username')
    
    if not github_username:
        return jsonify({"msg": "GitHub username required"}), 400
        
    github_data = GitHubService.get_user_data(github_username)
    if not github_data:
        return jsonify({"msg": "GitHub user not found"}), 404
        
    repos = GitHubService.get_user_repos(github_username)
    scores = GitHubService.calculate_scores(github_data, repos)
    
    # Update user and profile
    user.github_username = github_username
    user.avatar_url = github_data.get('avatar_url')
    
    profile = DeveloperProfile.query.filter_by(user_id=user_id).first()
    profile.overall_score = scores['overall_score']
    profile.project_score = scores['project_score']
    profile.trust_score = scores['trust_score']
    profile.consistency_score = scores['consistency_score']
    profile.team_score = scores['team_score']
    profile.total_stars = scores['total_stars']
    profile.total_forks = scores['total_forks']
    profile.public_repos = len(repos)
    
    db.session.commit()
    
    return jsonify({"msg": "GitHub profile synced", "scores": scores}), 200
