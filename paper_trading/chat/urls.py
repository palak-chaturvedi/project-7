from django.contrib import admin
from django.urls import path, include

from django.urls import path, include
from .views import *

urlpatterns = [
    path("", chatPage, name="chat-page"),
]