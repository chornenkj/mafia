from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import ListView, CreateView

from .models import PlayerName, Game, Player, Turn
from .forms import AddPlayerNameForm, PlayersNumber, AddPlayerForm

from Mafia import settings

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

    def get_queryset(self):
        return super().get_queryset().order_by('title')


class AddPlayerNameView(CreateView):

    def get(self, request):
        form = AddPlayerNameForm
        context = {
            'form': form,
        }
        return render(request, 'mafia/add_player_name.html', context)

    def post(self, request):
        form = AddPlayerNameForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('mafia:players'))
        context = {
            'form': form,
        }
        return render(request, 'mafia/add_player_name.html', context)


def current_view(request):
    if request.session.get('game_id'):
        number = request.session.get('number')
        added_players = request.session.get('added_players')
        if added_players < number:
            return HttpResponseRedirect(reverse_lazy('mafia:add_player'))
        return HttpResponseRedirect(reverse_lazy('mafia:turn'))
    return HttpResponseRedirect(reverse_lazy('mafia:new'))


class AddPlayerView(CreateView):
    model = Player
    template_name = 'mafia/add_player.html'

    def get(self, request):
        player_form = AddPlayerForm()
        more = request.session.get('number') - request.session.get('added_players')
        game = Game(id=request.session.get('game_id'))
        players = game.players.all()
        context = {
            'form': player_form,
            'players': players,
            'more': more,
        }
        return render(request, self.template_name, context)


    def post(self, request):
        player_form = AddPlayerForm(request.POST)
        more = request.session.get('number') - request.session.get('added_players')
        game = Game(id=request.session.get('game_id'))
        if player_form.is_valid():
            player = player_form.save(commit=False)
            player.game = game
            player.save()
            request.session['added_players'] = game.players.count()
            return HttpResponseRedirect(reverse_lazy('mafia:current'))
        players = game.players.all()
        context = {
            'form': player_form,
            'players': players,
            'more': more,
        }
        return render(request, self.template_name, context)


class AddTurnView(CreateView):
    model = Turn
    template_name = 'mafia/turn.html'


def new_view(request):
    if request.session.get('game_id'):
        game_id = request.session.get('game_id')
        context = {
            'game_id': game_id,
        }
        return render(request, 'mafia/new.html', context)
    elif request.GET.get('number'):
        try:
            number = int(request.GET.get('number'))
        except:
            return HttpResponseRedirect(reverse_lazy('mafia:new'))
        if (number < settings.MIN_PLAYERS_COUNT) or (number > settings.MAX_PLAYERS_COUNT):
            return HttpResponseRedirect(reverse_lazy('mafia:new'))
        request.session['number'] = number
        request.session['added_players'] = 0
        game = Game()
        game.save()
        request.session['game_id'] = game.id
        return HttpResponseRedirect(reverse_lazy('mafia:add_player'))
    else:
        form = PlayersNumber
        context = {
            'form': form,
        }
        return render(request, 'mafia/new.html', context)


def delete_game_view(request):
    game = Game(id=request.session['game_id'])
    game.delete()
    del request.session['game_id']
    del request.session['number']
    del request.session['added_players']
    return HttpResponseRedirect(reverse_lazy('mafia:new'))
