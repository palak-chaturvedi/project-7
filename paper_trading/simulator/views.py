import queue
# from datetime import time
import time
from threading import Thread
import decimal

from django.shortcuts import render, redirect
from .models import User, Stock, Trade
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from yahoo_fin.stock_info import *

from email.headerregistry import Address
from tkinter.font import nametofont
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages, auth
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from stock.utils import varsha, get_local
from stock.utils import top
@login_required(login_url = 'login')
def dashboard(request):
    print(request)
    print("hello")
    print(request.user.username)
    userdeets = UserDetails.objects.get(username = request.user.username)
    print(userdeets.cash)
    stocks = Stock.objects.filter(username = request.user.username)
    print(stocks)
    total_cash = 0
    for stock in stocks:
        price = get_quote_table(str(stock.symbol))['Open'] * int(stock.no_of_shares)
        total_cash += price
    userdeets.profit = round((decimal.Decimal(total_cash) + userdeets.cash - decimal.Decimal(1000000)) / 10000,2)
    userdeets.stock_value = round(decimal.Decimal(total_cash),2)
    userdeets.save()
    context = {
        'stocks': stocks,
        'userdeets':userdeets
    }
    return render(request, 'dashboard.html', context)
#
#
#
#
@login_required(login_url = 'login')
def trade(request,stockname):


    # check if request method is POST
    if request.method == 'POST':
        # return HttpResponse("Hiiii")
        # retrieve user input from the form
        shares = request.POST['shares']
        # trade_type = request.POST['trade_type', False]
        if 'trade_type' in request.POST:
            trade_type = request.POST['trade_type']
        else:
            trade_type = 'buy'

        print(trade_type)
        symbol = stockname
        prev_share = 0
        try:
            stocks = Stock.objects.filter(username=request.user.username, symbol=symbol)
            stock = stocks[0]
            prev_share = stock.no_of_shares
            flag = True

        except:
            flag = False





        print(request.user.email)
        user = UserDetails.objects.get(username=request.user.username)
        # return HttpResponse(str(user)+symbol+ trade_type+str(shares))
        # update user's portfolio based on trade type
        print(user.cash)
        if trade_type == 'buy':
            # calculate the cost of the trade
            data = get_quote_table(symbol)
            price = data['Open']
            cost = price * int(shares)
            # check if user has enough cash to make the trade
            if user.cash < cost:
                # raise an error if not enough cash
                messages.error(request, 'Not enough cash to make the trade.')
                return render(request, 'trade.html')
            else:
                # deduct cost from user's cash
                user.cash -= decimal.Decimal(cost)
                # update user's portfolio
                # user.stocks.update_or_create(symbol=symbol, defaults={'shares': shares})
                # create a new trade

                Trade.objects.create(username = request.user.username, stock=symbol, shares=shares, type='buy', cost=cost)
                user.save()

                updated_shares = int(shares) + prev_share


                obj, created = Stock.objects.update_or_create(username = request.user.username,
                                    symbol=symbol,defaults={'no_of_shares': updated_shares},
                                )
                obj.save()


        else:
            # trade type is sell
            # retrieve the stock from the user's portfolio
            # check if user has enough shares to sell
            if prev_share < int(shares):
                # raise an error if not enough shares
                messages.error(request, 'Not enough shares to sell.')
                return render(request, 'trade.html')
            else:
                # update the user's portfolio
                data = get_quote_table(symbol)
                price = data['Open']
                cost = price * int(shares)
                updated_shares = prev_share - int(shares)
                # add the sale value to user's cash
                user.cash += decimal.Decimal(cost)
                user.save()
                # create a new trade
                Trade.objects.create(username=request.user.username, stock=symbol, shares=shares, type='sell', cost=cost)

                obj, created = Stock.objects.update_or_create(username = request.user.username,
                                    symbol=symbol,defaults={'no_of_shares': updated_shares},
                                )
                obj.save()


        # messages.success(request, 'Trade successfully executed.')
        return redirect('Dashboard')
    else:
        data = get_quote_table(stockname)
        ctxt = {
            'sym':stockname,
            'open':data['Open']
        }
        return render(request, 'trade2.html', ctxt)
#
@login_required(login_url = 'login')
def history(request):
    username = request.user.username
    trades = Trade.objects.filter(username=username)
    # trades = Trade.objects.all()
    context = {
        'trades': trades
    }
    print(context)
    return render(request, 'history.html', context)


def stockTracker(request):
    if (request.method == "GET"):
        stockpicker = tickers_nifty50()
        data = {}
        available_stocks = tickers_nifty50()
        for i in stockpicker:
            if i in available_stocks:
                pass
            else:
                return HttpResponse("Error")

        n_threads = len(stockpicker)
        thread_list = []
        que = queue.Queue()
        start = time.time()
        # for i in stockpicker:
        #     result = get_quote_table(i)
        #     data.update({i: result})
        for i in range(n_threads):
            thread = Thread(target=lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}),
                            args=(que, stockpicker[i]))
            thread_list.append(thread)
            thread_list[i].start()

        for thread in thread_list:
            thread.join()

        while not que.empty():
            result = que.get()
            data.update(result)
        end = time.time()
        time_taken = end - start
        print(time_taken)

        print(data)

        stock_picker = tickers_nifty50()
        return render(request, 'stocktracker.html',
                      {'data': data,'result':stock_picker})

    else:
        # return HttpResponse("HIII")
        # pass
        # print("ok")
        stock_picker = tickers_nifty50()


        stockname = request.POST.get('symbol', 0)
        data = get_quote_table(stockname)
        print(data)


        return render(request, 'stocktracker.html',
                      {'data': {stockname:data},'result':stock_picker})


def view_users(request):
    if (request.method == "GET"):
        users = UserDetails.objects.all().order_by('profit').values()
        return render(request, 'view_users.html',
                      {'users': users,'users':users})

    else:
        # return HttpResponse("HIII")
        # pass
        # print("ok")
        # stock_picker = tickers_nifty50()
        username = request.POST.get('username', 0)

        users = UserDetails.objects.filter(username = username).order_by('-profit').values()
        return render(request, 'view_users.html',
                      {'data': users,'users':users})


def track(request,username):
    trades = Trade.objects.filter(username=username)
    # trades = Trade.objects.all()
    context = {
        'trades': trades
    }
    print(context)
    return render(request, 'history.html', context)

def learn(request):
    return render(request, 'learn.html')


def appl_ts(request):
    return render(request, 'timestamp/AAPL_index.html')
def goog_ts(request):
    return render(request, 'timestamp/GOOG_index.html')
def ibm_ts(request):
    return render(request, 'timestamp/IBM_index.html')
def amzn_ts(request):
    return render(request, 'timestamp/AMZN_index.html')
def jnj_ts(request):
    return render(request, 'timestamp/JNJ_index.html')
def msft_ts(request):
    return render(request, 'timestamp/MSFT_index.html')
def wmt_ts(request):
    return render(request, 'timestamp/WMT_index.html')

def reports(request):
    return render(request, 'stock/reports.html', context=None)


def topg(request):
    gainers = top.top_gainers()
    losers = top.top_losers()
    con = {
        'gainers': gainers,
        'losers': losers,
    }
    return render(request, 'topg.html', con)


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

def index(request):
    #scraper.scr_call()
    print("Reached Views.index")
    return render(request, 'stock/index.html', context=None)