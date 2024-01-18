from django.shortcuts import HttpResponse
from django.urls import reverse
from .models import Player, GoalsScored, Games, PlayerProfile, TeamReg
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.db import connection, reset_queries


# Create your views here.

def shop_link():
    url=reverse("eshop_home")
    return f"""</br>
                <h3>Wanna buy from our online Shop?"</h3>
                <a href={url}>e-Shop</a>"""

def top_links(exclude_request):
    """Navigation links excluding the calling page."""
    urls =[
        (reverse("home_page"), "Home"),
        (reverse("about_page"), f"About"),
        (reverse("team_page"), f"Team"),
        (reverse("scores_page"), f"Goals per player"),
        (reverse("seasons_page"), f"Seasons")
    ]
    returnded_urls = ""
    for url in [url for url in urls if not url[0] == exclude_request.path]:
        returnded_urls += f"<a href={url[0]}>{url[1]}</a></br>"
    return returnded_urls
                

def homePageView(request):
    page = f"""
     <!DOCTYPE html>
        <html>
            <body>
                {top_links(request)}
                <h1>This is the web page for our favorite Team!</h1>
                {shop_link()}
            </body>
        </html> 
    """
    return HttpResponse(page)

def about(request):
    page = f"""
     <!DOCTYPE html>
        <html>
            <body>
                {top_links(request)}
                <h1>About</h1>
                <p>CONTACT</p>
                {shop_link()}

            </body>
        </html> 
    """
    return HttpResponse(page)


def team_players(request):
    reset_queries()
    players = Player.objects.values("id", "name", "position")
    page_part1 = f"""
     <!DOCTYPE html>
        <html>
            <body>
                {top_links(request)}
                <h1>Here are our players, ordered by Position:</h1>
                <ul>"""
    positions = Player.objects.values('position').annotate(count=Count('position'))
    # print("POSITIONS:", positions)
    for position in positions:
        pos_name = position["position"]
        pos_count = position["count"]
        #name of position
        page_part1 += f"<li><h3>{pos_name}</h3>"
        # number of players in position
        page_part1 += f"<p>number of players: {pos_count}</p><ol>"
        for player in players:
            if player["position"] == pos_name:
                #add link to player
                player_url = reverse("player_data", args=[player["id"]])
                page_part1 += f'<li><a href ="{player_url}">' + player["name"] + "</a></li>"
        page_part1 += "</ol></li>"
    page_part1 += f"""
                </ul>
                {shop_link()}
            </body>
        </html> 
    """
    print("TEAMPLAYERS:", connection.queries)
    return HttpResponse(page_part1)

def player(request, player_id):
    reset_queries()
    player = Player.objects.get(id=player_id)
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Our Scores</title>
    </head>
    <body>
                {top_links(request)}
    <h1>About Player {player_id}</h1>
    <p>Name:{player.name}</p>
    <p>Age:{player.age}</p>
    <p>Position:{player.position}</p>
    <p>Goals: {len(GoalsScored.objects.filter(player=player))}</p>
    <h3>additional informations:</h3><ul>"""
    player_profile = PlayerProfile.objects.get(player = player)
    for col_name, val in player_profile.__dict__.items():
        if col_name in ["height", "weight", "nationality"]:  # Exclude private attributes
            page += f"""<li>{col_name}: {val}</li>"""
    other_teams = TeamReg.objects.filter(player=player)
    if other_teams:
        page += f"<li><p>Joined our Team: {other_teams[len(other_teams)-1].to_date}</p><h5>former Teams:</h5><ul>"
        for team in other_teams:
            page += f"""<li>Team '{team.team.name}': from {team.from_date} to {team.to_date}</li>"""
        page += "</ul></li>"
    else:
        page += "<li>Joined our Team from the very beginning.</li>"
    page += f"""</ul></br>
                {shop_link()}
    </body>
    </html>
    """
    print("PLAYERS:", connection.queries)
    return HttpResponse(page)

def scorers(request):
    reset_queries()
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Our Seasons</title>
    </head>
    <body>
                {top_links(request)}
    <h1>Our Players goals:</h1>"""
    for player in Player.objects.annotate(total_goals=Count('goals_scored')).order_by('-total_goals'):
        player_url = reverse("player_data", args=[int(player.id)])
        page += f"""<h3><a href={player_url}>{player.name}</a></h3>
                    <p>total goals: {player.total_goals}"""
    page += f"""</body>
    </br>
    {shop_link()}
    </html>
    """
    print("SCORERS:", connection.queries)
    return HttpResponse(page)

def best_seasons(request):
    reset_queries()
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Our Team</title>
    </head>
    <body>
                {top_links(request)}
    <h1>Our Best Seasons so far:</h1>"""
    # This is chatGPT...
    # Query for the number of games per year
    games_per_year = (
        Games.objects
        .annotate(year=ExtractYear('game_date'))
        .values('year')
        .annotate(num_games=Count('id'))
        .order_by('year')
    )

    # Query for the number of goals per year for each player
    goals_per_year = (
        GoalsScored.objects
        .values('player__name', 'game__game_date__year')  # Use 'game__game_date__year' to reference the extracted year
        .annotate(num_goals=Count('id'))
        .order_by('-num_goals')
    )

    # Combine the results into a dictionary for each year
    result_dict = {}
    for goal in goals_per_year:
        year = goal['game__game_date__year']  # Reference the extracted year using 'game__game_date__year'
        if year not in result_dict:
            result_dict[year] = {
                'num_games': 0,
                'total_goals': 0,
                'top_scorers': []
            }

        result_dict[year]['top_scorers'].append({
            'player_name': goal['player__name'],
            'num_goals': goal['num_goals']
        })
        result_dict[year]['total_goals'] += goal['num_goals']

    # Update the result dictionary with the number of games per year
    for game in games_per_year:
        year = game['year']
        if year in result_dict:
            result_dict[year]['num_games'] = game['num_games']

    # Sort the result dictionary by total goals
    sorted_result = sorted(result_dict.items(), key=lambda x: x[1]['total_goals'], reverse=True)

    # Print the sorted result dictionary
    for year, data in sorted_result:
        page += f"""<h2>{year}</h2>
                    <p>Number of games: {data['num_games']}</p>
                    <p>Total goals: {data['total_goals']}</p>
                    <h3>Top Scorers:</h3><ol style='list-style-type: none; padding: 0;'>"""
        for scorer in data['top_scorers']:
            player_url = reverse("player_data", args=[int(Player.objects.get(name=scorer['player_name']).id)])
            # print(player_url)
            page += f"""<li style='display: inline-block; margin-right: 10px';><p><a href={player_url}>{scorer['player_name']}</a> (goals: {scorer['num_goals']})</p>
                        </li>
            """
    page += f"""</ol>
    </br>
    {shop_link()}
    </body>
    </html>
    """
    print("SEASONS:", connection.queries)
    return HttpResponse(page)