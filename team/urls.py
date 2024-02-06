from django.urls import path
from .views import HomePageView, AboutPageView, TeamPageView, PlayerPageView, ScorerPageView, SeasonsPageView, GamesPageView, GamePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("about/", AboutPageView.as_view(), name="about_page"),
    path("team/", TeamPageView.as_view(), name="team_page"),
    path("team/scorers", ScorerPageView.as_view(), name="scores_page"),
    path("team/seasons", SeasonsPageView.as_view(), name="seasons_page"),
    path("team/games", GamesPageView.as_view(), name="games_page"),
    path("team/game/<int:game_id>", GamePageView.as_view(), name="game_page"),
    path("team/<int:player_id>/", PlayerPageView.as_view(), name="player_data"),
]