# Generated by Django 5.0.2 on 2024-03-06 10:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_date', models.DateField()),
                ('opponent', models.CharField(max_length=100)),
                ('score', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('position', models.CharField(choices=[('goalkeeper', 'Goal Keeper'), ('forward', 'Forward'), ('defense', 'Midfielder'), ('striker', 'Striker'), ('substitute', 'Substitute')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.PositiveIntegerField()),
                ('weight', models.PositiveIntegerField()),
                ('nationality', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OpponentScoresUserUpated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.PositiveIntegerField()),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.games')),
                ('update_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GoalsScored',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.PositiveIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.games')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals_scored', to='team.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='team.playerprofile'),
        ),
        migrations.CreateModel(
            name='TeamReg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.player')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.team')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='teams',
            field=models.ManyToManyField(through='team.TeamReg', to='team.team'),
        ),
    ]
