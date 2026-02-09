from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, datetime, timedelta

from .models import Patient, Medecin, RendezVous, Consultation, Medicament, Facturation, Ordonnance


class APISmokeTests(APITestCase):
    def setUp(self):
        # create user
        self.username = 'admin'
        self.password = 'admin123'
        self.user = User.objects.create_user(username=self.username, email='admin@hospital.local', password=self.password)

        # create sample patient
        self.patient = Patient.objects.create(
            nom='Durand', prenom='Jean', date_naissance=date(1980, 1, 1),
            adresse='1 rue Test', telephone='0123456789', email='durand.jean@example.com'
        )

        # create sample medecin
        self.medecin = Medecin.objects.create(
            nom='Martin', prenom='Alice', specialite='cardiologie',
            telephone='0987654321', email='alice.martin@example.com', numero_licence='LIC123', adresse_cabinet='Clinique 1'
        )

        # create medicament
        self.medicament = Medicament.objects.create(
            nom='Lisinopril', description='Anti-hypertenseur', prix=12.5, dosage='10mg', fabricant='LabX'
        )

        # rendez-vous
        dt = datetime.now() + timedelta(days=1)
        self.rdv = RendezVous.objects.create(patient=self.patient, medecin=self.medecin, date_heure=dt, motif='Consultation')

        # consultation
        self.consultation = Consultation.objects.create(patient=self.patient, medecin=self.medecin, rendez_vous=self.rdv, diagnostic='Test', traitement='Repos')

        # facturation
        self.facturation = Facturation.objects.create(
            patient=self.patient, consultation=self.consultation, montant=100.0, montant_paye=40.0, date_echeance=date.today(), description='Consultation cardiologie', statut='partiel'
        )

        # API client
        self.client = APIClient()

    def authenticate(self):
        resp = self.client.post('/api/token/', {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_token_and_patients_endpoints(self):
        # token
        resp = self.client.post('/api/token/', {'username': self.username, 'password': self.password}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.json())

        # auth for next requests
        self.authenticate()

        # list patients
        resp = self.client.get('/api/patients/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        # expect at least one
        self.assertTrue(len(data) >= 1 or 'results' in data)

        # patient consultations
        resp = self.client.get(f'/api/patients/{self.patient.id}/consultations/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # patient facturations
        resp = self.client.get(f'/api/patients/{self.patient.id}/facturations/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        json_data = resp.json()
        # if view returns aggregated dict, it contains 'facturations' key
        if isinstance(json_data, dict):
            self.assertIn('facturations', json_data)

    def test_medecin_filter_and_facturation_stats(self):
        self.authenticate()

        # filter medecins by specialite
        resp = self.client.get('/api/medecins/?specialite=cardiologie')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # facturation statistics endpoint
        resp = self.client.get('/api/facturations/statistiques/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        stats = resp.json()
        self.assertIn('total_facturation', stats)
        self.assertIn('total_paye', stats)

    def test_create_patient_post_and_bad_request(self):
        self.authenticate()

        # valid creation
        payload = {
            'nom': 'New', 'prenom': 'Patient', 'date_naissance': '1990-01-01',
            'adresse': 'Adresse 2', 'telephone': '000111222', 'email': 'new.patient@example.com'
        }
        resp = self.client.post('/api/patients/', payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))

        # invalid creation (missing required email)
        bad_payload = {
            'nom': 'Bad', 'prenom': 'NoEmail', 'date_naissance': '1990-01-01',
            'adresse': 'Nowhere', 'telephone': '000'
        }
        resp = self.client.post('/api/patients/', bad_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_patient_put(self):
        self.authenticate()

        update = {'nom': self.patient.nom, 'prenom': self.patient.prenom, 'date_naissance': str(self.patient.date_naissance),
                  'adresse': self.patient.adresse, 'telephone': '999888777', 'email': self.patient.email}
        resp = self.client.put(f'/api/patients/{self.patient.id}/', update, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json().get('telephone'), '999888777')

    def test_enregistrer_paiement_endpoint(self):
        self.authenticate()

        # register a payment that finishes the invoice
        resp = self.client.post(f'/api/facturations/{self.facturation.id}/enregistrer_paiement/', {'montant': 60}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        json_data = resp.json()
        self.assertIn('montant_paye', json_data)
        # montant_paye should now be previous + 60
        expected = float(self.facturation.montant_paye) + 60.0
        self.assertAlmostEqual(float(json_data.get('montant_paye')), expected)

        # invalid payment (zero) should return 400
        resp = self.client.post(f'/api/facturations/{self.facturation.id}/enregistrer_paiement/', {'montant': 0}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_patient_email_and_create_medecin(self):
        self.authenticate()

        # duplicate email should fail
        payload = {
            'nom': 'Dup', 'prenom': 'Email', 'date_naissance': '1990-01-01',
            'adresse': 'X', 'telephone': '111', 'email': self.patient.email
        }
        resp = self.client.post('/api/patients/', payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # create a new medecin via API
        med_payload = {
            'nom': 'Bernard', 'prenom': 'Paul', 'specialite': 'dermatologie',
            'telephone': '123123123', 'email': 'paul.bernard@example.com', 'numero_licence': 'LIC999', 'adresse_cabinet': 'Cabinet 9'
        }
        resp = self.client.post('/api/medecins/', med_payload, format='json')
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))

    def test_rendezvous_unique_constraint(self):
        self.authenticate()
        # attempting to create another RDV with same medecin and date_heure should fail
        dt = self.rdv.date_heure.isoformat()
        payload = {
            'patient': self.patient.id,
            'medecin': self.medecin.id,
            'date_heure': dt,
            'motif': 'Another'
        }
        resp = self.client.post('/api/rendez-vous/', payload, format='json')
        # Model enforces unique_together; DRF returns 400
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ajouter_medicament_to_ordonnance(self):
        self.authenticate()

        # create ordonnance via ORM (serializer does not auto-fill patient/medecin)
        ordonnance = Ordonnance.objects.create(
            consultation=self.consultation,
            patient=self.patient,
            medecin=self.medecin,
            date_expiration=date.today(),
            instructions='Prendre après repas'
        )
        ordonnance_id = ordonnance.id

        # add medication to ordonnance
        add_payload = {'medicament_id': self.medicament.id, 'dosage': '10mg', 'frequence': '2x/jour', 'duree': '5 jours'}
        resp = self.client.post(f'/api/ordonnances/{ordonnance_id}/ajouter_medicament/', add_payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
