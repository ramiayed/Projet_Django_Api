from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Facture
from .serializers import FactureSerializer


class FactureViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les factures : CRUD.
    """
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restreindre l'accès aux factures appartenant à l'utilisateur connecté.
        """
        return self.queryset.filter(client=self.request.user)

    @swagger_auto_schema(
        operation_description="Lister les factures de l'utilisateur connecté.",
        responses={200: FactureSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        """
        Liste les factures de l'utilisateur connecté.
        """
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Créer une facture.",
        request_body=FactureSerializer,
        responses={201: FactureSerializer},
    )
    def create(self, request, *args, **kwargs):
        """
        Crée une nouvelle facture et associe automatiquement l'utilisateur connecté comme client.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Récupérer les détails d'une facture.",
        responses={200: FactureSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Récupère les détails d'une facture spécifique.
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Mettre à jour une facture existante.",
        request_body=FactureSerializer,
        responses={200: FactureSerializer},
    )
    def update(self, request, *args, **kwargs):
        """
        Met à jour une facture existante.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Supprimer une facture.",
        responses={204: "Facture supprimée avec succès."},
    )
    def destroy(self, request, *args, **kwargs):
        """
        Supprime une facture spécifique.
        """
        return super().destroy(request, *args, **kwargs)
