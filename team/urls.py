from django.urls import path
from .views import homePageView, about, team_players, player, scorers, best_seasons

urlpatterns = [
    path("", homePageView, name="home_page"),
    path("about/", about, name="about_page"),
    path("team/", team_players, name="team_page"),
    path("team/scorers", scorers, name="scores_page"),
    path("team/seasons", best_seasons, name="seasons_page"),
    path("team/<int:player_id>/", player, name="player_data"),
]