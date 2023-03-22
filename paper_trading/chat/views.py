from django.shortcuts import render, redirect, HttpResponse

def chatPage(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    return render(request, "chatPage.html",context)
    # return render(request,"new.html")