from django.shortcuts import HttpResponse
from django.urls import reverse
from .models import Player, GoalsScored, Games
from django.db.models import Count
from django.db.models.functions import ExtractYear


# Create your views here.

def shop_link():
    url=reverse("eshop_home")
    return f"""</br>
                <h3>Wanna buy from our online Shop?"</h3>
                <a href={url}>e-Shop</a>"""

def homePageView(request):
    url1=reverse("about_page")
    url2=reverse("team_page")
    url3=reverse("scores_page")
    url4=reverse("seasons_page")
    page = f"""
     <!DOCTYPE html>
        <html>
            <body>

                <h1>This is the web page for our favorite Team!</h1>
                <a href={url1}>about</a></br>
                <a href={url2}>Team</a></br>
                <a href={url3}>Goals per player</a></br>
                <a href={url4}>Seasons</a>
                {shop_link()}
            </body>
        </html> 
    """
    return HttpResponse(page)

def about(request):
    url1=reverse("home_page")
    page = f"""
     <!DOCTYPE html>
        <html>
            <body>

                <h1>About</h1>
                <a href={url1}>home</a>
                <p>CONTACT</p>
                {shop_link()}

            </body>
        </html> 
    """
    return HttpResponse(page)


def team_players(request):
    url1=reverse("home_page")
    url2=reverse("about_page")
    url3=reverse("scores_page")
    players = Player.objects.all()
    page_part1 = f"""
     <!DOCTYPE html>
        <html>
            <body>

                <a href={url1}>home</a><br>
                <a href={url2}>about</a><br>
                <a href={url3}>Scores</a>
                <h1>Here are our players, ordered by Position:</h1>
                <ul>"""
    positions = Player.objects.values_list("position", flat=True)
    for position in list(positions.distinct()):
        #name of position
        page_part1 += f"<li><h3>{position}</h3>"
        # number of players in position
        page_part1 += f"<p>number of players: {list(positions).count(position)}</p><ol>"
        for player in players:
            if player.position == position:
                #add link to player
                player_url = reverse("player_data", args=[player.id])
                page_part1 += f'<li><a href ="{player_url}">' + player.name + "</a></li>"
        page_part1 += "</ol></li>"
    page_part1 += f"""
                </ul>
                {shop_link()}
            </body>
        </html> 
    """
    return HttpResponse(page_part1)

def player(request, player_id):
    url = reverse("home_page")
    url2 = reverse("team_page")
    url3=reverse("scores_page")
    player = Player.objects.get(id=player_id)
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Our Scores</title>
    </head>
    <body>
    <a href = "{url}">Home Page</a><br>
    <a href = "{url2}">Team Page</a><br>
    <a href = "{url3}">Scorers Page</a>
    <h1>About Player {player_id}</h1>
    <p>Name:{player.name}</p>
    <p>Age:{player.age}</p>
    <p>Position:{player.position}</p>
    <p>Goals: {len(GoalsScored.objects.filter(player=player_id))}</p>
    </br>
                {shop_link()}
    </body>
    </html>
    """
    return HttpResponse(page)

def scorers(request):
    url = reverse("home_page")
    url2 = reverse("team_page")
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Our Seasons</title>
    </head>
    <body>
    <a href = "{url}">Home Page</a><br>
    <a href = "{url2}">Team Page</a>
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
    return HttpResponse(page)

def best_seasons(request):
    url = reverse("home_page")
    url2 = reverse("team_page")
    page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Our Team</title>
    </head>
    <body>
    <a href = "{url}">Home Page</a><br>
    <a href = "{url2}">Team Page</a>
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
            print(player_url, scorer['player_name'], year)
    page += f"""</ol>
    </br>
    {shop_link()}
    </body>
    </html>
    """
    return HttpResponse(page)