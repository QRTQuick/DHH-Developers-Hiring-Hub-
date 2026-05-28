from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Developer

def developers_list(request):
    # Get search query
    query = request.GET.get('q', '')
    stack_filter = request.GET.get('stack', '')
    
    # Filter developers
    developers = Developer.objects.all()
    
    if query:
        developers = developers.filter(
            Q(github_username__icontains=query) |
            Q(name__icontains=query) |
            Q(bio__icontains=query)
        )
    
    if stack_filter:
        developers = developers.filter(stacks__contains=[stack_filter])
    
    context = {
        'developers': developers,
        'query': query,
        'stack_filter': stack_filter,
    }
    
    return render(request, 'developers/developers_list.html', context)

def developer_detail(request, username):
    developer = get_object_or_404(Developer, github_username=username)
    repositories = developer.repositories.all()[:6]  # Top 6 repos
    
    context = {
        'developer': developer,
        'repositories': repositories,
    }
    
    return render(request, 'developers/developer_detail.html', context)
