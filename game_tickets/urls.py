from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('show_teams/', show_teams, name='show_teams'),
    path('show_games/', show_games, name='show_games'),
    path('show_game/<int:pk>/', show_game, name='show_game'),
    path('create_order/<int:pk>/', create_order, name='create_order'),
    path('show_orders/', show_orders, name='show_orders'),
    path('edit_order/<int:pk>/', edit_order, name='edit_order'),
    path('delete_order/<int:pk>/', delete_order, name='delete_order'),
    path('login/', login_user, name="login"),
    path('registration/', registration, name='registration'),
    path('logout/', logout_user, name="logout"),
    path('teams/<int:pk>/', show_team, name='show_team')
]