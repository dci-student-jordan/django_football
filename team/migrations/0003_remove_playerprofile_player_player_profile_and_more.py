# Generated by Django 4.2.9 on 2024-01-19 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_playerprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerprofile',
            name='player',
        ),
        migrations.AddField(
            model_name='player',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='team.playerprofile'),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(choices=[('goalkeeper', 'Goal Keeper'), ('forward', 'Forward'), ('defense', 'Midfielder'), ('striker', 'Striker'), ('substitute', 'Substitute')], max_length=100),
        ),
    ]