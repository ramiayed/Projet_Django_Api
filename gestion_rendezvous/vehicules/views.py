from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Vehicule
from .serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    """
    CRUD pour les véhicules.
    """
    queryset = Vehicule.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associe le véhicule à l'utilisateur connecté
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Restriction : Les clients ne voient que leurs propres véhicules.
        """
        if self.request.user.groups.filter(name="Client").exists():
            return self.queryset.filter(user=self.request.user)
        elif self.request.user.groups.filter(name="Mechanic").exists():
            return self.queryset
        return self.queryset.none()

    @swagger_auto_schema(
        operation_description="Lister les véhicules",
        responses={200: VehicleSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Créer un véhicule",
        responses={201: VehicleSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
