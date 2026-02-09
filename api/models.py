from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Patient(models.Model):
    GENRE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin'), ('A', 'Autre')]
    STATUT_CHOICES = [('actif', 'Actif'), ('inactif', 'Inactif'), ('suspendu', 'Suspendu')]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, default='M')
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    numero_secu = models.CharField(max_length=15, unique=True, blank=True, null=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_enregistrement']

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Medecin(models.Model):
    SPECIALITES_CHOICES = [
        ('cardiologie', 'Cardiologie'),
        ('dermatologie', 'Dermatologie'),
        ('neurologie', 'Neurologie'),
        ('pediatrie', 'Pédiatrie'),
        ('psychiatrie', 'Psychiatrie'),
        ('chirurgie', 'Chirurgie'),
        ('ophtalmologie', 'Ophtalmologie'),
        ('dentiste', 'Dentiste'),
        ('autre', 'Autre'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=50, choices=SPECIALITES_CHOICES)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    numero_licence = models.CharField(max_length=20, unique=True)
    adresse_cabinet = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"Dr. {self.prenom} {self.nom}"

class RendezVous(models.Model):
    STATUT_RDV = [
        ('confirme', 'Confirmé'),
        ('annule', 'Annulé'),
        ('complete', 'Complété'),
        ('reporte', 'Reporté'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='rendez_vous')
    date_heure = models.DateTimeField()
    motif = models.CharField(max_length=255)
    statut = models.CharField(max_length=15, choices=STATUT_RDV, default='confirme')
    notes = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_heure']
        unique_together = ['medecin', 'date_heure']

    def __str__(self):
        return f"RDV {self.patient} - Dr. {self.medecin.prenom} - {self.date_heure}"

class Consultation(models.Model):
    STATUT_CONSULTATION = [
        ('en_cours', 'En cours'),
        ('complete', 'Complétée'),
        ('suspendue', 'Suspendue'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='consultations')
    rendez_vous = models.OneToOneField(RendezVous, on_delete=models.SET_NULL, null=True, blank=True)
    date_consultation = models.DateTimeField(auto_now_add=True)
    diagnostic = models.TextField()
    traitement = models.TextField()
    statut = models.CharField(max_length=15, choices=STATUT_CONSULTATION, default='complete')
    notes_supplementaires = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_consultation']

    def __str__(self):
        return f"Consultation de {self.patient} avec {self.medecin} le {self.date_consultation}"

class Medicament(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    composition = models.TextField(blank=True, null=True)
    dosage = models.CharField(max_length=100)
    fabricant = models.CharField(max_length=100)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Ordonnance(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='ordonnance')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ordonnances')
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name='ordonnances')
    date_ordonnance = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField()
    instructions = models.TextField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_ordonnance']

    def __str__(self):
        return f"Ordonnance {self.id} - {self.patient} ({self.date_ordonnance})"

class OrdonnanceMedicament(models.Model):
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='medicaments')
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequence = models.CharField(max_length=100)  # Ex: "3 fois par jour"
    duree = models.CharField(max_length=100)  # Ex: "7 jours"
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicament} - {self.dosage}"

class Facturation(models.Model):
    STATUT_PAIEMENT = [
        ('paye', 'Payé'),
        ('partiel', 'Paiement partiel'),
        ('impaye', 'Impayé'),
        ('annule', 'Annulé'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='facturations')
    consultation = models.OneToOneField(Consultation, on_delete=models.SET_NULL, null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    date_facturation = models.DateField(auto_now_add=True)
    date_echeance = models.DateField()
    statut = models.CharField(max_length=15, choices=STATUT_PAIEMENT, default='impaye')
    description = models.TextField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_facturation']

    def __str__(self):
        return f"Facture {self.id} - {self.patient} - {self.montant}€"
