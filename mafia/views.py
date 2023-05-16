from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import ListView, CreateView, View

from .models import PlayerName, Game, Player, Turn, Move, role_display
from .forms import AddPlayerNameForm, PlayersNumber, ChoosePlayerNameForm, ChoosePlayerForm

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
        return HttpResponseRedirect(reverse_lazy('mafia:players'))


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
        game = Game.objects.get(id=request.session.get('game_id'))
        more = request.session.get('number') - request.session.get('added_players')
        players = Player.objects.filter(game=game)
        all_players = PlayerName.objects.all()
        form = ChoosePlayerNameForm(players=all_players)
        assigned_players = []
        for player in players:
            assigned_players.append(player)
        context = {
            'form': form,
            'assigned_players': assigned_players,
            'more': more,
        }
        return render(request, self.template_name, context)


    def post(self, request):
        game = Game.objects.get(id=request.session.get('game_id'))
        player_name = PlayerName.objects.get(id=request.POST['player'])
        if Player.objects.filter(name=player_name).exists():
            return HttpResponseRedirect(reverse_lazy('mafia:current'))
        player = Player(name=player_name,game=game)
        player.save()
        request.session['added_players'] = Player.objects.filter(game=game).count()
        return HttpResponseRedirect(reverse_lazy('mafia:current'))


class AssignPlayerRoleView(View):

    def get(self, request, role):
        game = Game.objects.get(id=request.session.get('game_id'))
        players = Player.objects.filter(game=game)
        form = ChoosePlayerForm(players=players)
        assigned_players = []
        for player in players:
            if hasattr(player,'role'):
                assigned_players.append(player)
        context = {
            'form': form,
            'assigned_players': assigned_players,
            'role': role,
            'role_display': role_display(role),
        }
        return render(request, 'mafia/add_player_role.html', context)

    def post(self, request, role):
        player = Player.objects.get(id=request.POST['player'])
        player.role = role
        player.save()
        if role == 'maf':
            print('>>>>>> add role redirect to role maf')
            return HttpResponseRedirect(reverse_lazy('mafia:role', args=['maf']))
        print('>>>>>> add role redirect to current from last')
        game = Game.objects.get(id=request.session.get('game_id'))
        if role == 'man':
            game.man_assigned = True
            game.save()
        if role == 'pro':
            game.pro_assigned = True
            game.save()
        if role == 'doc':
            game.doc_assigned = True
            game.save()
            Player.objects.filter(game=game, role=None).update(role='pea')
        return HttpResponseRedirect(reverse_lazy('mafia:current'))


def end_maf(request):
    game = Game.objects.get(id=request.session.get('game_id'))
    game.maf_assigned = True
    game.save()
    return HttpResponseRedirect(reverse_lazy('mafia:turn'))


class AddMoveView(CreateView):
    model = Move
    template_name = 'mafia/add_move.html'

    def get(self, request, pk, role):
        game = Game.objects.get(id=request.session.get('game_id'))
        players = Player.objects.filter(game=game, dead=False)
        dead_players = Player.objects.filter(game=game, dead=True)
        form = ChoosePlayerForm(players=players)
        turn = Turn.objects.get(id=pk)
        turns = Turn.objects.filter(game=game).order_by('-id')
        context = {
            'form': form,
            'turn': turn,
            'turns': turns,
            'role': role,
            'role_display': role_display(role),
            'dead_players': dead_players,
        }
        return render(request, 'mafia/add_move.html', context)

    def post(self, request, pk, role):
        turn = Turn.objects.get(id=pk)
        player = Player.objects.get(id=request.POST['player'])
        move = Move(turn=turn,role=role,choice=player)
        move.save()
        return HttpResponseRedirect(reverse_lazy('mafia:turn'))


def finish_game(request, data):
    context = {
        'congrats': data,
    }
    return render(request, 'mafia/end_game.html', context)


def new_night_turn(game):
    print('>>>>>> new_night_turn started')
    turn = Turn(game=game, type='n')
    turn.save()
    if game.maf_assigned:
        print('>>>>>> redirect to move-maf')
        return HttpResponseRedirect(reverse_lazy('mafia:move', args=[turn.id, 'maf']))
    print('>>>>>> redirect to role-maf')
    return HttpResponseRedirect(reverse_lazy('mafia:role', args=['maf']))


def new_day_turn(game):
    turn = Turn(game=game, type='d')
    turn.save()
    return HttpResponseRedirect(reverse_lazy('mafia:move', args=[turn.id,'pea']))


