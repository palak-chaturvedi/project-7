from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePage, name="homepage"),
    path('About_us/', About_us, name="about_us"),
    path('Contact_us/', Contact_us, name="Contact_us"),
    path('help/', help, name="help"),
    path('simulator/', include("simulator.urls"), name="simulator"),
    path("chat/", include("chat.urls")),
    path("predict/", include("prediction.urls")),
    path("blog/", include("blog.urls")),
]