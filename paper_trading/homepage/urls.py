from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePage, name="homepage"),
    path('simulator/', include("simulator.urls"), name="simulator"),
    path("chat/", include("chat.urls")),
    path("predict/", include("prediction.urls")),
    path("blog/", include("blog.urls")),
]