def finish_turn(request, turn):
    moves = Move.objects.filter(turn=turn)
    if Move.objects.filter(turn=turn, role='doc').exists():
        saved_player = Move.objects.get(turn=turn, role='doc').choice
    else:
        saved_player = None
    for move in moves:
        chosen_player = move.choice
        if move.role == 'doc':
            turn.add_log('{} -> {} ({})\n'.format(
                move.get_role_display(),
                chosen_player.name,
                chosen_player.get_role_display()
            ))
        elif move.role == 'pro':
            turn.add_log('{} -> {} ({})\n'.format(
                move.get_role_display(),
                chosen_player.name,
                chosen_player.get_role_display()
            ))
        else:
            if chosen_player != saved_player:
                chosen_player.dead = True
                chosen_player.save()
                turn.add_log('{} -> {} ({})\n'.format(
                    move.get_role_display(),
                    chosen_player.name,
                    chosen_player.get_role_display()
                ))
            else:
                turn.add_log('лікар врятував: {} -> {} ({})\n'.format(
                    move.get_role_display,
                    chosen_player.name,
                    chosen_player.get_role_display))
    turn.done = True
    turn.save()
    peace_players = Player.objects.filter(game=turn.game).exclude(role='maf')
    peace = False
    for player in peace_players:
        if not player.dead:
            peace = True
    mafia_players = Player.objects.filter(game=turn.game, role='maf')
    mafia = False
    for player in mafia_players:
        if not player.dead:
            mafia = True
    if mafia and peace:
        return new_day_turn(turn.game)
    elif peace:
        return finish_game(request, 'Перемогли мирні жителі!')
    else:
        return finish_game(request, 'Перемогла МАФІЯ!')


def turn_view(request):
    if not request.session.get('game_id'):
        return HttpResponseRedirect(reverse_lazy('mafia:new'))
    print('>>>>>> turn.view started - point 1')
    number = request.session.get('number')
    added_players = request.session.get('added_players')
    if added_players < number:
        return HttpResponseRedirect(reverse_lazy('mafia:add_player'))

    game = Game.objects.get(id=request.session.get('game_id'))
    if not Turn.objects.filter(game=game).exists():
        return new_night_turn(game)

    turn = Turn.objects.filter(game=game).order_by('-id')[0]
    print('>>>>>> turn.view started - point 2')
    if turn.type == 'd':
        if hasattr(turn, 'moves'):
            move = Move.objects.get(turn=turn)
            player = move.choice
            player.dead = True
            player.save()
            turn.add_log('голосування: {} -> {} ({})\n'.format(
                move.get_role_display(),
                player.name,
                player.get_role_display()))
            turn.done = True
            turn.save()
            mafia_players = Player.objects.filter(game=game, role='maf')
            mafia = False
            for player in mafia_players:
                if not player.dead:
                    mafia = True
            peace_players = Player.objects.filter(game=turn.game).exclude(role='maf')
            peace = False
            for player in peace_players:
                if not player.dead:
                    peace = True
            if mafia and peace:
                return new_night_turn(game)
            elif peace:
                return finish_game(request, 'Перемогли мирні жителі!')
            else:
                return finish_game(request, 'Перемогла МАФІЯ!')
    if turn.type == 'd':
        return HttpResponseRedirect(reverse_lazy('mafia:move', args=[turn.id,'pea']))
    print('>>>>>> turn.view started - point 3')
    if not game.maf_assigned:
        print('>>>>>> turn.view started - point 4')
        HttpResponseRedirect(reverse_lazy('mafia:role', args=['maf']))
    if hasattr(turn, 'moves'):
        print('>>>>>> turn.view started - point 5')
        if Move.objects.filter(turn=turn,role='doc').exists():
            return finish_turn(request, turn)
        if Move.objects.filter(turn=turn,role='pro').exists():
            if not game.doc_assigned:
                return HttpResponseRedirect(reverse_lazy('mafia:role', args=['doc']))
            if not Player.objects.get(game=game, role='doc').dead:
                return HttpResponseRedirect(reverse_lazy('mafia:move', args=[turn.id, 'doc']))
            else:
                return finish_turn(request, turn)
        if Move.objects.filter(turn=turn,role='man').exists():
            if not game.pro_assigned:
                return HttpResponseRedirect(reverse_lazy('mafia:role', args=['pro']))
            if not Player.objects.get(game=game, role='pro').dead:
                return HttpResponseRedirect(reverse_lazy('mafia:move', args=[turn.id, 'pro']))
            else:
                return finish_turn(request, turn)
        if Move.objects.filter(turn=turn,role='maf').exists():
            if not game.man_assigned:
                return HttpResponseRedirect(reverse_lazy('mafia:role', args=['man']))
            if not Player.objects.get(game=game, role='man').dead:
                return HttpResponseRedirect(reverse_lazy('mafia:move', args=[turn.id, 'man']))
            return finish_turn(request, turn)
    print('>>>>>> turn.view started - point 6')
    return HttpResponseRedirect(reverse_lazy('mafia:move', args=[turn.id,'maf']))


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
