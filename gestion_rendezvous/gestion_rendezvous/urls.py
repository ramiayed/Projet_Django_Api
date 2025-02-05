
from django.http import HttpResponse  # Ajout pour une vue simple

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehicules/', include('vehicules.urls')),
    #path('factures/', include('factures.urls')),
    path('rendez_vous/', include('rendez_vous.urls')),
    path('users/', include('users.urls')),  # Inclure les URLs de l'application `users`
    path('', RedirectView.as_view(url='/users/register/', permanent=False), name='index'),
    path('stats/', include('stats.urls')),  # Inclusion de l'application stats
    path('facture/', include('facture.urls')),  # Inclusion de l'application factures
     
]
