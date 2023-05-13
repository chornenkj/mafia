from django.shortcuts import render

from django.views.generic import ListView

from .models import PlayerName

# Create your views here.

def index_view(request):
    game_id = request.session.get('game_id', False)
    context = {
        'game_id': game_id,
    }
    return render(request, 'mafia/index.html', context)


class PlayerNameListView(ListView):
    model = PlayerName
    template_name = 'mafia/players.html'


def current_view(request):
    return render(request, 'mafia/current.html')


def new_view(request):
    return render(request, 'mafia/new.html')
