# Generated by Django 4.2.1 on 2023-05-16 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maf_assigned', models.BooleanField(default=False)),
                ('man_assigned', models.BooleanField(default=False)),
                ('pro_assigned', models.BooleanField(default=False)),
                ('doc_assigned', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name="Ім'я гравця")),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('d', 'день'), ('n', 'ніч')], max_length=1)),
                ('done', models.BooleanField(default=False)),
                ('log', models.TextField(blank=True, default='', max_length=2000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='turns', to='mafia.game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, choices=[('pea', 'мирний'), ('maf', 'мафія'), ('pro', 'прокурор'), ('doc', 'лікар'), ('man', 'маніяк')], max_length=3, null=True)),
                ('dead', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='mafia.game')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='mafia.playername')),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('pea', 'мирний'), ('maf', 'мафія'), ('pro', 'прокурор'), ('doc', 'лікар'), ('man', 'маніяк')], max_length=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('choice', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chosen', to='mafia.player')),
                ('turn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='mafia.turn')),
            ],
        ),
    ]
