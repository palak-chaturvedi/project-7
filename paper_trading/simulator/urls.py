from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', ClientHomePage, name="client_homepage"),
    path('logout/', logout, name="logout"),
    path('newuser/', clientNewuser, name="clientNewuser"),
    path('dashboard/', dashboard, name="Dashboard"),
    path('trade/<str:stockname>', trade, name="Trade"),
    path('history/', history, name="History"),
    path('stocks/', stockTracker, name="Stocks"),
]
