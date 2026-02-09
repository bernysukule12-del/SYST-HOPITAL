from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum
from decimal import Decimal, InvalidOperation
from .models import (Patient, Medecin, Consultation, Medicament, Facturation,
                     RendezVous, Ordonnance, OrdonnanceMedicament)
from .serializers import (PatientSerializer, MedecinSerializer, ConsultationSerializer,
                         MedicamentSerializer, FacturationSerializer, RendezVousSerializer,
                         OrdonnanceSerializer, OrdonnanceMedicamentSerializer)

# JWT Token personnalisé
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# ViewSets
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'genre']
    search_fields = ['nom', 'prenom', 'email', 'telephone']
    ordering_fields = ['date_enregistrement', 'nom', 'prenom']
    ordering = ['-date_enregistrement']
    

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def consultations(self, request, pk=None):
        patient = self.get_object()
        consultations = patient.consultations.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def facturations(self, request, pk=None):
        patient = self.get_object()
        facturations = patient.facturations.all()
        serializer = FacturationSerializer(facturations, many=True)
        total = facturations.aggregate(Sum('montant'))['montant__sum'] or 0
        paye = facturations.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
        return Response({
            'facturations': serializer.data,
            'total': total,
            'paye': paye,
            'solde': total - paye
        })

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def rendez_vous(self, request, pk=None):
        patient = self.get_object()
        rdv = patient.rendez_vous.all()
        serializer = RendezVousSerializer(rdv, many=True)
        return Response(serializer.data)

class MedecinViewSet(viewsets.ModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialite']
    search_fields = ['nom', 'prenom', 'email', 'specialite']
    ordering_fields = ['nom', 'prenom', 'specialite']
    ordering = ['nom', 'prenom']

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def consultations(self, request, pk=None):
        medecin = self.get_object()
        consultations = medecin.consultations.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def rendez_vous(self, request, pk=None):
        medecin = self.get_object()
        rdv = medecin.rendez_vous.filter(statut='confirme')
        serializer = RendezVousSerializer(rdv, many=True)
        return Response(serializer.data)

class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'medecin']
    search_fields = ['patient__nom', 'patient__prenom', 'medecin__nom']
    ordering_fields = ['date_heure', 'date_creation']
    ordering = ['-date_heure']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirmer(self, request, pk=None):
        rdv = self.get_object()
        rdv.statut = 'confirme'
        rdv.save()
        return Response({'status': 'rendez-vous confirmé'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def annuler(self, request, pk=None):
        rdv = self.get_object()
        rdv.statut = 'annule'
        rdv.save()
        return Response({'status': 'rendez-vous annulé'})

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'medecin', 'patient']
    search_fields = ['patient__nom', 'patient__prenom', 'medecin__nom']
    ordering_fields = ['date_consultation', 'statut']
    ordering = ['-date_consultation']

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def ordonnance(self, request, pk=None):
        consultation = self.get_object()
        if hasattr(consultation, 'ordonnance'):
            serializer = OrdonnanceSerializer(consultation.ordonnance)
            return Response(serializer.data)
        return Response({'detail': 'Pas d\'ordonnance pour cette consultation'}, status=status.HTTP_404_NOT_FOUND)

class MedicamentViewSet(viewsets.ModelViewSet):
    queryset = Medicament.objects.all()
    serializer_class = MedicamentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nom', 'description', 'fabricant']
    ordering_fields = ['nom', 'prix']
    ordering = ['nom']

class OrdonnanceViewSet(viewsets.ModelViewSet):
    queryset = Ordonnance.objects.all()
    serializer_class = OrdonnanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['patient', 'medecin']
    ordering_fields = ['date_ordonnance']
    ordering = ['-date_ordonnance']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def ajouter_medicament(self, request, pk=None):
        ordonnance = self.get_object()
        medicament_id = request.data.get('medicament_id')
        dosage = request.data.get('dosage')
        frequence = request.data.get('frequence')
        duree = request.data.get('duree')

        try:
            medicament = Medicament.objects.get(id=medicament_id)
            OrdonnanceMedicament.objects.create(
                ordonnance=ordonnance,
                medicament=medicament,
                dosage=dosage,
                frequence=frequence,
                duree=duree
            )
            return Response({'status': 'Médicament ajouté'})
        except Medicament.DoesNotExist:
            return Response({'error': 'Médicament non trouvé'}, status=status.HTTP_404_NOT_FOUND)

class FacturationViewSet(viewsets.ModelViewSet):
    queryset = Facturation.objects.all()
    serializer_class = FacturationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['statut', 'patient']
    search_fields = ['patient__nom', 'patient__prenom']
    ordering_fields = ['date_facturation', 'montant', 'statut']
    ordering = ['-date_facturation']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enregistrer_paiement(self, request, pk=None):
        facture = self.get_object()
        montant = request.data.get('montant')

        try:
            montant = Decimal(str(montant))
        except (InvalidOperation, TypeError):
            return Response({'error': 'Montant invalide'}, status=status.HTTP_400_BAD_REQUEST)

        if montant <= 0:
            return Response({'error': 'Le montant doit être positif'}, status=status.HTTP_400_BAD_REQUEST)

        facture.montant_paye = facture.montant_paye + montant
        if facture.montant_paye >= facture.montant:
            facture.statut = 'paye'
        else:
            facture.statut = 'partiel'
        facture.save()

        return Response({
            'status': 'Paiement enregistré',
            'montant_paye': float(facture.montant_paye),
            'solde': float(facture.montant - facture.montant_paye)
        })

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def statistiques(self, request):
        total_facture = Facturation.objects.aggregate(Sum('montant'))['montant__sum'] or 0
        total_paye = Facturation.objects.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
        impaye = Facturation.objects.filter(statut='impaye').count()
        
        return Response({
            'total_facturation': total_facture,
            'total_paye': total_paye,
            'total_impaye': total_facture - total_paye,
            'nombre_factures_impayees': impaye
        })
