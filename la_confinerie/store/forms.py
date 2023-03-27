from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList
from django import forms

from .models import Product, Category
from login.models import Client


class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])


class ContactForm(ModelForm):
    class Meta:
        model = Client
        fields = ["last_name", "email"]
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'})
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'shopkeeper',
                  'available', 'picture', 'category')


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ('name',)
