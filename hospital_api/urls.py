from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

def home(request):
    return JsonResponse({
        'message': 'Bienvenue dans Hospital API',
        'version': '1.0.0',
        'documentation': {
            'swagger': '/api/docs/',
            'redoc': '/api/redoc/',
            'openapi': '/api/schema/'
        },
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'api_patients': '/api/patients/',
            'api_medecins': '/api/medecins/',
            'api_consultations': '/api/consultations/',
            'api_medicaments': '/api/medicaments/',
            'api_facturations': '/api/facturations/'
        }
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    
    # OpenAPI 3.0 Schema and Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/', include('api.urls')),
]
