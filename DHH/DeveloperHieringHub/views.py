from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    BetaJoinerForm,
    DeveloperSignupForm,
    GitHubConnectionForm,
    HirerSignupForm,
    JobPostForm,
)
from .models import (
    BetaJoiner,
    DeveloperProfile,
    GitHubAuth,
    GitHubCommit,
    GitHubRepository,
    HirerProfile,
    JobPost,
    PlatformUser,
)


def site_stats():
    return {
        'beta_joiners': BetaJoiner.objects.count(),
        'developers': DeveloperProfile.objects.count(),
        'hirers': HirerProfile.objects.count(),
        'jobs': JobPost.objects.filter(is_active=True).count(),
        'repositories': GitHubRepository.objects.count(),
        'commits': GitHubCommit.objects.count(),
        'code_score': DeveloperProfile.objects.aggregate(total=Sum('code_score'))['total'] or 0,
    }


def index(request):
    context = {
        'stats': site_stats(),
        'featured_developers': DeveloperProfile.objects.select_related('user')[:3],
        'latest_jobs': JobPost.objects.filter(is_active=True)[:3],
    }
    return render(request, 'DeveloperHieringHub/index.html', context)


def developers(request):
    context = {
        'developers': DeveloperProfile.objects.select_related('user').prefetch_related('skills'),
        'stats': site_stats(),
    }
    return render(request, 'DeveloperHieringHub/developers.html', context)


def companies(request):
    context = {
        'hirers': HirerProfile.objects.select_related('user')[:6],
        'jobs': JobPost.objects.filter(is_active=True)[:6],
        'stats': site_stats(),
    }
    return render(request, 'DeveloperHieringHub/companies.html', context)


def pricing(request):
    return render(request, 'DeveloperHieringHub/pricing.html', {'stats': site_stats()})


def join_beta(request):
    form = BetaJoinerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'You joined the DHH beta list. We will contact you soon.')
        return redirect('join-beta')

    return render(request, 'DeveloperHieringHub/join-beta.html', {'form': form})


def dashboard(request):
    context = {
        'stats': site_stats(),
        'latest_joiners': BetaJoiner.objects.all()[:8],
        'latest_developers': DeveloperProfile.objects.select_related('user')[:6],
        'latest_jobs': JobPost.objects.filter(is_active=True)[:6],
        'latest_commits': GitHubCommit.objects.select_related('developer__user', 'repository')[:8],
    }
    return render(request, 'DeveloperHieringHub/dashboard.html', context)


def jobs(request):
    form = JobPostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Job post saved. Developers can now see it.')
        return redirect('jobs')

    context = {
        'form': form,
        'jobs': JobPost.objects.filter(is_active=True),
        'stats': site_stats(),
    }
    return render(request, 'DeveloperHieringHub/jobs.html', context)


def developer_detail(request, pk):
    developer = get_object_or_404(
        DeveloperProfile.objects.select_related('user').prefetch_related('skills', 'repositories'),
        pk=pk,
    )
    context = {
        'developer': developer,
        'repositories': developer.repositories.all()[:12],
        'commits': developer.commits.select_related('repository')[:12],
    }
    return render(request, 'DeveloperHieringHub/developer-detail.html', context)


def developer_signup(request):
    form = DeveloperSignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = PlatformUser.objects.create(
            full_name=form.cleaned_data['full_name'],
            email=form.cleaned_data['email'],
            role=PlatformUser.ROLE_DEVELOPER,
            github_username=form.cleaned_data['github_username'],
            bio=form.cleaned_data['bio'],
        )
        DeveloperProfile.objects.create(
            user=user,
            headline=form.cleaned_data['headline'],
            primary_stack=form.cleaned_data['primary_stack'],
            years_experience=form.cleaned_data['years_experience'],
            portfolio_url=form.cleaned_data['portfolio_url'],
        )
        GitHubAuth.objects.create(user=user, username=form.cleaned_data['github_username'])
        messages.success(request, 'Developer profile created.')
        return redirect('developers')

    return render(request, 'DeveloperHieringHub/signup-developer.html', {'form': form})


def hirer_signup(request):
    form = HirerSignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = PlatformUser.objects.create(
            full_name=form.cleaned_data['full_name'],
            email=form.cleaned_data['email'],
            role=PlatformUser.ROLE_HIRER,
        )
        HirerProfile.objects.create(
            user=user,
            company_name=form.cleaned_data['company_name'],
            company_website=form.cleaned_data['company_website'],
            company_size=form.cleaned_data['company_size'],
            hiring_needs=form.cleaned_data['hiring_needs'],
        )
        messages.success(request, 'Hirer profile created.')
        return redirect('companies')

    return render(request, 'DeveloperHieringHub/signup-hirer.html', {'form': form})


def github_activity(request):
    form = GitHubConnectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user, _ = PlatformUser.objects.get_or_create(
            email=form.cleaned_data['email'],
            defaults={
                'full_name': form.cleaned_data['full_name'],
                'role': PlatformUser.ROLE_DEVELOPER,
                'github_username': form.cleaned_data['github_username'],
            },
        )
        if not hasattr(user, 'developer_profile'):
            DeveloperProfile.objects.create(
                user=user,
                headline=form.cleaned_data['headline'] or 'Developer',
            )
        GitHubAuth.objects.update_or_create(
            user=user,
            defaults={'username': form.cleaned_data['github_username'], 'is_active': True},
        )
        messages.success(request, 'GitHub connection saved. OAuth sync can be added with your GitHub app keys.')
        return redirect('github-activity')

    context = {
        'form': form,
        'connections': GitHubAuth.objects.select_related('user')[:12],
        'repositories': GitHubRepository.objects.select_related('developer__user')[:12],
        'commits': GitHubCommit.objects.select_related('developer__user', 'repository')[:12],
        'stats': site_stats(),
    }
    return render(request, 'DeveloperHieringHub/github.html', context)
