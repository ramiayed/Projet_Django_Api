# facture/models.py
from django.db import models
from django.contrib.auth.models import User
from rendez_vous.models import RendezVous

class Facture(models.Model):
    client = models.ForeignKey(User, related_name='factures', on_delete=models.CASCADE)
    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.CASCADE, related_name='facture')
    date_emission = models.DateTimeField(auto_now_add=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    est_payee = models.BooleanField(default=False)

    def __str__(self):
        return f"Facture #{self.id} pour {self.client.username}"
