from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BetaJoiner(TimeStampedModel):
    ROLE_DEVELOPER = 'developer'
    ROLE_HIRER = 'hirer'
    ROLE_COMPANY = 'company'
    ROLE_CHOICES = [
        (ROLE_DEVELOPER, 'Developer'),
        (ROLE_HIRER, 'Hirer'),
        (ROLE_COMPANY, 'Company'),
    ]

    full_name = models.CharField(max_length=160)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company_name = models.CharField(max_length=180, blank=True)
    github_username = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    is_contacted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} ({self.get_role_display()})'


class PlatformUser(TimeStampedModel):
    ROLE_DEVELOPER = 'developer'
    ROLE_HIRER = 'hirer'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_DEVELOPER, 'Developer'),
        (ROLE_HIRER, 'Hirer'),
        (ROLE_ADMIN, 'Admin'),
    ]

    auth_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='dhh_profile',
    )
    full_name = models.CharField(max_length=160)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    location = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    avatar_url = models.URLField(blank=True)
    github_username = models.CharField(max_length=120, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} - {self.get_role_display()}'

    @property
    def password(self):
        """Delegate password access to auth_user"""
        if self.auth_user:
            return self.auth_user.password
        return ''


class Skill(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DeveloperProfile(TimeStampedModel):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('interviewing', 'Interviewing'),
        ('busy', 'Busy'),
    ]

    user = models.OneToOneField(
        PlatformUser,
        on_delete=models.CASCADE,
        related_name='developer_profile',
    )
    headline = models.CharField(max_length=180)
    primary_stack = models.CharField(max_length=180, blank=True)
    years_experience = models.PositiveSmallIntegerField(default=0)
    availability = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='available',
    )
    hourly_rate = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    portfolio_url = models.URLField(blank=True)
    resume_url = models.URLField(blank=True)
    code_score = models.PositiveSmallIntegerField(default=0)
    repositories_count = models.PositiveIntegerField(default=0)
    commits_count = models.PositiveIntegerField(default=0)
    open_source_contributions = models.PositiveIntegerField(default=0)
    last_github_sync = models.DateTimeField(null=True, blank=True)
    skills = models.ManyToManyField(Skill, through='DeveloperSkill', blank=True)

    class Meta:
        ordering = ['-code_score', '-updated_at']

    def __str__(self):
        return self.user.full_name


class DeveloperSkill(TimeStampedModel):
    developer = models.ForeignKey(DeveloperProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    years_used = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ['developer', 'skill']
        ordering = ['skill__name']

    def __str__(self):
        return f'{self.developer} - {self.skill}'


class HirerProfile(TimeStampedModel):
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10'),
        ('11-50', '11-50'),
        ('51-200', '51-200'),
        ('201-500', '201-500'),
        ('500+', '500+'),
    ]

    user = models.OneToOneField(
        PlatformUser,
        on_delete=models.CASCADE,
        related_name='hirer_profile',
    )
    company_name = models.CharField(max_length=180)
    company_website = models.URLField(blank=True)
    company_size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, blank=True)
    hiring_needs = models.TextField(blank=True)
    active_jobs_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name


class JobPost(TimeStampedModel):
    TYPE_CHOICES = [
        ('full_time', 'Full-time'),
        ('contract', 'Contract'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
    ]

    hirer = models.ForeignKey(
        HirerProfile,
        on_delete=models.CASCADE,
        related_name='jobs',
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=180)
    company_name = models.CharField(max_length=180)
    location = models.CharField(max_length=160, blank=True)
    job_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='full_time')
    salary_range = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    required_skills = models.CharField(max_length=260, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} at {self.company_name}'


class GitHubAuth(TimeStampedModel):
    user = models.OneToOneField(
        PlatformUser,
        on_delete=models.CASCADE,
        related_name='github_auth',
    )
    github_user_id = models.CharField(max_length=80, blank=True)
    username = models.CharField(max_length=120)
    access_token_reference = models.CharField(max_length=255, blank=True)
    scopes = models.CharField(max_length=255, blank=True)
    connected_at = models.DateTimeField(default=timezone.now)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-connected_at']

    def __str__(self):
        return f'GitHub: {self.username}'


class GitHubRepository(TimeStampedModel):
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='repositories',
    )
    github_repo_id = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=180)
    full_name = models.CharField(max_length=260)
    url = models.URLField(blank=True)
    language = models.CharField(max_length=80, blank=True)
    stars = models.PositiveIntegerField(default=0)
    forks = models.PositiveIntegerField(default=0)
    commits_count = models.PositiveIntegerField(default=0)
    last_pushed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['developer', 'full_name']
        ordering = ['-stars', 'name']

    def __str__(self):
        return self.full_name


class GitHubCommit(TimeStampedModel):
    repository = models.ForeignKey(
        GitHubRepository,
        on_delete=models.CASCADE,
        related_name='commits',
    )
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='commits',
    )
    sha = models.CharField(max_length=80, unique=True)
    message = models.TextField()
    author_name = models.CharField(max_length=160, blank=True)
    author_email = models.EmailField(blank=True)
    committed_at = models.DateTimeField()
    additions = models.PositiveIntegerField(default=0)
    deletions = models.PositiveIntegerField(default=0)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ['-committed_at']

    def __str__(self):
        return self.sha[:10]


class DeveloperMetricSnapshot(TimeStampedModel):
    developer = models.ForeignKey(
        DeveloperProfile,
        on_delete=models.CASCADE,
        related_name='metric_snapshots',
    )
    code_score = models.PositiveSmallIntegerField(default=0)
    repositories_count = models.PositiveIntegerField(default=0)
    commits_count = models.PositiveIntegerField(default=0)
    open_source_contributions = models.PositiveIntegerField(default=0)
    captured_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-captured_at']

    def __str__(self):
        return f'{self.developer} metrics at {self.captured_at:%Y-%m-%d}'


class EmailOTP(TimeStampedModel):
    PURPOSE_LOGIN = 'login'
    PURPOSE_CHOICES = [
        (PURPOSE_LOGIN, 'Login'),
    ]

    user = models.ForeignKey(
        PlatformUser,
        on_delete=models.CASCADE,
        related_name='email_otps',
    )
    email = models.EmailField()
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default=PURPOSE_LOGIN)
    code_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    request_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'purpose', 'used_at']),
            models.Index(fields=['expires_at']),
        ]

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def is_usable(self):
        return self.used_at is None and not self.is_expired and self.attempts < 5

    def set_code(self, code):
        self.code_hash = make_password(code)

    def verify(self, code):
        is_valid = self.is_usable and check_password(code, self.code_hash)
        self.attempts += 1
        if is_valid:
            self.used_at = timezone.now()
        self.save(update_fields=['attempts', 'used_at', 'updated_at'])
        return is_valid

    def __str__(self):
        return f'{self.email} {self.get_purpose_display()} OTP'
