from django.shortcuts import render, redirect
from .models import User, Stock, Trade, Portfolio
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from ..accounts.models import Account


def dashboard(request):
    user = User.objects.get(id=request.user.id)
    trades = Trade.objects.filter(user=user)
    stocks = []
    for trade in trades:
        stocks.append(trade.stock)
    context = {
        'stocks': stocks
    }
    return render(request, 'trading_simulator/dashboard.html', context)




def trade(request):
    # check if request method is POST
    if request.method == 'POST':
        # retrieve user input from the form
        symbol = request.POST['symbol']
        shares = request.POST['shares']
        trade_type = request.POST['trade_type']

        # retrieve user's portfolio
        portfolio = Portfolio.objects.get(user=request.user)

        # update user's portfolio based on trade type
        if trade_type == 'buy':
            # calculate the cost of the trade
            cost = Stock.objects.get(symbol=symbol).price * int(shares)
            # check if user has enough cash to make the trade
            if portfolio.cash < cost:
                # raise an error if not enough cash
                # messages.error(request, 'Not enough cash to make the trade.')
                return render(request, 'trade.html')
            else:
                # deduct cost from user's cash
                portfolio.cash -= cost
                # update user's portfolio
                portfolio.stocks.update_or_create(symbol=symbol, defaults={'shares': shares})
                # create a new trade
                Trade.objects.create(user=request.user, symbol=symbol, shares=shares, trade_type='buy', cost=cost)
        else:
            # trade type is sell
            # retrieve the stock from the user's portfolio
            stock = portfolio.stocks.get(symbol=symbol)
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
                portfolio.cash += stock.price * int(shares)
                portfolio.save()
                # create a new trade
                Trade.objects.create(user=request.user, symbol=symbol, shares=shares, trade_type='sell',
                                     cost=stock.price * int(shares))

        # messages.success(request, 'Trade successfully executed.')
        return redirect('dashboard')
    else:
        return render(request, 'trade.html')


def history(request):
    user = User.objects.get(id=request.user.id)
    trades = Trade.objects.filter(user=user)
    context = {
        'trades': trades
    }
    return render(request, 'trading_simulator/history.html', context)



def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'simulator/create_user.html', {'form': form})

def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return redirect('dashboard')


def ClientHomePage(request):
    if(request.method == "GET"):
        return render(request, "user_login.html")
    else:
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('homepage')

        else:
            return redirect('client_homepage')

def clientNewuser(request):
    if(request.method == "GET"):
        return render(request, "ClientApp/ClientNewuser.html")
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
