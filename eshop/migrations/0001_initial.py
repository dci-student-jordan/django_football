# Generated by Django 5.0.2 on 2024-03-05 11:55

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
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
                ('price', models.PositiveIntegerField()),
                ('size', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=100)),
                ('size', models.CharField(choices=[('S', 'S'), ('XS', 'XS'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('X', 'X')], default='S', max_length=100)),
                ('number', models.IntegerField()),
                ('address', models.TextField()),
                ('payment', models.IntegerField(choices=[(1, 'Paypal'), (2, 'Card'), (3, 'Apple')], default=1)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
