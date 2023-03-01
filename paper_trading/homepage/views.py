from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def HomePage(request):

    return render(request, "home.html")


def About_us(request):
    return HttpResponse("Terms and conditions")


def Contact_us(request):
    return HttpResponse("Terms and conditions")


def help(request):
    return HttpResponse("Terms and conditions")


def tnc(request):
    return HttpResponse("Terms and conditions")


