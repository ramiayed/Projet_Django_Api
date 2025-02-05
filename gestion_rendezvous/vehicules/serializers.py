from rest_framework import serializers
from .models import Vehicule

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = ['id', 'user', 'vin', 'make', 'model', 'year', 'created_at']
        read_only_fields = ['user', 'created_at']
