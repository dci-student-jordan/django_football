# Generated by Django 4.2.9 on 2024-01-29 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playeruser',
            name='height',
        ),
        migrations.RemoveField(
            model_name='playeruser',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='playeruser',
            name='weight',
        ),
        migrations.AlterField(
            model_name='playeruser',
            name='profile',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='team.player'),
        ),
    ]