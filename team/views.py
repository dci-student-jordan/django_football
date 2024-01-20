from typing import Any
from django.shortcuts import HttpResponse
from django.views.generic.base import TemplateView
from django.urls import reverse
from .models import Player, GoalsScored, Games, PlayerProfile, Team
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.db import connection, reset_queries
from django.utils.safestring import mark_safe


# Create your views here.

def shop_link():
    url=reverse("eshop_home")
    return f"""</br>
                <h3>Wanna buy from our online Shop?</h3>
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
    for url in [url for url in urls if not url[0] == exclude_request]:
        returnded_urls += f"<a href={url[0]}>{url[1]}</a></br>"
    return returnded_urls     


class HomePageView(TemplateView):
    template_name = "home.html"
    def get_context_data(self):
        context = {"navs": mark_safe(top_links(reverse("home_page"))), "foot": mark_safe(shop_link())}
        return context
        
    
class AboutPageView(TemplateView):
    template_name = "about.html"
    def get_context_data(self):
        context = {"navs": mark_safe(top_links(reverse("about_page"))), "foot": mark_safe(shop_link())}
        return context


class TeamPageView(TemplateView):
    template_name = "team.html"

    def get_context_data(self):
        players = Player.objects.values("id", "name", "position")
        positions = Player.objects.values('position').annotate(count=Count('position'))
        context = {
            "players":players,
            "positions":positions,
            "navs": mark_safe(top_links(reverse("team_page"))),
            "foot": mark_safe(shop_link())
        }
        return context
        

class PlayerPageView(TemplateView):
    template_name = "player.html"

    def get_context_data(self, player_id):
        player = Player.objects.get(id=player_id)
        context = {
            "player":player,
            "goals": GoalsScored.objects.filter(player=player).count(),
            "navs": mark_safe(top_links(reverse("player_data", args=[1]))),
            "foot": mark_safe(shop_link())
        }
        if player.teams.exists():
            context["teams"] = mark_safe(f"<p>Joined our Team: {player.teamreg_set.last().to_date}</p><h3>Former Teams:</h3>")
        else:
            context["teams"] = "Joined our Team from the very beginning."
        return context


class ScorerPageView(TemplateView):
    template_name = "scorers.html"

    def get_context_data(self):
        players = Player.objects.annotate(total_goals=Count('goals_scored')).order_by('-total_goals')
        return {
            "players":players,
            "navs": mark_safe(top_links(reverse("scores_page"))),
            "foot": mark_safe(shop_link())
        }


class SeasonsPageView(TemplateView):
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
        .values('player__name', 'player__id', 'game__game_date__year')  # Use 'game__game_date__year' to reference the extracted year
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
            'player_id': goal['player__id'],
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

    template_name = "seasons.html"

    def get_context_data(self):
        return {
            "years":self.sorted_result,
            "navs": mark_safe(top_links(reverse("seasons_page"))),
            "foot": mark_safe(shop_link())
        }
