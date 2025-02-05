from django.urls import path
from .views import (
    liste_rendez_vous,
    creer_rendez_vous,
    detail_rendez_vous,
    modifier_rendez_vous,
    supprimer_rendez_vous,
    update_rendezvous_status,
)

urlpatterns = [
    path("rendezvous/", liste_rendez_vous, name="liste_rendez_vous"),
    path("rendezvous/create/", creer_rendez_vous, name="creer_rendez_vous"),
    path("rendezvous/<int:id>/", detail_rendez_vous, name="detail_rendez_vous"),
    path("rendezvous/<int:id>/edit/", modifier_rendez_vous, name="modifier_rendez_vous"),
    path("rendezvous/<int:id>/delete/", supprimer_rendez_vous, name="supprimer_rendez_vous"),
    path("rendezvous/<int:id>/status/", update_rendezvous_status, name="update_rendezvous_status"),
]
