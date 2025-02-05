from django.db import models
from django.contrib.auth.models import User

class Vehicule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
    vin = models.CharField(max_length=17, unique=True)  # Numéro de série du véhicule
    make = models.CharField(max_length=50, default="Unknown")  # Marque
    model = models.CharField(max_length=50, default="Unknown")  # Modèle
    year = models.PositiveIntegerField(default=2000)  # Année
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"
