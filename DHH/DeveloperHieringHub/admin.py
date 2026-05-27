from django.contrib import admin

from .models import (
    BetaJoiner,
    DeveloperMetricSnapshot,
    DeveloperProfile,
    DeveloperSkill,
    GitHubAuth,
    GitHubCommit,
    GitHubRepository,
    HirerProfile,
    JobPost,
    PlatformUser,
    Skill,
)


@admin.register(BetaJoiner)
class BetaJoinerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'company_name', 'is_contacted', 'created_at')
    list_filter = ('role', 'is_contacted', 'created_at')
    search_fields = ('full_name', 'email', 'company_name', 'github_username')


@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'role', 'github_username', 'is_verified', 'created_at')
    list_filter = ('role', 'is_verified')
    search_fields = ('full_name', 'email', 'github_username')


class DeveloperSkillInline(admin.TabularInline):
    model = DeveloperSkill
    extra = 1


@admin.register(DeveloperProfile)
class DeveloperProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'headline',
        'availability',
        'code_score',
        'repositories_count',
        'commits_count',
    )
    list_filter = ('availability',)
    search_fields = ('user__full_name', 'user__email', 'headline', 'primary_stack')
    inlines = [DeveloperSkillInline]


@admin.register(HirerProfile)
class HirerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'company_size', 'active_jobs_count', 'created_at')
    search_fields = ('company_name', 'user__full_name', 'user__email')


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'job_type', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active')
    search_fields = ('title', 'company_name', 'required_skills')


@admin.register(GitHubAuth)
class GitHubAuthAdmin(admin.ModelAdmin):
    list_display = ('username', 'user', 'is_active', 'connected_at', 'last_sync_at')
    list_filter = ('is_active',)
    search_fields = ('username', 'github_user_id', 'user__email')


@admin.register(GitHubRepository)
class GitHubRepositoryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'developer', 'language', 'stars', 'forks', 'commits_count')
    list_filter = ('language',)
    search_fields = ('name', 'full_name', 'developer__user__full_name')


@admin.register(GitHubCommit)
class GitHubCommitAdmin(admin.ModelAdmin):
    list_display = ('sha', 'repository', 'developer', 'committed_at', 'additions', 'deletions')
    search_fields = ('sha', 'message', 'repository__full_name', 'developer__user__full_name')


admin.site.register(Skill)
admin.site.register(DeveloperMetricSnapshot)
