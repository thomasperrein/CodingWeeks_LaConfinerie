from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
#Création d'une classe User personnalisé s'appuyant sur les propriétés de l'abstract user fourni par Django
#Les attributs : password, username, et email sont inclus dans AbstractUser

class User(AbstractUser):
    """
    Custom user model that need email, first name, last name, password, groupe in order to be created
    """
    #Création de la propriété Type associé à l'utilisateur, avec deux champs possibles : Vendeur ou Client
    class Types(models.TextChoices):
        SELLER = "SELLER" , "Seller"
        CLIENT = "CLIENT", "Client"

    type = models.CharField(_('Type'), max_length=30, choices=Types.choices, default=Types.CLIENT)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)

#Nécessaire pour les formulaires et l'ajout de données
class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return(super().get_queryset(*args, **kwargs).filter(type=User.Types.SELLER))

class ClientManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return(super().get_queryset(*args, **kwargs).filter(type=User.Types.CLIENT))

#Subdivision de l'objet User (Group) pour lui donner ou non certaines propriétés (des permissions par exemple)
class Seller(User):
    objects = SellerManager()
    class Meta:
        proxy = True #pour se 'connecter' aux attributs du User
        permissions = (
            ("sell_product", "Can sell products"), #il peut vendre des produits
            )
    
    
    def save(self, *args,**kwargs):
        if not self.pk:
            self.type = User.Types.SELLER
        return(super().save(*args, **kwargs))

#Pas de propriétés particulières 
class Client(User):
    objects = ClientManager()
    class Meta:
        proxy = True

    def save(self, *args,**kwargs):
        if not self.pk:
            self.type = User.Types.CLIENT
        return(super().save(*args, **kwargs))