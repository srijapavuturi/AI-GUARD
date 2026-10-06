from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Signup
    path(
        "signup/",
        views.signup_view,
        name="signup"
    ),

    # Login
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # Logout
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Analyze Job
    path(
        "api/analyze/",
        views.analyze_job,
        name="analyze_job"
    ),

    # History
    path(
        "history/",
        views.history,
        name="history"
    ),

    # Delete Analysis
    path(
        "history/delete/<int:id>/",
        views.delete_analysis,
        name="delete_analysis"
    ),
]

