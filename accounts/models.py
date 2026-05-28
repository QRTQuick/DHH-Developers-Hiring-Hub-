from django.db import models
from django.contrib.auth.models import User

class DeveloperProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='developer_profile')
    github_username = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    portfolio_url = models.URLField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    stacks = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'developer_profiles'
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
