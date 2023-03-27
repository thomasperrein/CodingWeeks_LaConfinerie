from django.template import loader
from django.db import models
from store.models import *
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, ParagraphErrorList, ProductForm, CategoryForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, Cart_item, Shopkeeper
from login.models import User, Client, Seller
from django.contrib.auth.decorators import login_required


# code recherche de produit


def search(request):
    query = request.GET.get('query')
    products = Product.objects.all()  # products est déjà utilisé
    # récupère tous les vendeurs dont le nom contient l'objet de la recherche
    shopkeeper = Shopkeeper.objects.filter(name__icontains=query)
    if not query:  # Si la recherche est vide, on affiche tous les produits
        products = Product.objects.all()  # OI
        message = 'Voici tous nos produits :'

    else:  # Si le nom d'un vendeur contient l'objet de la recherche, on affiche tous les produits du/des vendeur
        message = 'Voici les produits vendus par le vendeur qui correspond à votre recherche :'
        products = Product.objects.filter(shopkeeper__name__icontains=query)

        if not products.exists():  # On modifie le message si aucun produit n'est proposé par le vendeur
            message = 'Désolé, ce vendeur est bien inscrit mais celui-ci ne propose aucun produit'

    if not shopkeeper.exists():  # Si aucun vendeur ne correspond à la recherche
        # Alors on récupère tous les produits dont le nom contient l'objet de la recherche
        products = Product.objects.filter(name__icontains=query)
        message = 'Voici les produits qui correspondent à votre demande :'

        if not products.exists():  # Si aucun produit n'est trouvé
            message = 'Nous sommes désolés, nous n\'avons pas ce que vous recherchez. Voici les produits disponibles: '
            products = Product.objects.all()  # alors on affiche tous les produits

    context = {
        'query': query,
        'message': message,
        'products': products,
        'name': query,
        'shopkeeper': shopkeeper
    }

    return render(request, "./search_results.html", context)


def detail(request, product_id):
    # erreur 404 si l'id du produit demandé ne correspond pas à l'id d'un produit existant
    product = get_object_or_404(Product, pk=int(product_id))

    shopkeeper = product.shopkeeper

    # RECUPERATON DES INFORMATIONS SUR LE PRODUIT:
    # Disponibilité
    availability = product.available
    if availability == True:
        message_available = 'Oui'
    else:
        message_available = 'Non'
    # Lister les catégories auxquelles appartient le produit
    categories = product.category.all()
    list_categories = ''
    for category in categories:
        list_categories += str(category.name)

    if list_categories == '':
        list_categories = 'Aucune'  # Si le produit n'appartient à aucune catégorie

    context = {
        'product': product,
        'shopkeeper_name': shopkeeper.name,
        'product_available': message_available,
        'product_category': list_categories,
    }

    if request.method == 'POST':
        # Si un compte est connecté, on propose à l'utilisateur d'ajouter le produit à son panier.
        if request.user.is_authenticated:
            context = {
                'product_name': product.name
            }
            add_to_cart(request, product_id)
            # Si le produit a été ajouté, on redirige l'utilisateur vers une page le remerciant
            return render(request, './merci.html', context)
        else:
            # S'il n'est pas connecté, on redirige l'utilisateur vers la page de connexion
            return redirect('/accounts/login')
    return render(request, './detail.html', context)


def listing(request):
    products = Product.objects.all()
    # Pour afficher les produits sur plusieurs page
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Si le numéro de page n'est pas bon
        products = paginator.page(1)
    except EmptyPage:
        # Si l'url est entré manuellement avec un numéro de page qui dépassse le nombre de pages total, alors c'est la dernière page qui est affichée
        products = paginator.page(paginator.num_pages)
    context = {
        'products': products,
        'paginate': True,
    }

    template = loader.get_template("./list.html")
    return HttpResponse(template.render(context, request=request))


@login_required()
def add_product(request):
    if request.user.type == 'SELLER':  # Si le compte connecté est un compte vendeur, alors il a accès à la page
        form = ProductForm()
        return(render(request, 'add_product.html', {'form': form}))
    else:  # Sinon il est renvoyé vers une page lui affichant l'interdi
        template = loader.get_template("./unauthorized.html")
        return HttpResponse(template.render(request=request))


def confirm_added_product(request):
    # Afin de clarifier le code, la focntion est découpée en 2 parties
    # on récupère les informations pour les afficher sur la page de confirmation, ce sont les messages qui seront passés en arguments au html
    product_name = request.POST.get('name')
    product_description = request.POST.get('description')
    product_price = request.POST.get('price')
    product_shopkeeper = request.POST.get('shopkeeper')
    product_available = request.POST.get('available')
    product_picture = request.POST.get('picture')
    product_category = request.POST.get('category')
    if Product.objects.filter(name = product_name).exists():
        template = loader.get_template("error.html")
        return HttpResponse(template.render(request=request))
    if product_available == 'on':
        message_available = 'Oui'  # Pour afficher l'information sur la page de confirmation
        product_available = True  # Variable correspondant au format de la base de données
    else:
        message_available = 'Non'
        product_available = False

    if product_category != None:  # Si une catégorie a été indiquée
        # On récupère le nom de la catégorie indiquée (car resquet.POST renvoie l'id de la catégorie et pas son nom )
        category = Category.objects.get(pk=product_category)
        category_name = category.name
    else:
        # On indiquera sur la page que le produit n'appartient à aucune catégorie
        category_name = 'Aucune'

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # C'est ici que le produit est véritablement enregistré
            product = Product.objects.get(name=product_name)
    product = Product.objects.get(name=product_name)

    context = {
        'product': product,
        'product_description': product_description,
        'product_price': product_price,
        'product_shopkeeper': product_shopkeeper,
        'product_available': message_available,
        'product_picture': product_picture,
        'product_category': category_name,
    }

    template = loader.get_template("confirm_added_product.html")
    return HttpResponse(template.render(context, request=request))


@login_required()
def add_category(request):
    if request.user.type == 'SELLER':
        form = CategoryForm()
        return(render(request, 'add_category.html', {'form': form}))
    else:
        template = loader.get_template("./unauthorized.html")
        return HttpResponse(template.render(request=request))


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_name = request.user.username
    order = Cart_item.objects.create(
        name=user_name, product=product, quantity=1)


def remove_from_cart(request):
    print(5)

    if request.user.is_authenticated:
        user_name = request.user.username
        Cart_item.objects.filter(name=str(user_name)).delete()
        template = loader.get_template("store/base.html")
        return HttpResponse(template.render(request=request))
    else:
        return redirect('/accounts/login')


def cart(request):

    if request.user.is_authenticated:
        user_name = request.user.username
        orders = Cart_item.objects.filter(name=user_name)

        total = 0
        count = 0

        for order in orders:
            total += order.product.price * order.quantity
            count += order.quantity

        context = {
            'total': total,
            'count': count,
            'orders': orders,
        }
        return render(request, 'store/cart.html', context)
    else:
        return redirect('/accounts/login')


def confirm_added_category(request):
    """Vue qui ajoute une catégorie"""
    category_name = str(request.POST.get(
        'name'))  # On récupère le nom de catégorie que l'utilisateur voudrait créer
    category = Category.objects.create(name=category_name)

    # Affichage de la page de confirmation
    context = {'category_name': category_name}
    template = loader.get_template("confirm_added_category.html")
    return HttpResponse(template.render(context, request=request))
