from django.db import models
from login.models import Seller, Client
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
#Faire attention avant de mofier la base de données

class Shopkeeper(models.Model):
    # On considère que le vendeur est défini par son nom, i.e. qu'il est unique.
    name = models.CharField(max_length=200, unique=True)
    # (Le site étant dédié aux petis commercants, le cas d'une chaine de distribution sera traité après le MVP)
    # null = True pour le MVP
    description = models.TextField(default="Description de votre entrepôt")
    phone = PhoneNumberField(null=True)
    address = models.CharField(max_length=300, null=True)
    seller = models.ManyToManyField(Seller, related_name='shop')
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    # Catégorie du produit (lait, robe...), une catégorie n'appartient qu'à un seul secteur mais un secteru contient plusieurs catégories

    def __str__(self):
        return self.name


class Product(models.Model):
    # Deux produits peuvent avoir le même nom mais etre vendus par deux commercants différents
    name = models.CharField(max_length=200, unique=False, null=False, blank=False)#indispensable
    description = models.TextField(default="Description de l'objet", null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True) #indispensable
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE) #indispensable
    available = models.BooleanField(default=True)
    picture = models.ImageField(upload_to="pictures/", null=True, blank=True)
    category = models.ManyToManyField(
        Category, related_name='product', blank=True)

    def __str__(self):
        return self.name



class Cart_item(models.Model):
    """Ce sont les sous-commandes d'une commande commerciale"""
    name = models.CharField(max_length=200, unique=False, null=False, blank=False, default='rip')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

