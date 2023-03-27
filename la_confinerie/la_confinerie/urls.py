"""la_confinerie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib.auth import urls

urlpatterns = [
    # Espace regroupant les page d'accueil et 'about us'
    path('', include(('homepage.urls', 'homepage'), namespace='homepage')),
    # Tous les sous-liens de l'app store sont regroupé dans cet espace
    path('store/', include(('store.urls', 'store'), namespace='store')),


    path('admin/', admin.site.urls),
    path('accounts/', include('login.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Ajout permettant de regrouper les images des
# produits lors de l'enregistrement de ces derniers dans le fichier media. Permet de créer un url simplifiant l'appel des images


if settings.DEBUG:  # Création de la toolbar django
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
