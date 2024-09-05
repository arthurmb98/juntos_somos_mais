from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('create-user/', views.create_user, name='create_user'),
    path('health/', views.health_check, name='health_check'),
    path('populate-database/', views.populate_database_view, name='populate_database'),
    path('populate-json/', views.populate_json_view, name='populate_json_view'),
    path('populate-csv/', views.populate_csv_view, name='populate_csv_view'),
    path('purge-users/', views.purge_users_view, name='purge-users'),
]