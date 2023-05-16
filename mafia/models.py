from django.db import models

# Create your models here.

ROLE_CHOICES = (
    ('pea', "мирний"),
    ('maf', "мафія"),
    ('pro', "прокурор"),
    ('doc', "лікар"),
    ('man', "маніяк"),
)

def role_display(role):
    if role == 'maf':
        return "мафія"
    if role == 'man':
        return "маніяк"
    if role == 'pro':
        return "прокурор"
    if role == 'doc':
        return "лікар"
    return "мирний"


TURN_CHOICES = (
    ('d', "день"),
    ('n', "ніч"),
)

class PlayerName(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name="Ім'я гравця")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Game(models.Model):
    maf_assigned = models.BooleanField(default=False)
    man_assigned = models.BooleanField(default=False)
    pro_assigned = models.BooleanField(default=False)
    doc_assigned = models.BooleanField(default=False)
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
    done = models.BooleanField(default=False)
    log = models.TextField(max_length=2000, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def log_to_list(self):
        if hasattr(self, 'log'):
            return self.log.split('\n')

    def add_log(self, data):
        self.log = self.log + data + '\n'
        self.save()
        return self.log


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

    def __str__(self):
        return self.name.title


class Move(models.Model):
    turn = models.ForeignKey(
        Turn,
        on_delete=models.CASCADE,
        related_name="moves",
    )
    role = models.CharField(
        max_length=3,
        choices=ROLE_CHOICES,
    )
    choice = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name="chosen",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
