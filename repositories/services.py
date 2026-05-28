import requests
from django.conf import settings
from developers.models import Developer, Repository

class GitHubService:
    """Service for interacting with GitHub API"""
    
    BASE_URL = 'https://api.github.com'
    
    def __init__(self):
        self.client_id = settings.GITHUB_CLIENT_ID
        self.client_secret = settings.GITHUB_CLIENT_SECRET
    
    def get_user_profile(self, username):
        """Fetch user profile from GitHub"""
        url = f'{self.BASE_URL}/users/{username}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'github_username': data.get('login'),
                'name': data.get('name'),
                'bio': data.get('bio'),
                'avatar_url': data.get('avatar_url'),
                'location': data.get('location'),
                'website': data.get('blog'),
                'company': data.get('company'),
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
            }
        return None
    
    def get_user_repositories(self, username, limit=50):
        """Fetch user repositories from GitHub"""
        url = f'{self.BASE_URL}/users/{username}/repos'
        params = {
            'sort': 'stars',
            'direction': 'desc',
            'per_page': limit,
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            repos_data = response.json()
            repos = []
            
            for data in repos_data:
                repos.append({
                    'name': data.get('name'),
                    'description': data.get('description'),
                    'html_url': data.get('html_url'),
                    'language': data.get('language'),
                    'stars': data.get('stargazers_count', 0),
                    'forks': data.get('forks_count', 0),
                    'watchers': data.get('watchers_count', 0),
                    'is_fork': data.get('fork', False),
                    'is_private': data.get('private', False),
                    'pushed_at': data.get('pushed_at'),
                })
            
            return repos
        return []
    
    def sync_developer(self, username):
        """Sync developer profile and repositories from GitHub"""
        profile_data = self.get_user_profile(username)
        
        if not profile_data:
            return None
        
        # Update or create developer
        developer, created = Developer.objects.update_or_create(
            github_username=username,
            defaults=profile_data
        )
        
        # Sync repositories
        repos_data = self.get_user_repositories(username)
        
        for repo_data in repos_data:
            Repository.objects.update_or_create(
                developer=developer,
                name=repo_data['name'],
                defaults=repo_data
            )
        
        return developer
