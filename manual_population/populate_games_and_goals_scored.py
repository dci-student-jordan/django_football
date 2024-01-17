from datetime import datetime, timedelta
from team.models import Games, GoalsScored, Player
import random

opponents = [
    "Thunder Strikers",
    "Solar Titans",
    "Eagle Warriors",
    "Lunar Panthers",
    "Aurora Falcons",
    "Blaze Phoenix",
    "Galactic Wolves",
    "Celestial Hawks",
    "Mystic Griffins",
    "Solaris Lions",
    "Neptune Sharks",
    "Infinity Jaguars",
    "Vortex Raptors",
    "Cosmic Cobras",
    "Velocity Bears",
    "Supernova Tigers",
    "Pinnacle Stallions",
    "Quantum Cougars",
    "Solar Flare Wildcats",
    "Starlight Rhinos",
    "Cosmic Cyclones",
    "Nebula Panthers",
    "Radiant Pegasus",
    "Orion Dragons",
    "Astral Gryphons",
    "Zenith Wolves",
    "Spectra Falcons",
    "Nova Hawks",
    "Interstellar Lions",
    "Dreamscape Jaguars",
]

def saturdays():

    start_date = datetime(2015, 1, 1)
    end_date = datetime(2023, 12, 31)
    saturdays = []

    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() == 5:  # Saturday has a weekday value of 5
            saturdays.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return saturdays

def create_games():
    for _ in range(200):
        Games.objects.create(game_date=random.choice(saturdays()), opponent=random.choice(opponents), score=random.randint(1, 5))

def populate_goals():
    player_ids = Player.objects.values_list("id", flat=True)
    for game in Games.objects.all():
        for goal in range(1, game.score):
            GoalsScored.objects.create(game_id=game.pk, minute=random.randint(0,59), player_id=random.choice(player_ids))