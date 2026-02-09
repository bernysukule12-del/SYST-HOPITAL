from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'message': 'Bienvenue dans Hospital API',
        'version': '1.0.0',
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
    path('api/', include('api.urls')),
]
