# Generated by Django 4.2.1 on 2023-05-14 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mafia', '0006_player_dead'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='ended',
            field=models.BooleanField(default=False),
        ),
    ]
