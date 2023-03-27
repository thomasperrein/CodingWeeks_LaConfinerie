from django.urls import include, path, re_path
from django.conf import settings
from homepage import views


urlpatterns = [
    re_path(r'^$', views.welcome), #Lien de la page d'accueil, c'est le lien le plus simple de tout le site
    path('about/', views.about_us),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
