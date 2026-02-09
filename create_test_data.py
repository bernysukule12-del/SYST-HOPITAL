import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_api.settings')
django.setup()

from api.models import (Patient, Medecin, RendezVous, Consultation, 
                       Medicament, Ordonnance, OrdonnanceMedicament, Facturation)

# Créer des médecins
medecin1 = Medecin.objects.create(
    nom='Dupont',
    prenom='Jean',
    specialite='cardiologie',
    telephone='01 23 45 67 89',
    email='jean.dupont@hospital.com',
    numero_licence='ML001',
    adresse_cabinet='123 Rue de la Santé, Paris'
)

medecin2 = Medecin.objects.create(
    nom='Martin',
    prenom='Marie',
    specialite='dermatologie',
    telephone='01 98 76 54 32',
    email='marie.martin@hospital.com',
    numero_licence='ML002',
    adresse_cabinet='456 Avenue des Médecins, Paris'
)

print(f"✓ {Medecin.objects.count()} médecins créés")

# Créer des patients
patient1 = Patient.objects.create(
    nom='Durand',
    prenom='Sophie',
    date_naissance='1985-05-15',
    genre='F',
    adresse='789 Boulevard Principal, Paris',
    telephone='06 12 34 56 78',
    email='sophie.durand@email.com',
    numero_secu='185051234567890',
    statut='actif'
)

patient2 = Patient.objects.create(
    nom='Laurent',
    prenom='Pierre',
    date_naissance='1990-12-20',
    genre='M',
    adresse='321 Rue Secondaire, Paris',
    telephone='06 98 76 54 32',
    email='pierre.laurent@email.com',
    numero_secu='190122123456789',
    statut='actif'
)

patient3 = Patient.objects.create(
    nom='Blanc',
    prenom='Anne',
    date_naissance='1978-03-08',
    genre='F',
    adresse='654 Avenue Tertaire, Paris',
    telephone='06 55 66 77 88',
    email='anne.blanc@email.com',
    numero_secu='178030876543210',
    statut='actif'
)

print(f"✓ {Patient.objects.count()} patients créés")

# Créer des rendez-vous
rdv1 = RendezVous.objects.create(
    patient=patient1,
    medecin=medecin1,
    date_heure=datetime.now() + timedelta(days=7),
    motif='Consultation cardiaque',
    statut='confirme'
)

rdv2 = RendezVous.objects.create(
    patient=patient2,
    medecin=medecin2,
    date_heure=datetime.now() + timedelta(days=3),
    motif='Contrôle de peau',
    statut='confirme'
)

print(f"✓ {RendezVous.objects.count()} rendez-vous créés")

# Créer des consultations
consultation1 = Consultation.objects.create(
    patient=patient1,
    medecin=medecin1,
    rendez_vous=rdv1,
    diagnostic='Tension artérielle élevée',
    traitement='Médicament antihypertenseur',
    statut='complete'
)

consultation2 = Consultation.objects.create(
    patient=patient3,
    medecin=medecin2,
    diagnostic='Dermatite',
    traitement='Crème anti-inflammatoire',
    statut='complete'
)

print(f"✓ {Consultation.objects.count()} consultations créées")

# Créer des médicaments
med1 = Medicament.objects.create(
    nom='Lisinopril',
    description='Traitement de l\'hypertension',
    prix=15.50,
    composition='Lisinopril dihydrate',
    dosage='10mg',
    fabricant='Pharma SA'
)

med2 = Medicament.objects.create(
    nom='Crème Dermatologique',
    description='Traitement des inflammations cutanées',
    prix=25.00,
    composition='Hydrocortisone',
    dosage='1%',
    fabricant='DermaLabs'
)

med3 = Medicament.objects.create(
    nom='Ibuprofen',
    description='Analgésique anti-inflammatoire',
    prix=8.99,
    composition='Ibuprofen',
    dosage='400mg',
    fabricant='MedPharma'
)

print(f"✓ {Medicament.objects.count()} médicaments créés")

# Créer des ordonnances
ordonnance1 = Ordonnance.objects.create(
    consultation=consultation1,
    patient=patient1,
    medecin=medecin1,
    date_expiration=datetime.now().date() + timedelta(days=30),
    instructions='Prendre 1 comprimé le matin avec un verre d\'eau'
)

OrdonnanceMedicament.objects.create(
    ordonnance=ordonnance1,
    medicament=med1,
    dosage='10mg',
    frequence='1 fois par jour',
    duree='30 jours'
)

ordonnance2 = Ordonnance.objects.create(
    consultation=consultation2,
    patient=patient3,
    medecin=medecin2,
    date_expiration=datetime.now().date() + timedelta(days=14),
    instructions='Appliquer sur la zone affectée'
)

OrdonnanceMedicament.objects.create(
    ordonnance=ordonnance2,
    medicament=med2,
    dosage='1%',
    frequence='2 fois par jour',
    duree='14 jours'
)

print(f"✓ {Ordonnance.objects.count()} ordonnances créées")

# Créer des facturations
facture1 = Facturation.objects.create(
    patient=patient1,
    consultation=consultation1,
    montant=150.00,
    montant_paye=150.00,
    date_echeance=datetime.now().date() + timedelta(days=30),
    statut='paye',
    description='Consultation cardiaque'
)

facture2 = Facturation.objects.create(
    patient=patient3,
    consultation=consultation2,
    montant=80.00,
    montant_paye=40.00,
    date_echeance=datetime.now().date() + timedelta(days=30),
    statut='partiel',
    description='Consultation dermatologique'
)

facture3 = Facturation.objects.create(
    patient=patient2,
    montant=120.00,
    montant_paye=0.00,
    date_echeance=datetime.now().date() + timedelta(days=20),
    statut='impaye',
    description='Consultation générale'
)

print(f"✓ {Facturation.objects.count()} facturations créées")

print("\n" + "="*50)
print("✓ Données de test créées avec succès !")
print("="*50)
print(f"\nRésumé :")
print(f"  - Médecins : {Medecin.objects.count()}")
print(f"  - Patients : {Patient.objects.count()}")
print(f"  - Rendez-vous : {RendezVous.objects.count()}")
print(f"  - Consultations : {Consultation.objects.count()}")
print(f"  - Médicaments : {Medicament.objects.count()}")
print(f"  - Ordonnances : {Ordonnance.objects.count()}")
print(f"  - Facturations : {Facturation.objects.count()}")
