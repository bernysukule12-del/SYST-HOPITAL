from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from api.models import (
    Patient, Medecin, RendezVous, Consultation, 
    Medicament, Ordonnance, OrdonnanceMedicament, Facturation
)
import random


class Command(BaseCommand):
    help = 'Seed the database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database seed...')
        
        # Create patients
        self.stdout.write('Creating patients...')
        patients = self.create_patients()
        
        # Create doctors
        self.stdout.write('Creating doctors...')
        doctors = self.create_doctors()
        
        # Create medications
        self.stdout.write('Creating medications...')
        medications = self.create_medications()
        
        # Create appointments
        self.stdout.write('Creating appointments...')
        appointments = self.create_appointments(patients, doctors)
        
        # Create consultations
        self.stdout.write('Creating consultations...')
        consultations = self.create_consultations(appointments, doctors)
        
        # Create prescriptions
        self.stdout.write('Creating prescriptions...')
        prescriptions = self.create_prescriptions(consultations, medications)
        
        # Create invoices
        self.stdout.write('Creating invoices...')
        self.create_invoices(patients, consultations)
        
        self.stdout.write(self.style.SUCCESS('[OK] Database seed completed successfully!'))
        self.stdout.write(f'  • {len(patients)} patients created')
        self.stdout.write(f'  • {len(doctors)} doctors created')
        self.stdout.write(f'  • {len(medications)} medications created')
        self.stdout.write(f'  • {len(appointments)} appointments created')
        self.stdout.write(f'  • {len(consultations)} consultations created')
        self.stdout.write(f'  • {len(prescriptions)} prescriptions created')

    def create_patients(self):
        """Create sample patients"""
        patient_data = [
            {'nom': 'Diallo', 'prenom': 'Ahmed', 'email': 'ahmed.diallo@example.com', 'telephone': '77123456', 'genre': 'M', 'date_naissance': '1980-03-15', 'adresse': 'Dakar, Senegal'},
            {'nom': 'Cisse', 'prenom': 'Fatima', 'email': 'fatima.cisse@example.com', 'telephone': '77234567', 'genre': 'F', 'date_naissance': '1985-07-22', 'adresse': 'Dakar, Senegal'},
            {'nom': 'Ba', 'prenom': 'Mamadou', 'email': 'mamadou.ba@example.com', 'telephone': '77345678', 'genre': 'M', 'date_naissance': '1975-11-10', 'adresse': 'Thiès, Senegal'},
            {'nom': 'Sow', 'prenom': 'Awa', 'email': 'awa.sow@example.com', 'telephone': '77456789', 'genre': 'F', 'date_naissance': '1990-01-05', 'adresse': 'Dakar, Senegal'},
            {'nom': 'Toure', 'prenom': 'Ibrahim', 'email': 'ibrahim.toure@example.com', 'telephone': '77567890', 'genre': 'M', 'date_naissance': '1988-06-18', 'adresse': 'Kaolack, Senegal'},
            {'nom': 'Kane', 'prenom': 'Mariam', 'email': 'mariam.kane@example.com', 'telephone': '77678901', 'genre': 'F', 'date_naissance': '1992-09-25', 'adresse': 'Dakar, Senegal'},
            {'nom': 'Ndiaye', 'prenom': 'Ali', 'email': 'ali.ndiaye@example.com', 'telephone': '77789012', 'genre': 'M', 'date_naissance': '1979-12-08', 'adresse': 'Saint-Louis, Senegal'},
            {'nom': 'Gueye', 'prenom': 'Khadija', 'email': 'khadija.gueye@example.com', 'telephone': '77890123', 'genre': 'F', 'date_naissance': '1987-04-30', 'adresse': 'Dakar, Senegal'},
        ]
        
        patients = []
        for data in patient_data:
            patient, created = Patient.objects.get_or_create(
                email=data['email'],
                defaults={
                    'nom': data['nom'],
                    'prenom': data['prenom'],
                    'telephone': data['telephone'],
                    'genre': data['genre'],
                    'date_naissance': data['date_naissance'],
                    'adresse': data['adresse'],
                    'statut': 'actif'
                }
            )
            patients.append(patient)
        
        return patients

    def create_doctors(self):
        """Create sample doctors"""
        doctor_data = [
            {'nom': 'Sall', 'prenom': 'Adama', 'email': 'adama.sall@hospital.com', 'telephone': '77111111', 'specialite': 'cardiologie', 'licence': 'LIC001', 'adresse': '123 Rue des Docteurs'},
            {'nom': 'Camara', 'prenom': 'Ousmane', 'email': 'ousmane.camara@hospital.com', 'telephone': '77222222', 'specialite': 'neurologie', 'licence': 'LIC002', 'adresse': '456 Avenue Médicale'},
            {'nom': 'Traore', 'prenom': 'Aissatou', 'email': 'aissatou.traore@hospital.com', 'telephone': '77333333', 'specialite': 'pediatrie', 'licence': 'LIC003', 'adresse': '789 Boulevard Santé'},
            {'nom': 'Bah', 'prenom': 'Sekou', 'email': 'sekou.bah@hospital.com', 'telephone': '77444444', 'specialite': 'dermatologie', 'licence': 'LIC004', 'adresse': '321 Rue Skin Care'},
        ]
        
        doctors = []
        for data in doctor_data:
            doctor, created = Medecin.objects.get_or_create(
                email=data['email'],
                defaults={
                    'nom': data['nom'],
                    'prenom': data['prenom'],
                    'telephone': data['telephone'],
                    'specialite': data['specialite'],
                    'numero_licence': data['licence'],
                    'adresse_cabinet': data['adresse']
                }
            )
            doctors.append(doctor)
        
        return doctors

    def create_medications(self):
        """Create sample medications"""
        med_data = [
            {'nom': 'Amoxicilline', 'dosage': '500mg', 'description': 'Antibiotique', 'fabricant': 'Pharma Co', 'prix': Decimal('1500')},
            {'nom': 'Ibuprofene', 'dosage': '200mg', 'description': 'Anti-inflammatoire', 'fabricant': 'Medic Inc', 'prix': Decimal('500')},
            {'nom': 'Paracetamol', 'dosage': '1000mg', 'description': 'Analgésique', 'fabricant': 'Health Labs', 'prix': Decimal('300')},
            {'nom': 'Loratadine', 'dosage': '10mg', 'description': 'Antihistaminique', 'fabricant': 'Allergy Care', 'prix': Decimal('400')},
            {'nom': 'Metformine', 'dosage': '500mg', 'description': 'Antidiabétique', 'fabricant': 'Diabetes Corp', 'prix': Decimal('2000')},
            {'nom': 'Vitamine C', 'dosage': '500mg', 'description': 'Supplément vitaminé', 'fabricant': 'Nutrition Plus', 'prix': Decimal('800')},
        ]
        
        medications = []
        for data in med_data:
            med, created = Medicament.objects.get_or_create(
                nom=data['nom'],
                dosage=data['dosage'],
                defaults={
                    'description': data['description'],
                    'fabricant': data['fabricant'],
                    'prix': data['prix'],
                    'composition': f"Ingrédient actif: {data['nom']}"
                }
            )
            medications.append(med)
        
        return medications

    def create_appointments(self, patients, doctors):
        """Create sample appointments"""
        appointments = []
        statuts = ['confirme', 'annule', 'complete']
        motifs = ['Consultation générale', 'Suivi médical', 'Traitement', 'Contrôle', 'Urgence']
        
        for i in range(10):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            statut = random.choice(statuts)
            date_rdv = timezone.now() + timedelta(days=random.randint(1, 30))
            
            rdv, created = RendezVous.objects.get_or_create(
                patient=patient,
                medecin=doctor,
                date_heure=date_rdv,
                defaults={
                    'motif': random.choice(motifs),
                    'statut': statut
                }
            )
            if created:
                appointments.append(rdv)
        
        return appointments

    def create_consultations(self, appointments, doctors):
        """Create consultations from appointments"""
        consultations = []
        
        for appointment in appointments:
            if appointment.statut == 'complete':
                consultation, created = Consultation.objects.get_or_create(
                    rendez_vous=appointment,
                    defaults={
                        'patient': appointment.patient,
                        'medecin': appointment.medecin,
                        'diagnostic': f'Consultation de suivi pour {appointment.patient.prenom} {appointment.patient.nom}',
                        'traitement': 'Continuer le traitement actuel. Revenir en cas de complication.',
                        'statut': 'complete',
                        'notes_supplementaires': 'Patient en bon état de santé'
                    }
                )
                if created:
                    consultations.append(consultation)
        
        return consultations

    def create_prescriptions(self, consultations, medications):
        """Create prescriptions with medications"""
        prescriptions = []
        
        for consultation in consultations:
            date_exp = timezone.now().date() + timedelta(days=30)
            ordonnance, created = Ordonnance.objects.get_or_create(
                consultation=consultation,
                defaults={
                    'medecin': consultation.medecin,
                    'patient': consultation.patient,
                    'date_expiration': date_exp,
                    'instructions': 'Prendre les médicaments selon les instructions. Revenez dans 7 jours.'
                }
            )
            if created:
                prescriptions.append(ordonnance)
                
                # Add 1-3 medications to prescription
                num_meds = random.randint(1, 3)
                for _ in range(num_meds):
                    med = random.choice(medications)
                    OrdonnanceMedicament.objects.get_or_create(
                        ordonnance=ordonnance,
                        medicament=med,
                        defaults={
                            'dosage': f'{random.choice([1, 2, 3])} comprimé(s)',
                            'frequence': random.choice(['1x/jour', '2x/jour', '3x/jour']),
                            'duree': f'{random.randint(5, 14)} jours'
                        }
                    )
        
        return prescriptions

    def create_invoices(self, patients, consultations):
        """Create sample invoices"""
        statuts_paiement = ['paye', 'en attente', 'partiel']
        
        for consultation in consultations:
            montant_total = Decimal(str(random.randint(5000, 50000)))
            montant_paye = montant_total if random.random() > 0.5 else (montant_total * Decimal('0.5'))
            date_ech = timezone.now().date() + timedelta(days=30)
            
            Facturation.objects.get_or_create(
                consultation=consultation,
                defaults={
                    'patient': consultation.patient,
                    'montant': montant_total,
                    'montant_paye': montant_paye,
                    'date_echeance': date_ech,
                    'statut': random.choice(statuts_paiement),
                    'description': f'Facture pour consultation du Dr. {consultation.medecin.prenom} {consultation.medecin.nom}'
                }
            )

