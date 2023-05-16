from django import forms

from .models import PlayerName, Player, Move

from Mafia import settings


class AddPlayerNameForm(forms.ModelForm):
    class Meta:
        model = PlayerName
        fields = ['title']


class PlayersNumber(forms.Form):
    number = forms.IntegerField(
        min_value=settings.MIN_PLAYERS_COUNT,
        max_value=settings.MAX_PLAYERS_COUNT,
        label="Кількість гравців",
        help_text="від {} до {}".format(settings.MIN_PLAYERS_COUNT, settings.MAX_PLAYERS_COUNT)
    )


class ChoosePlayerNameForm(forms.Form):
    player = forms.ChoiceField(label="Виберіть гравця:")

    def __init__(self, players, *args, **kwargs):
        super(ChoosePlayerNameForm, self).__init__(*args, **kwargs)
        self.fields['player'].choices = [(x.pk, x.title) for x in players]


class ChoosePlayerForm(forms.Form):
    player = forms.ChoiceField(label="Виберіть гравця:")

    def __init__(self, players, *args, **kwargs):
        super(ChoosePlayerForm, self).__init__(*args, **kwargs)
        self.fields['player'].choices = [(x.pk, '{} ({})'.format(x.name.title, x.get_role_display())) for x in players]

