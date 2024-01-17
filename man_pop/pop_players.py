"""Manually call create_players() from this file to populate the team_players table with some players"""

import random
from faker import Faker
from team.models import Player


tplayers = [{'name': 'Christina Chavez', 'age': 19, 'position': 'goalkeeper'}, {'name': 'Elizabeth Hill', 'age': 31, 'position': 'midfielder'}, {'name': 'Deanna Maldonado', 'age': 19, 'position': 'substitute'}, {'name': 'Derek Ryan', 'age': 21, 'position': 'substitute'}, {'name': 'John Martinez Jr.', 'age': 18, 'position': 'forward'}, {'name': 'Aaron Osborne', 'age': 34, 'position': 'striker'}, {'name': 'Natalie Cobb', 'age': 35, 'position': 'midfielder'}, {'name': 'David Mathews', 'age': 34, 'position': 'forward'}, {'name': 'Charles Macdonald', 'age': 21, 'position': 'striker'}, {'name': 'Cynthia Baker', 'age': 25, 'position': 'forward'}, {'name': 'Arthur Bruce', 'age': 27, 'position': 'forward'}, {'name': 'Vincent Goodman', 'age': 24, 'position': 'defender'}, {'name': 'Courtney Moore', 'age': 26, 'position': 'substitute'}, {'name': 'David Vance', 'age': 30, 'position': 'striker'}, {'name': 'Karen Fisher', 'age': 29, 'position': 'midfielder'}, {'name': 'Kelly Allen DVM', 'age': 28, 'position': 'goalkeeper'}, {'name': 'Katherine Walker', 'age': 18, 'position': 'midfielder'}, {'name': 'Ashley Quinn', 'age': 28, 'position': 'forward'}, {'name': 'Carlos Ayers', 'age': 26, 'position': 'forward'}, {'name': 'Jason Delacruz', 'age': 29, 'position': 'midfielder'}, {'name': 'Jeremiah Watkins', 'age': 22, 'position': 'goalkeeper'}, {'name': 'Ronald Stone', 'age': 26, 'position': 'forward'}, {'name': 'Austin Gonzalez', 'age': 28, 'position': 'goalkeeper'}, {'name': 'Robert Gonzalez', 'age': 22, 'position': 'midfielder'}, {'name': 'Johnny Hernandez', 'age': 21, 'position': 'goalkeeper'}]

def create_players ():
    fake = Faker()

    positions = ['goalkeeper', 'forward', 'midfielder', 'defender', 'striker', 'substitute']

    for _ in range(25):
        Player.objects.create(name= fake.name(), age=random.randint(18, 35), position=random.choice(positions))