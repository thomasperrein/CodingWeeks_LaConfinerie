from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpRequest

# Create your views here.


def welcome(request):
    """La vue welcome charge la parge d'accueil du site"""
    template = loader.get_template("./homepage/welcome_page.html")
    return HttpResponse(template.render(request=request))


def about_us(request):
    """La vue about_us renvoie l'utilisateur vers une page html fournissant diverses informations à l'utilisateur"""
    template = loader.get_template('homepage/about_us.html')
    return HttpResponse(template.render(request=request))
