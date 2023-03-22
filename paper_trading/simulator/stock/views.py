from django.http import HttpResponse
from django.shortcuts import render

from stock.utils import varsha, get_local
from stock.utils import top
#from stock.utils import scraper

# Create your views here.


def index(request):
    #scraper.scr_call()
    print("Reached Views.index")
    return render(request, 'stock/index.html', context=None)


def dashboard(request):
    return render(request, 'stock/dashboard.html', context=None)


def reports(request):
    return render(request, 'stock/reports.html', context=None)


def topg(request):
    gainers = top.top_gainers()
    losers = top.top_losers()
    con = {
        'gainers': gainers,
        'losers': losers,
    }
    return render(request, 'stock/topg.html', con)


def current(request):
    return render(request, 'stock/current.html', context=None)


def today(request):
    return render(request, 'stock/today.html', context=None)


def experts(request):
    return render(request, 'stock/experts.html', context=None)


def company_reviews(request):
    return render(request, 'stock/company_reviews.html', context=None)


def todays_comments(request):
    return render(request, 'stock/todays_comments.html', context=None)


def graph(request):
    return render(request, 'stock/graph.html', context=None)


def try_python(request):
    result = varsha.x()
    return render(request, 'stock/trial.html', {'result':result})


