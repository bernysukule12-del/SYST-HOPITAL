from rest_framework import serializers
from .models import (Patient, Medecin, Consultation, Medicament, Facturation, 
                     RendezVous, Ordonnance, OrdonnanceMedicament)

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'age', 'date_naissance', 'genre', 'adresse', 
                  'telephone', 'email', 'numero_secu', 'statut', 'date_enregistrement', 'notes']
        read_only_fields = ['date_enregistrement']
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_naissance.year - ((today.month, today.day) < (obj.date_naissance.month, obj.date_naissance.day))

class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ['id', 'nom', 'prenom', 'specialite', 'telephone', 'email', 'numero_licence', 'adresse_cabinet', 'date_ajout']
        read_only_fields = ['date_ajout']

class RendezVousSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    medecin = MedecinSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient', write_only=True)
    medecin_id = serializers.PrimaryKeyRelatedField(queryset=Medecin.objects.all(), source='medecin', write_only=True)

    class Meta:
        model = RendezVous
        fields = ['id', 'patient', 'patient_id', 'medecin', 'medecin_id', 'date_heure', 'motif', 'statut', 'notes', 'date_creation']
        read_only_fields = ['date_creation']

class ConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    medecin = MedecinSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient', write_only=True)
    medecin_id = serializers.PrimaryKeyRelatedField(queryset=Medecin.objects.all(), source='medecin', write_only=True)
    rendez_vous_id = serializers.PrimaryKeyRelatedField(queryset=RendezVous.objects.all(), source='rendez_vous', write_only=True, required=False)

    class Meta:
        model = Consultation
        fields = ['id', 'patient', 'patient_id', 'medecin', 'medecin_id', 'rendez_vous_id', 
                  'date_consultation', 'diagnostic', 'traitement', 'statut', 'notes_supplementaires']
        read_only_fields = ['date_consultation']

class MedicamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicament
        fields = ['id', 'nom', 'description', 'prix', 'composition', 'dosage', 'fabricant', 'date_creation']
        read_only_fields = ['date_creation']

class OrdonnanceMedicamentSerializer(serializers.ModelSerializer):
    medicament = MedicamentSerializer(read_only=True)
    medicament_id = serializers.PrimaryKeyRelatedField(queryset=Medicament.objects.all(), source='medicament', write_only=True)

    class Meta:
        model = OrdonnanceMedicament
        fields = ['id', 'medicament', 'medicament_id', 'dosage', 'frequence', 'duree', 'notes']

class OrdonnanceSerializer(serializers.ModelSerializer):
    medicaments = OrdonnanceMedicamentSerializer(many=True, read_only=True)
    patient = PatientSerializer(read_only=True)
    medecin = MedecinSerializer(read_only=True)
    consultation_id = serializers.PrimaryKeyRelatedField(queryset=Consultation.objects.all(), source='consultation', write_only=True)

    class Meta:
        model = Ordonnance
        fields = ['id', 'consultation_id', 'patient', 'medecin', 'date_ordonnance', 
                  'date_expiration', 'instructions', 'notes', 'medicaments']
        read_only_fields = ['date_ordonnance', 'patient', 'medecin']

class FacturationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), source='patient', write_only=True)
    solde = serializers.SerializerMethodField()

    class Meta:
        model = Facturation
        fields = ['id', 'patient', 'patient_id', 'montant', 'montant_paye', 'solde', 
                  'date_facturation', 'date_echeance', 'statut', 'description', 'notes']
        read_only_fields = ['date_facturation']
    
    def get_solde(self, obj):
        return obj.montant - obj.montant_paye
