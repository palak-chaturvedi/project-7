from django.shortcuts import render, HttpResponse, redirect
from .models import Articles
from django.db import models


# Create your views here.


def AddArticles(request):
    if (request.method == "GET"):
        Author = request.user.username
        context = {
            'author': Author
        }
        return render(request, "addArticle.html", context)
    else:
        Author = request.user.username
        Title = request.POST.get('title', 0)
        Description = request.POST.get('disc', 0)
        ArticleImage = request.FILES["articleimage"]
        values = Articles(Author=Author, Title=Title,
                          Description=Description, ArticleImage=ArticleImage)
        values.save()
        return redirect('showAllArticle')



def showAllArticle(request):
    articles = Articles.objects.all()
    context = {
        'Articles': articles
    }
    return render(request, "allArticles.html", context)


def perarticle(request, id):
    article = Articles.objects.get(pk=id)
    context = {
        'Article': article
    }
    return render(request, "perarticle.html", context)
