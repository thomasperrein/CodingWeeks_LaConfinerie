from django.contrib.auth.forms import UserCreationForm
from django import forms
from login.models import User
from django.forms import ModelForm
from store.models import Shopkeeper, Product


class CreationUserForm(UserCreationForm):
    class Meta :
        model = User
        fields = ['username','email', 'password1', 'password2','type']

class ShopkeeperForm(ModelForm):
    class Meta :
        model = Shopkeeper
        fields = ['name','description','address','phone']

class AvailabilityForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name','available']