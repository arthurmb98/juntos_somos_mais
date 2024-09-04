from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('users/', views.get_users, name='get_users'),
     path('populate-database/', views.populate_database_view, name='populate_database'),
]
