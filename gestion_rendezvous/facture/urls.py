from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from .views import FactureViewSet

# Configuration de Swagger pour l'application facture
schema_view = get_schema_view(
    openapi.Info(
        title="Factures API Documentation",
        default_version="v1",
        description="Endpoints pour la gestion des factures",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

# Router pour le ViewSet
router = DefaultRouter()
router.register(r'', FactureViewSet, basename='facture')

urlpatterns = [
    path('', include(router.urls)),  # Endpoints CRUD de l'application facture
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='facture-swagger-ui'),  # Swagger pour l'application facture
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='facture-redoc'),  # Redoc pour l'application facture
]
