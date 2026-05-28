from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from developers.models import Developer, Repository
from repositories.services import GitHubService

@api_view(['GET'])
def developers_api(request):
    """API endpoint to get list of developers"""
    developers = Developer.objects.all()[:50]  # Limit to 50
    
    data = [{
        'username': dev.github_username,
        'name': dev.name,
        'bio': dev.bio,
        'avatar_url': dev.avatar_url,
        'public_repos': dev.public_repos,
        'followers': dev.followers,
        'total_stars': dev.total_stars,
        'stacks': dev.stacks,
    } for dev in developers]
    
    return Response(data)

@api_view(['GET'])
def developer_detail_api(request, username):
    """API endpoint to get single developer details"""
    try:
        developer = Developer.objects.get(github_username=username)
        
        data = {
            'username': developer.github_username,
            'name': developer.name,
            'bio': developer.bio,
            'avatar_url': developer.avatar_url,
            'location': developer.location,
            'website': developer.website,
            'company': developer.company,
            'public_repos': developer.public_repos,
            'followers': developer.followers,
            'following': developer.following,
            'total_stars': developer.total_stars,
            'contribution_streak': developer.contribution_streak,
            'stacks': developer.stacks,
            'repositories': [{
                'name': repo.name,
                'description': repo.description,
                'html_url': repo.html_url,
                'language': repo.language,
                'stars': repo.stars,
                'forks': repo.forks,
                'stacks': repo.stacks,
            } for repo in developer.repositories.all()[:10]]
        }
        
        return Response(data)
    except Developer.DoesNotExist:
        return Response({'error': 'Developer not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def sync_github(request, username):
    """Sync developer data from GitHub"""
    service = GitHubService()
    developer = service.sync_developer(username)
    
    if developer:
        return Response({
            'message': 'Successfully synced',
            'username': developer.github_username
        })
    
    return Response(
        {'error': 'Failed to sync. User may not exist on GitHub.'},
        status=status.HTTP_400_BAD_REQUEST
    )
