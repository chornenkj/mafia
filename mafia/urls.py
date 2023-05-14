from django.urls import path

from . import views

app_name = 'mafia'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('players/', views.PlayerNameListView.as_view(), name='players'),
    path('players/add/', views.AddPlayerNameView.as_view(), name='add_player_name'),
    path('current/', views.current_view, name='current'),
    path('current/players/add', views.AddPlayerView.as_view(), name='add_player'),
    path('new/', views.new_view, name='new'),
    path('delete/', views.delete_game_view, name='delete'),

]