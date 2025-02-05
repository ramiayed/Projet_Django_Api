from django.db import models
from django.contrib.auth.models import User
from vehicules.models import Vehicule
from django.utils.timezone import now

class RendezVous(models.Model):
    client = models.ForeignKey(User, related_name="rendezvous_client", on_delete=models.CASCADE)
    mecanicien = models.ForeignKey(User, related_name="rendezvous_mecanicien", on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    description = models.TextField(blank=True, null=True)
    cout_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'En attente'), ('accepted', 'Accepté'), ('refused', 'Refusé')],
        default='pending'
    )
    vehicule = models.ForeignKey(Vehicule, related_name="rendezvous", on_delete=models.CASCADE)
    creneau_horaire = models.CharField(max_length=50, blank=True, null=True)  # Ajouté
    cout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Ajouté

    def __str__(self):
        return f"Rendez-vous {self.id} - {self.client.username} avec {self.mecanicien.username}"
