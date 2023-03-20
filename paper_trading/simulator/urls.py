from django.urls import path, include
from .views import *
from .views import dashboard
urlpatterns = [
    path('', include('authenticate.urls')),
    path('dashboard/', dashboard, name="Dashboard"),
    path('trade/<str:stockname>', trade, name="Trade"),
    path('track/<str:username>', track, name="Track"),
    path('history/', history, name="History"),
    path('stocks/', stockTracker, name="Stocks"),
    path('google/', goog_ts, name="goog_ts"),
    path('apple/', appl_ts, name="appl_ts"),
    path('view_users/',view_users, name="viewUsers"),
    path('learn/',learn, name="learn"),
    path('topg/', topg, name='topg'),
]
