from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from .permissions import IsClient, IsMechanic
from .serializers import UserWithVehiclesSerializer



# ---- Vue pour l'inscription avec un template ---- #
def register(request):
    """
    Vue pour l'inscription d'un utilisateur avec un rôle (avec un template).
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not all([username, email, first_name, last_name, password, role]):
            return render(request, 'users/register.html', {'error': "Tous les champs sont requis."})

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': "Nom d'utilisateur déjà pris."})

        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {'error': "Email déjà utilisé."})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        if role == 'client':
            group, _ = Group.objects.get_or_create(name='Client')
            user.groups.add(group)
        elif role == 'mechanic':
            group, _ = Group.objects.get_or_create(name='Mechanic')
            user.groups.add(group)
        else:
            return render(request, 'users/register.html', {'error': "Rôle invalide."})

        return render(request, 'users/register.html', {'success': "Utilisateur créé avec succès !"})

    return render(request, 'users/register.html')


# ---- API Login ---- #


class UserWithVehiclesAPI(APIView):
    """
    API pour obtenir un utilisateur avec ses véhicules.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserWithVehiclesSerializer(request.user)
        return Response(serializer.data)
class LoginAPI(APIView):
    """
    API pour connecter un utilisateur et retourner un jeton JWT.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Connecter un utilisateur avec un nom d'utilisateur et un mot de passe",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Nom d'utilisateur"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="Mot de passe"),
            },
            required=['username', 'password'],
        ),
        responses={
            200: openapi.Response(
                description="Connexion réussie avec JWT",
                examples={
                    "application/json": {
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
                        "role": "Client",
                    }
                },
            ),
            401: "Nom d'utilisateur ou mot de passe incorrect",
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Nom d'utilisateur et mot de passe requis."}, status=400)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=401)

        refresh = RefreshToken.for_user(user)
        role = user.groups.first().name if user.groups.exists() else "Unknown"

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role,
        }, status=200)


# ---- API pour le tableau de bord client ---- #
class ClientDashboardAPI(APIView):
    """
    API pour le tableau de bord client.
    """
    permission_classes = [IsAuthenticated, IsClient]

    @swagger_auto_schema(
        operation_description="Accéder au tableau de bord client",
        responses={
            200: openapi.Response(
                description="Données du tableau de bord client",
                examples={
                    "application/json": {
                        "message": "Bienvenue, John Doe. Voici votre tableau de bord client."
                    }
                },
            ),
            403: "Permission refusée",
        }
    )
    def get(self, request):
        return Response({
            "message": f"Bienvenue {request.user.first_name}, ceci est votre tableau de bord client."
        })


# ---- API pour le tableau de bord mécanicien ---- #
class MechanicDashboardAPI(APIView):
    """
    API pour le tableau de bord mécanicien.
    """
    permission_classes = [IsAuthenticated, IsMechanic]

    @swagger_auto_schema(
        operation_description="Accéder au tableau de bord mécanicien",
        responses={
            200: openapi.Response(
                description="Données du tableau de bord mécanicien",
                examples={
                    "application/json": {
                        "message": "Bienvenue, Jane Doe. Voici votre tableau de bord mécanicien."
                    }
                },
            ),
            403: "Permission refusée",
        }
    )
    def get(self, request):
        return Response({
            "message": f"Bienvenue {request.user.first_name}, ceci est votre tableau de bord mécanicien."
        })
