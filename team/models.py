from django.db import models

class Team(models.Model):
    """Model for Teams"""
    name = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

class PlayerProfile(models.Model):
    """Model for additional informations about Players."""
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    nationality = models.CharField(max_length=100)


class Player(models.Model):
    """The Player model"""
    POSITIONS = [
        ("goalkeeper", "Goal Keeper"),
        ("forward", "Forward"),
        ("defense", "Midfielder"),
        ("striker", "Striker"),
        ("substitute", "Substitute")
    ]
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    position = models.CharField(max_length=100, choices=POSITIONS)
    teams = models.ManyToManyField(Team, through="TeamReg")
    profile = models.OneToOneField(PlayerProfile, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name


class TeamReg(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()


class Games(models.Model):
    """The Games Model"""
    game_date = models.DateField()
    opponent = models.CharField(max_length=100)
    score = models.PositiveIntegerField()


class GoalsScored(models.Model):
    """Model for scores"""
    game = models.ForeignKey(Games, on_delete=models.CASCADE)
    minute = models.PositiveIntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="goals_scored")
