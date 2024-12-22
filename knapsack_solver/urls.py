from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),        # Page d'accueil
    path('knapsack/', views.knapsack_view, name='knapsack'),  # Page du solveur
]
