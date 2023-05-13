from django.urls import path

from . import views

app_name = 'mafia'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('players/', views.PlayerNameListView.as_view(), name='players'),
    path('current/', views.current_view, name='current'),
    path('new/', views.new_view, name='new'),
]