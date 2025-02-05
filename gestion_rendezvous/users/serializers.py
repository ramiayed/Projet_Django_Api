from rest_framework import serializers
from .models import User
from django.contrib.auth.models import User
from vehicules.models import Vehicule
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', 'client')  # Rôle par défaut : Client
        )
        return user
    


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = ['id', 'brand', 'model', 'license_plate', 'created_at']

class UserWithVehiclesSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'vehicles']
