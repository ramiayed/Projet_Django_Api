from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import RendezVous
from vehicules.models import Vehicule


class RendezVousSerializer(serializers.ModelSerializer):
    mecanicien = serializers.CharField()  # Nom d'utilisateur du mécanicien
    vehicule = serializers.PrimaryKeyRelatedField(queryset=Vehicule.objects.all())  # ID du véhicule

    class Meta:
        model = RendezVous
        fields = ['id', 'client', 'mecanicien', 'vehicule', 'creneau_horaire', 'status', 'cout']

    def validate_mecanicien(self, value):
        """
        Vérifie que le mécanicien existe et appartient au groupe 'Mechanic'.
        """
        try:
            mecanicien = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Le mécanicien spécifié n'existe pas.")
        
        if not mecanicien.groups.filter(name="Mechanic").exists():
            raise serializers.ValidationError("Le mécanicien spécifié n'appartient pas au groupe 'Mechanic'.")
        
        return mecanicien  # Retourne l'instance User

    def create(self, validated_data):
        """
        Personnalisation de la méthode `create` pour gérer les champs `client` et `mecanicien`.
        """
        # Remplace le champ `mecanicien` (string) par l'instance User validée
        mecanicien = validated_data.pop('mecanicien')  # Récupère la chaîne de caractères
        validated_data['mecanicien'] = self.validate_mecanicien(mecanicien)  # Convertit en instance User

        # Ajoute automatiquement le client à partir du contexte de la requête
        validated_data['client'] = self.context['request'].user

        return super().create(validated_data)
