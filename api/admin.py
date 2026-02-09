from django.contrib import admin
from .models import (Patient, Medecin, Consultation, Medicament, Facturation,
                     RendezVous, Ordonnance, OrdonnanceMedicament)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'telephone', 'email', 'statut')
    list_filter = ('statut', 'genre', 'date_enregistrement')
    search_fields = ('nom', 'prenom', 'email', 'numero_secu')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance', 'genre')
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'telephone', 'email')
        }),
        ('Médical', {
            'fields': ('numero_secu', 'notes')
        }),
        ('Gestion', {
            'fields': ('statut', 'date_enregistrement', 'date_modification')
        }),
    )
    readonly_fields = ('date_enregistrement', 'date_modification')

@admin.register(Medecin)
class MedecinAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'specialite', 'telephone', 'email')
    list_filter = ('specialite', 'date_ajout')
    search_fields = ('nom', 'prenom', 'specialite', 'email', 'numero_licence')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'numero_licence')
        }),
        ('Spécialisation', {
            'fields': ('specialite',)
        }),
        ('Coordonnées', {
            'fields': ('telephone', 'email', 'adresse_cabinet')
        }),
        ('Gestion', {
            'fields': ('date_ajout',)
        }),
    )
    readonly_fields = ('date_ajout',)

@admin.register(RendezVous)
class RendezVousAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_heure', 'statut')
    list_filter = ('statut', 'date_heure', 'medecin')
    search_fields = ('patient__nom', 'medecin__nom', 'motif')
    readonly_fields = ('date_creation',)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_consultation', 'statut')
    list_filter = ('date_consultation', 'medecin', 'statut')
    search_fields = ('patient__nom', 'medecin__nom', 'diagnostic')
    readonly_fields = ('date_consultation',)
    fieldsets = (
        ('Informations', {
            'fields': ('patient', 'medecin', 'rendez_vous', 'date_consultation')
        }),
        ('Diagnostic et Traitement', {
            'fields': ('diagnostic', 'traitement', 'statut')
        }),
        ('Notes', {
            'fields': ('notes_supplementaires',)
        }),
    )

@admin.register(Medicament)
class MedicamentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'dosage', 'prix', 'fabricant')
    list_filter = ('fabricant', 'date_creation')
    search_fields = ('nom', 'description', 'fabricant')
    readonly_fields = ('date_creation',)

@admin.register(Ordonnance)
class OrdonnanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'medecin', 'date_ordonnance', 'date_expiration')
    list_filter = ('date_ordonnance', 'date_expiration', 'medecin')
    search_fields = ('patient__nom', 'medecin__nom')
    readonly_fields = ('date_ordonnance', 'patient', 'medecin')

@admin.register(OrdonnanceMedicament)
class OrdonnanceMedicamentAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'dosage', 'frequence', 'duree')
    list_filter = ('ordonnance__date_ordonnance',)
    search_fields = ('medicament__nom', 'ordonnance__id')

@admin.register(Facturation)
class FacturationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'montant', 'montant_paye', 'statut', 'date_facturation')
    list_filter = ('statut', 'date_facturation', 'date_echeance')
    search_fields = ('patient__nom', 'patient__prenom')
    readonly_fields = ('date_facturation',)
    fieldsets = (
        ('Patient', {
            'fields': ('patient', 'consultation')
        }),
        ('Montants', {
            'fields': ('montant', 'montant_paye', 'statut')
        }),
        ('Dates', {
            'fields': ('date_facturation', 'date_echeance')
        }),
        ('Description', {
            'fields': ('description', 'notes')
        }),
    )
