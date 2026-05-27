import secrets
from datetime import timedelta
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    BetaJoinerForm,
    DeveloperSignupForm,
    EmailLoginForm,
    GitHubConnectionForm,
    HirerSignupForm,
    JobPostForm,
    OTPVerificationForm,
    ProfileSettingsForm,
)
from .email_service import send_otp_email
from .models import (
    BetaJoiner,
    DeveloperProfile,
    EmailOTP,
    GitHubAuth,
    GitHubCommit,
    GitHubRepository,
    HirerProfile,
    JobPost,
    PlatformUser,
)


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def current_platform_user(request):
    user_id = request.session.get('platform_user_id')
    if not user_id:
        return None
    return PlatformUser.objects.filter(pk=user_id).first()


def platform_login_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        user = current_platform_user(request)
        if not user:
            messages.info(request, 'Sign in with your email code to continue.')
            return redirect('login')
        request.platform_user = user
        return view_func(request, *args, **kwargs)

    return wrapped


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


def loading(request):
    """Loading page that redirects to dashboard if authenticated, otherwise to landing page."""
    return render(request, 'DeveloperHieringHub/loading.html')


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


def about(request):
    return render(request, 'DeveloperHieringHub/about.html', {'stats': site_stats()})


def how_it_works(request):
    return render(request, 'DeveloperHieringHub/how-it-works.html', {'stats': site_stats()})


def security(request):
    return render(request, 'DeveloperHieringHub/security.html', {'user': current_platform_user(request)})


def shortlist(request):
    context = {
        'developers': DeveloperProfile.objects.select_related('user').prefetch_related('skills')[:8],
        'stats': site_stats(),
    }
    return render(request, 'DeveloperHieringHub/shortlist.html', context)


def join_beta(request):
    form = BetaJoinerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'You joined the DHH beta list. We will contact you soon.')
        return redirect('dashboard')

    return render(request, 'DeveloperHieringHub/join-beta.html', {'form': form})


@platform_login_required
def dashboard(request):
    user = request.platform_user
    context = {
        'stats': site_stats(),
        'latest_joiners': BetaJoiner.objects.all()[:8],
        'latest_developers': DeveloperProfile.objects.select_related('user')[:6],
        'latest_jobs': JobPost.objects.filter(is_active=True)[:6],
        'latest_commits': GitHubCommit.objects.select_related('developer__user', 'repository')[:8],
        'user': user,
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


def login(request):
    form = EmailLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        user = PlatformUser.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'No DHH profile exists for that email yet. Create a developer or hirer profile first.')
            return redirect('login')

        code = f'{secrets.randbelow(1000000):06d}'
        otp = EmailOTP(
            user=user,
            email=email,
            expires_at=timezone.now() + timedelta(minutes=settings.EMAIL_OTP_EXPIRY_MINUTES),
            request_ip=get_client_ip(request),
        )
        otp.set_code(code)
        otp.save()

        try:
            send_otp_email(email, code)
        except Exception as exc:
            otp.delete()
            messages.error(request, f'Could not send the email code yet: {exc}')
            return redirect('login')

        request.session['pending_otp_id'] = otp.pk
        messages.success(request, 'We sent a 6-digit sign-in code to your email.')
        return redirect('verify-code')

    return render(request, 'DeveloperHieringHub/login.html', {'form': form})


def verify_code(request):
    otp_id = request.session.get('pending_otp_id')
    otp = EmailOTP.objects.select_related('user').filter(pk=otp_id).first() if otp_id else None
    if not otp:
        messages.info(request, 'Request a new sign-in code.')
        return redirect('login')

    form = OTPVerificationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        if otp.verify(form.cleaned_data['code']):
            request.session['platform_user_id'] = otp.user_id
            request.session.pop('pending_otp_id', None)
            otp.user.is_verified = True
            otp.user.save(update_fields=['is_verified', 'updated_at'])
            messages.success(request, 'You are signed in.')
            return redirect('dashboard')

        messages.error(request, 'That code is invalid, expired, or has too many attempts.')

    return render(request, 'DeveloperHieringHub/verify-code.html', {'form': form, 'otp': otp})


def logout(request):
    request.session.pop('platform_user_id', None)
    request.session.pop('pending_otp_id', None)
    messages.success(request, 'You are signed out.')
    return redirect('index')


@platform_login_required
def profile(request):
    user = request.platform_user
    context = {
        'user': user,
        'developer_profile': getattr(user, 'developer_profile', None),
        'hirer_profile': getattr(user, 'hirer_profile', None),
        'github_auth': getattr(user, 'github_auth', None),
    }
    return render(request, 'DeveloperHieringHub/profile.html', context)


@platform_login_required
def settings_page(request):
    user = request.platform_user
    form = ProfileSettingsForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your settings were saved.')
        return redirect('settings')

    return render(request, 'DeveloperHieringHub/settings.html', {'form': form, 'user': user})
