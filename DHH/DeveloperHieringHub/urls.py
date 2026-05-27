
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index-html'),
    path('developers.html', views.developers, name='developers'),
    path('companies.html', views.companies, name='companies'),
    path('pricing.html', views.pricing, name='pricing'),
    path('join-beta.html', views.join_beta, name='join-beta'),
    path('dashboard.html', views.dashboard, name='dashboard'),
    path('jobs.html', views.jobs, name='jobs'),
    path('github.html', views.github_activity, name='github-activity'),
    path('developer-signup.html', views.developer_signup, name='developer-signup'),
    path('hirer-signup.html', views.hirer_signup, name='hirer-signup'),
    path('developers/<int:pk>/', views.developer_detail, name='developer-detail'),
]
