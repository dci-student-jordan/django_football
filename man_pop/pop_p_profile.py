from team.models import Player, PlayerProfile, Team, TeamReg
from random import randint, choice
from man_pop.pop_games_and_goals_scored import opponents
from faker import Faker
from datetime import datetime, timedelta

nationalities = [
    "American",
    "British",
    "Canadian",
    "Chinese",
    "French",
    "German",
    "Indian",
    "Italian",
    "Japanese",
    "Mexican",
    "Russian",
    "Spanish",
    "Australian",
    "Brazilian",
    "South Korean"
]

cities = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose",
    "Austin",
    "Jacksonville",
    "San Francisco",
    "Charlotte",
    "Indianapolis",
    "Seattle",
    "Denver",
    "Washington",
    "Boston",
    "El Paso",
    "Nashville",
    "Detroit",
    "Portland",
    "Memphis",
    "Oklahoma City",
]

colors = [
    "Red",
    "Blue",
    "Green",
    "Yellow",
    "Purple",
    "Orange",
    "Pink",
    "Brown",
    "Cyan",
    "Magenta",
    "Teal",
    "Lime",
    "Olive",
    "Maroon",
    "Navy",
    "Aquamarine",
    "Turquoise",
    "Indigo",
    "Violet",
    "Beige",
    "Coral",
    "Khaki",
    "Lavender",
    "Salmon",
    "Sienna",
]

def create_infos():
    """populate the prayersprofile table"""
    for player in Player.objects.all():
        PlayerProfile.objects.create(player=player, height=randint(150, 200), weight=randint(75, 95), nationality=choice(nationalities))

def create_teams():
    """populate the teams table"""
    for team in opponents:
        Team.objects.create(name=team, town=choice(cities), color=choice(colors))

def generate_dates(start_year, end_year, num_dates, fake):
    dates = []
    for _ in range(num_dates):
        # Generate a random date within the specified range
        random_date = fake.date_between_dates(date_start=datetime(start_year, 1, 1), date_end=datetime(end_year, 12, 31))
        
        # Ensure dates follow one another by adding a random number of days between 1 and 30
        if dates:
            random_date = dates[-1] + timedelta(days=fake.random_int(min=1, max=30))
        
        dates.append(random_date)

    return dates

def create_player_to_teams_relations():
    fake = Faker()
    teams = Team.objects.all()
    for player in Player.objects.all():
        in_teams = randint(1, 4)
        enter_year = 2022 - in_teams
        other_teams_list = generate_dates(2010, enter_year, in_teams, fake)
        print(f"Teams for {player.name}")
        for entry in range(0, len(other_teams_list)-2):
            team = choice(teams)
            from_date = other_teams_list[entry]
            to_date = other_teams_list[entry+1]
            print(f"{player.name} played at team '{team.name}' from {from_date} till {to_date}")
            TeamReg.objects.create(player=player, team=team, from_date=from_date, to_date=to_date)