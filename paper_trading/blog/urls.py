from django.urls import path
from .views import *

urlpatterns = [
    path('', showAllArticle, name="showAllArticle"),
    path('addarticle/', AddArticles, name="AddArticle"),
    path('article/<int:id>/', perarticle, name="perarticle")
]
