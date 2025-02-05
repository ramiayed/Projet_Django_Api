from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .views import register, LoginAPI, ClientDashboardAPI, MechanicDashboardAPI, UserWithVehiclesAPI

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="API Gestion Rendezvous",
        default_version='v1',
        description="Documentation des APIs pour la gestion des utilisateurs",
        contact=openapi.Contact(email="support@rendezvous.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # Vue HTML
    path('register/', register, name='register'),

    # APIs
    path('api/login/', LoginAPI.as_view(), name='login_api'),
    path('api/client-dashboard/', ClientDashboardAPI.as_view(), name='client_dashboard_api'),
    path('api/mechanic-dashboard/', MechanicDashboardAPI.as_view(), name='mechanic_dashboard_api'),
    path('api/user-with-vehicules/', UserWithVehiclesAPI.as_view(), name='user_with_vehicules'),
    # Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
