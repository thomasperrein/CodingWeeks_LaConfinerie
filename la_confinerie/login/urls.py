from django.urls import include, path, re_path
from django.conf import settings
from login import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('successfulpage/',views.successfulpage, name='successfulpage'),
    path('add_shopkeeper/',views.add_shopkeeper, name='add_shopkeeper'),
    path('logout/',views.logout_view,name='logout'),
    path('confirmation_add_shopkeeper/',views.confirmation_add_shopkeeper, name='confirmation_add_shopkeeper'),
    path('confirmation_availability/',views.confirmation_availability,name='confirmation_availability'),
    path('availability/',views.availability,name='availability'),
]




if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
