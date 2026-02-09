from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (PatientViewSet, MedecinViewSet, ConsultationViewSet, MedicamentViewSet, 
                    FacturationViewSet, RendezVousViewSet, OrdonnanceViewSet,
                    CustomTokenObtainPairView)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'medecins', MedecinViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'medicaments', MedicamentViewSet)
router.register(r'facturations', FacturationViewSet)
router.register(r'rendez-vous', RendezVousViewSet)
router.register(r'ordonnances', OrdonnanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
