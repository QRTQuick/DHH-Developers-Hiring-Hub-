import requests
from flask import current_app

class GitHubService:
    BASE_URL = "https://api.github.com"

    @staticmethod
    def get_user_data(username):
        response = requests.get(f"{GitHubService.BASE_URL}/users/{username}")
        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_user_repos(username):
        response = requests.get(f"{GitHubService.BASE_URL}/users/{username}/repos?sort=updated&per_page=100")
        if response.status_code == 200:
            return response.json()
        return []

    @staticmethod
    def calculate_scores(user_data, repos):
        # Placeholder for AI scoring logic
        # In a real app, this would involve more complex analysis
        
        total_stars = sum(repo['stargazers_count'] for repo in repos)
        total_forks = sum(repo['forks_count'] for repo in repos)
        
        # Simple heuristic for demo
        project_score = min(100, (len(repos) * 5) + (total_stars * 2))
        trust_score = 70 if user_data.get('blog') or user_data.get('twitter_username') else 50
        consistency_score = min(100, user_data.get('public_repos', 0) * 2)
        
        overall_score = (project_score + trust_score + consistency_score) / 3
        
        return {
            "project_score": round(project_score, 1),
            "trust_score": round(trust_score, 1),
            "consistency_score": round(consistency_score, 1),
            "team_score": 75.0, # Static placeholder
            "overall_score": round(overall_score, 1),
            "total_stars": total_stars,
            "total_forks": total_forks
        }
