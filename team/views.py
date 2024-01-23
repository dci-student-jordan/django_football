from typing import Any
from django.shortcuts import HttpResponse
from django.views.generic.base import TemplateView
from django.urls import reverse
from .models import Player, GoalsScored, Games, PlayerProfile, Team
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.db import connection, reset_queries
from django.utils.safestring import mark_safe
from templates.shared import top_links, shop_link


# Create your views here.  


class HomePageView(TemplateView):
    template_name = "simple.html"
    def get_context_data(self):
        context = {
            "extra_style":"team/style.css",
            "top_header":"Welcome to our favorite team's page!",
            "content_text":"We love, love, love...",
            "navs": mark_safe(top_links(reverse("home_page"), "team")),
            "foot": mark_safe(shop_link())
            }
        return context
        
    
class AboutPageView(TemplateView):
    template_name = "simple.html"
    def get_context_data(self):
        context = {
            "extra_style":"team/style.css",
            "top_header":"About oue favorite team...",
            "content_text":"...there's nothing more to say but... LOVE",
            "navs": mark_safe(top_links(reverse("about_page"), "team")),
            "foot": mark_safe(shop_link())
            }
        return context


class TeamPageView(TemplateView):
    template_name = "team.html"

    def get_context_data(self):
        players = Player.objects.values("id", "name", "position")
        positions = Player.objects.values('position').annotate(count=Count('position'))
        context = {
            "extra_style":"team/style.css",
            "players":players,
            "positions":positions,
            "navs": mark_safe(top_links(reverse("team_page"), "team")),
            "foot": mark_safe(shop_link())
        }
        return context
        

class PlayerPageView(TemplateView):
    template_name = "player.html"

    def get_context_data(self, player_id):
        player = Player.objects.get(id=player_id)
        context = {
            "extra_style":"team/style.css",
            "player":player,
            "goals": GoalsScored.objects.filter(player=player).count(),
            "navs": mark_safe(top_links(reverse("player_data", args=[1]), "team")),
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
            "extra_style":"team/style.css",
            "players":players,
            "navs": mark_safe(top_links(reverse("scores_page"), "team")),
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
            "extra_style":"team/style.css",
            "years":self.sorted_result,
            "navs": mark_safe(top_links(reverse("seasons_page"), "team")),
            "foot": mark_safe(shop_link())
        }
