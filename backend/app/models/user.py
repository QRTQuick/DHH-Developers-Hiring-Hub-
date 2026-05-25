from .. import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True) # Nullable for GitHub OAuth users
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='developer') # 'developer', 'recruiter', 'admin'
    github_id = db.Column(db.String(100), unique=True, nullable=True)
    github_username = db.Column(db.String(100), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('DeveloperProfile', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class DeveloperProfile(db.Model):
    __tablename__ = 'developer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    resume_url = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.String(50), default='available') # 'available', 'busy', 'hired'
    
    # AI Scores
    trust_score = db.Column(db.Float, default=0.0)
    project_score = db.Column(db.Float, default=0.0)
    team_score = db.Column(db.Float, default=0.0)
    consistency_score = db.Column(db.Float, default=0.0)
    overall_score = db.Column(db.Float, default=0.0)

    # Stats
    total_stars = db.Column(db.Integer, default=0)
    total_forks = db.Column(db.Integer, default=0)
    public_repos = db.Column(db.Integer, default=0)
    followers = db.Column(db.Integer, default=0)

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Association table for developer-skills
dev_skills = db.Table('dev_skills',
    db.Column('profile_id', db.Integer, db.ForeignKey('developer_profiles.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)
