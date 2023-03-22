from django.contrib import admin
from django.urls import path, include

from django.urls import path, include
from .views import *

urlpatterns = [
    path("", predict, name="predict"),
    path("calculate",calculate,name="calculate")
]