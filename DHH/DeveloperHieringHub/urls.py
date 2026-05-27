
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index-html'),
    path('loading.html', views.loading, name='loading'),
    path('developers.html', views.developers, name='developers'),
    path('companies.html', views.companies, name='companies'),
    path('pricing.html', views.pricing, name='pricing'),
    path('join-beta.html', views.join_beta, name='join-beta'),
    path('dashboard.html', views.dashboard, name='dashboard'),
    path('jobs.html', views.jobs, name='jobs'),
    path('github.html', views.github_activity, name='github-activity'),
    path('about.html', views.about, name='about'),
    path('how-it-works.html', views.how_it_works, name='how-it-works'),
    path('security.html', views.security, name='security'),
    path('shortlist.html', views.shortlist, name='shortlist'),
    path('login.html', views.login, name='login'),
    path('verify-code.html', views.verify_code, name='verify-code'),
    path('logout/', views.logout, name='logout'),
    path('profile.html', views.profile, name='profile'),
    path('settings.html', views.settings_page, name='settings'),
    path('developer-signup.html', views.developer_signup, name='developer-signup'),
    path('hirer-signup.html', views.hirer_signup, name='hirer-signup'),
    path('developers/<int:pk>/', views.developer_detail, name='developer-detail'),
]
