from django.urls import path
from . import views

urlpatterns = [
    path('', views.developers_list, name='developers_list'),
    path('<str:username>/', views.developer_detail, name='developer_detail'),
]
