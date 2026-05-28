from django.db import models

class Developer(models.Model):
    github_username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    avatar_url = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    
    # Stats
    public_repos = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    total_stars = models.IntegerField(default=0)
    
    # Activity
    contribution_streak = models.IntegerField(default=0)
    
    # Tech Stack
    stacks = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'developers'
        ordering = ['-total_stars']
    
    def __str__(self):
        return self.github_username

class Repository(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, max_length=500)
    html_url = models.URLField()
    language = models.CharField(max_length=100, blank=True, null=True)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    watchers = models.IntegerField(default=0)
    is_fork = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    
    # Tech Stack for this repo
    stacks = models.JSONField(default=list)
    
    pushed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'repositories'
        ordering = ['-stars']
    
    def __str__(self):
        return f"{self.developer.github_username}/{self.name}"
