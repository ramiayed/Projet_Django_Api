from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Swagger schema view pour vehicules
schema_view = get_schema_view(
    openapi.Info(
        title="API Véhicules",
        default_version='v1',
        description="Documentation des APIs pour la gestion des véhicules",
        contact=openapi.Contact(email="support@rendezvous.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register(r'', VehicleViewSet, basename='vehicle')

urlpatterns = router.urls + [
    # Swagger documentation spécifique à l'application véhicules
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-vehicules'),
]
