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
    title = models.CharField(max_length=30, verbose_name="Ім'я гравця")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


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
    ended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


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
    dead = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
