from django.shortcuts import render, redirect
from .forms import CreationUserForm, ShopkeeperForm, AvailabilityForm
from .models import User, Seller
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from store.models import Shopkeeper, Product

# Create your views here.

def done(request):
    return(render(request, 'registration/successfulpage.html'))
def login(request):
    return(render(request, 'registration/login.html'))

@login_required()
def profile(request):
    """dashboard de l'user, selon qu'il soit Vendeur ou non, on renvoie un contexte
    pour l'ajouter au template"""
    boolean = request.user.type == 'SELLER'
    if boolean :
        u=Seller.objects.get(username=request.user.username)
        shops = [val for val in u.shop.all()] #Spécifique au ManyToMany Field
        products = [] #Récuparation des objets connectés au Shopkeeper lui meme relié au seller
        for shop in shops :
            v = Product.objects.filter(shopkeeper = shop.id).all()
            for val in v : #.all() pour avoir un itérable
                products.append(val)

        return(render(request,'registration/profile.html',{'type': boolean,'shops':shops , 'products' : products}))
    return(render(request,'registration/profile.html'))


def signup(request):
    """Inscription de l'utilsateur, nécessite l'importation du formulaire. 
    Champs nécessaires : username, email, password, type de compte"""
    if request.method == 'POST':
        form = CreationUserForm(request.POST)
        if form.is_valid():
            form.save()
            return(redirect('successfulpage'))
    else :
        form = CreationUserForm()
    return(render(request,'registration/signup.html', {'form' : form }))

def successfulpage(request):
    return(render(request, 'registration/successfulpage.html'))


@login_required()
def add_shopkeeper(request):
    """Vue pour ajouter un shop, nécessite l'importation du formulaire"""
    if request.user.type == 'SELLER' :
        form = ShopkeeperForm()
        if form.is_valid():
            form.save
            return(render(request,'registration/profile.html',{'form' : form }))
        else :
            form = ShopkeeperForm()
        return(render(request,'registration/add_shopkeeper.html',{'form' : form }))
    else :
        return(render(request,'registration/unauthorized.html'))

@login_required()
def confirmation_add_shopkeeper(request):
    if request.user.type == 'SELLER' :
        name = request.POST.get('name')
        description = request.POST.get('description')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        f = Shopkeeper.objects.create(name=name, description=description,address=address,phone=phone)
        u = Seller.objects.get(username=request.user.username)
        f.seller.add(u)
        context={'name': name}
        return(render(request,'registration/confirmation_add_shopkeeper.html',context=context))
    else :
        return(render(request,'registration/unauthorized.html'))

def logout_view(request):
    logout(request)
    return redirect('/')


@login_required()
def password_reset(request):
    return(render(request,'registration/password_reset_form.html'))
@login_required()
def password_reset_done(request):
    return(render(request,'registration/password_reset_done.html'))

def password_change(request):
    return(render(request,'registration/password_change.html'))

def password_change_done(request):
    return(render(request,'registration/password_change_done.html'))

def password_reset_complete(request):
    return(render(request,'registration/password_reset_complete.html'))

def password_reset_email(request):
    return(render(request,'registration/password_reset_email.html'))

def password_reset_confirm(request):
    return(render(request,'registration/password_reset_confirm.html'))


@login_required()
def availability(request):
    """Formulaire pour le stock des produits non fonctionnel"""
    if request.user.type == 'SELLER' :
        form = AvailabilityForm()
        if form.is_valid():
            form.save()
            return(render(request,'registration/availability.html',{'form' : form }))
        else :
            form = AvailabilityForm()
            return(render(request,'registration/availability.html',{'form' : form }))
    else :
        return(render(request,'registration/unauthorized.html'))

@login_required()
def confirmation_availability(request):
    """idem au dessus"""
    if request.user.type == 'SELLER' :
        return(render(request,'registration/confirmation_availability.html'))
    else :
        return(render(request,'registration/unauthorized.html'))