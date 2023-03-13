from django.urls import path, include
from .views import logout, dashboard, trade, history, stockTracker, view_users, track
from .views import dashboard
urlpatterns = [
    path('', include('authenticate.urls')),
    # path('login/', ClientHomePage, name="client_homepage"),
    # path('logout/', logout, name="logout"),
    # path('newuser/', clientNewuser, name="clientNewuser"),
    path('dashboard/', dashboard, name="Dashboard"),
    path('trade/<str:stockname>', trade, name="Trade"),
    path('track/<str:username>', track, name="Track"),
    path('history/', history, name="History"),
    path('stocks/', stockTracker, name="Stocks"),
    path('view_users/',view_users, name="viewUsers")
]
