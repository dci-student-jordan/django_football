
from django.urls import path
from .views import LoginView, SignUpView, UpdateUserView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("update/<int:pk>", UpdateUserView.as_view(), name="update"),
]