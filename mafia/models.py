from django.db import models

# Create your models here.

ROLE_CHOICES = (
    ('pea', "мирний"),
    ('maf', "мафія"),
    ('pro', "прокурор"),
    ('doc', "лікар"),
    ('man', "маніяк"),
)

TURN_CHOICES = (
    ('d', "день"),
    ('n', "ніч"),
)

class PlayerName(models.Model):
    title = models.CharField(max_length=16)


class Game(models.Model):
    pass


class Player(models.Model):
    name = models.ForeignKey(
        PlayerName,
        on_delete=models.CASCADE,
        related_name="players",
    )
    role = models.CharField(
        max_length=3,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="players",
    )


class Turn(models.Model):
    type = models.CharField(
        max_length=1,
        choices=TURN_CHOICES,
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="turns",
    )