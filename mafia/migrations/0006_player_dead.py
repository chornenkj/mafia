# Generated by Django 4.2.1 on 2023-05-14 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mafia', '0005_remove_player_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='dead',
            field=models.BooleanField(default=False),
        ),
    ]
