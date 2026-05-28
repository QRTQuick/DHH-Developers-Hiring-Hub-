from django.urls import path
from . import views

urlpatterns = [
    path('developers/', views.developers_api, name='api_developers'),
    path('developers/<str:username>/', views.developer_detail_api, name='api_developer_detail'),
    path('sync/github/<str:username>/', views.sync_github, name='api_sync_github'),
]
