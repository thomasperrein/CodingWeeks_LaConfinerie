from django.urls import include, path, re_path
from django.conf import settings
from store import views


urlpatterns = [
    # page d'acceuil de Store présentattous les produit
    re_path(r'^$', views.listing),
    re_path(r'^(?P<product_id>[0-9]+)/$', views.detail,
            name='detail'),  # détail des produits
    # permet la recherche des produits dans la barre de recherche
    re_path(r'^search/$', views.search, name='search'),
    re_path(r'add/$', views.add_product),
    re_path(r'added_product/', views.confirm_added_product,
            name='confirm_added_product'),
    re_path(r'add/category/$', views.add_category),
    re_path(r'added_category/', views.confirm_added_category,
            name='confirm_added_category'),
    re_path(r'cart/', views.cart, name='cart'),
    re_path(r'remove/', views.remove_from_cart,
        name='remove_from_cart'),
]
