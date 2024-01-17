from man_pop.pop_players import create_players
from man_pop.pop_eshop import create_items
from man_pop.pop_games_and_goals_scored import create_games, populate_goals, update_goals
from man_pop.pop_p_profile import create_infos, create_teams, create_player_to_teams_relations

def pop_db():
    print("popping players")
    create_players()
    print("popping shopItems")
    create_items
    print("popping games")
    create_games()
    print("popping goalsscores")
    populate_goals()
    print("updating goals")
    update_goals()
    print("popping playerinfos")
    create_infos()
    print("popping teams")
    create_teams()
    print("creating player to teams relations")
    create_player_to_teams_relations()