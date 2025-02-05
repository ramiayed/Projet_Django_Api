# facture/serializers.py
from rest_framework import serializers
from .models import Facture

class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facture
        fields = ['id', 'client', 'rendez_vous', 'date_emission', 'montant_total', 'est_payee']
        read_only_fields = ['id', 'date_emission']
