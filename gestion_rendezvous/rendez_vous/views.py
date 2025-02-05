from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from vehicules.models import Vehicule
from .models import RendezVous
from .serializers import RendezVousSerializer


@swagger_auto_schema(
    method="get",
    tags=["RendezVous"],
    responses={200: RendezVousSerializer(many=True)}
)
@api_view(["GET"])
def liste_rendez_vous(request):
    """
    Liste des rendez-vous selon le rôle de l'utilisateur.
    - Mécanicien : Affiche ses propres rendez-vous.
    - Client : Affiche ses propres rendez-vous.
    """
    user = request.user
    if user.groups.filter(name="Mechanic").exists():
        rendez_vous = RendezVous.objects.filter(mecanicien=user)
    else:
        rendez_vous = RendezVous.objects.filter(client=user)

    serializer = RendezVousSerializer(rendez_vous, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    tags=['RendezVous'],
    request_body=RendezVousSerializer,
    responses={201: RendezVousSerializer}
)
@api_view(['POST'])
def creer_rendez_vous(request):
    serializer = RendezVousSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()  # Le client sera automatiquement défini dans le serializer
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(
    method="get",
    tags=["RendezVous"],
    responses={200: RendezVousSerializer}
)
@api_view(["GET"])
def detail_rendez_vous(request, id):
    """
    Récupérer les détails d'un rendez-vous spécifique.
    """
    rendez_vous = get_object_or_404(RendezVous, id=id)
    serializer = RendezVousSerializer(rendez_vous, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="put",
    tags=["RendezVous"],
    request_body=RendezVousSerializer,
    responses={200: RendezVousSerializer}
)
@api_view(["PUT"])
def modifier_rendez_vous(request, id):
    """
    Modifier un rendez-vous existant.
    """
    rendez_vous = get_object_or_404(RendezVous, id=id)
    serializer = RendezVousSerializer(rendez_vous, data=request.data, partial=True, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="delete",
    tags=["RendezVous"],
    responses={204: "Rendez-vous supprimé avec succès"}
)
@api_view(["DELETE"])
def supprimer_rendez_vous(request, id):
    """
    Supprimer un rendez-vous existant.
    """
    rendez_vous = get_object_or_404(RendezVous, id=id)
    rendez_vous.delete()
    return Response({"message": "Rendez-vous supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method="patch",
    tags=["RendezVous"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "accepte": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="True = accepté, False = refusé"),
        },
        required=["accepte"],
    ),
    responses={200: "Statut mis à jour avec succès"}
)
@api_view(['PATCH'])
def update_rendezvous_status(request, id):
    rendez_vous = get_object_or_404(RendezVous, id=id)
    status = request.data.get("status")

    if status not in ['pending', 'accepted', 'refused']:
        return Response({"error": "Valeur invalide pour 'status'."}, status=status.HTTP_400_BAD_REQUEST)

    rendez_vous.status = status
    rendez_vous.save()
    return Response({"message": "Statut mis à jour avec succès.", "status": status}, status=status.HTTP_200_OK)