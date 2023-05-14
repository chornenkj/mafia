from django import forms

from .models import PlayerName, Player

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


class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']