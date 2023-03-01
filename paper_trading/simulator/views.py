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
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import EmailMessage
from accounts.models import *


@login_required(login_url = 'client_homepage')
def dashboard(request):
    print(request.user.email)

    user = Account.objects.get(email=request.user.email)
    print(user.cash)
    # print("kkkkkkkkkkkkkkkkkkk")
    print(user.name)
    # trades = Trade.objects.filter(user=request.user)
    # stocks = []
    # for trade in trades:
    #     stocks.append(trade.stock)
    # context = {
    #     'stocks': stocks
    # }
    # return render(request, 'dashboard.html', context)



# @login_required(login_url = 'client_homepage')
def trade(request,stockname):
    print(stockname)
    # stocks = Stock.objects.create(symbol="AAPL",price=19)
    # stocks.save()
    # stocks2 = Stock.objects.create(symbol="GOOGL",price=20)
    # stocks2.save()

    # list = Stock.objects.ge


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

        # retrieve user's portfolio
        # portfolio = Account.objects.get(user=request.user)
        print(request.user.email)
        user = Account.objects.get(email=request.user.email)
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
                # messages.error(request, 'Not enough cash to make the trade.')
                return render(request, 'trade.html')
            else:
                # deduct cost from user's cash
                user.cash -= decimal.Decimal(cost)
                # update user's portfolio
                # user.stocks.update_or_create(symbol=symbol, defaults={'shares': shares})
                # create a new trade
                Trade.objects.create(user=request.user, stock=symbol, shares=shares, type='buy', cost=cost)
                user.save()
        else:
            # trade type is sell
            # retrieve the stock from the user's portfolio
            stock = user.stocks.get(symbol=symbol)
            # check if user has enough shares to sell
            if stock.shares < int(shares):
                # raise an error if not enough shares
                # messages.error(request, 'Not enough shares to sell.')
                return render(request, 'trade.html')
            else:
                # update the user's portfolio
                stock.shares -= int(shares)
                stock.save()
                # add the sale value to user's cash
                user.cash += stock.price * int(shares)
                user.save()
                # create a new trade
                trade = Trade.objects.create(user=request.user, symbol=symbol, shares=shares, type='sell',
                                     cost=stock.price * int(shares))

        # messages.success(request, 'Trade successfully executed.')
        return redirect('Dashboard')
    else:
        # stock_picker = tickers_nifty50()
        # result = {}
        # for sym in stock_picker:
        #     data = get_quote_table(sym)
        #     result.update({sym:data['Open']})
        #
        # print(result)
        data = get_quote_table(stockname)
        ctxt = {
            'sym':stockname,
            'open':data['Open']
        }
        return render(request, 'trade2.html', ctxt)

# @login_required(login_url = 'client_homepage')
def history(request):
    # user = User.objects.get(request.user.email)
    # trades = Trade.objects.filter(user=user)
    trades = Trade.objects.all()
    context = {
        'trades': trades
    }
    print(context)
    return HttpResponse(context)
    # return render(request, 'history.html', context)


def ClientHomePage(request):
    if(request.method == "GET"):
        return render(request, "login.html")
    else:
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            print("Hello")
            return redirect('Dashboard')
            # return HttpResponse("Logged in")


        else:
            print("Hellp")
            # return HttpResponse("Logged in")
            return redirect('client_homepage')



def clientNewuser(request):
    if(request.method == "GET"):
        return render(request, "create_user.html")
    else:
        # print("ok")

        name = request.POST.get('name', 0)
        phone_number = request.POST.get('phonenumber', 0)
        password = request.POST.get('password', 0)
        email = request.POST.get('email', 0)

        try:
            print("yes")
            value = Account.objects.get(email = email)
            return redirect('client_homepage')
        except ObjectDoesNotExist:
            pass
        user = Account.objects.create_user(name=name, email=email, phone_number=phone_number, password=password)
        user.is_active = True
        user.save()

        return redirect('client_homepage')



def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('client_homepage')


def stockTracker(request):
    if (request.method == "GET"):
        stockpicker = tickers_nifty50()
        data = {}
        available_stocks = tickers_nifty50()
        # for i in stockpicker:
        #     if i in available_stocks:
        #         pass
        #     else:
        #         return HttpResponse("Error")

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
        # ctxt = {
        #     'sym':stockname,
        #     'open':data['Open']
        # }
        print(data)


        return render(request, 'stocktracker.html',
                      {'data': {stockname:data},'result':stock_picker})    # is_loginned = await checkAuthenticated(request)
    # if not is_loginned:
    #     return HttpResponse("Login First")
    # stockpicker = request.GET.getlist('stockpicker')
    # stockshare = str(stockpicker)[1:-1]
    # stockpicker = tickers.ni
    # print(stockpicker)
