from django.db import models

class Player(models.Model):
    """The Player model"""
    POSITIONS = (
        ("goalkeeper", "Goal Keeper"),
        ("forward", "Forward"),
        ("midfielder", "Middle"),
        ("defense", "Defense"),
        ("striker", "Striker"),
        ("substitute", "Substitute")
    )
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    position = models.CharField(max_length=100, choices=POSITIONS)

class Games(models.Model):
    """The Games Model"""
    game_date = models.DateField()
    opponent = models.CharField(max_length=100)
    score = models.PositiveIntegerField()

class GoalsScored(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="goals_scored")