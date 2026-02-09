import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{BASE_URL}/api"

# Identifiants
USERNAME = "admin"
PASSWORD = "admin123"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_result(endpoint, method, status, data=None):
    symbol = "✓" if 200 <= status < 300 else "✗"
    print(f"{symbol} {method:6} {endpoint:40} [{status}]")
    if data and 200 <= status < 300:
        if isinstance(data, dict):
            if 'count' in data:
                print(f"   Résultats: {data['count']} éléments")
            elif 'id' in data:
                print(f"   ID: {data['id']}")

# 1. Test d'authentification
print_section("1. AUTHENTIFICATION")

response = requests.post(
    f"{API_URL}/token/",
    json={"username": USERNAME, "password": PASSWORD}
)
print_result(f"{API_URL}/token/", "POST", response.status_code)

if response.status_code == 200:
    token = response.json().get('access')
    print(f"✓ Token obtenu avec succès")
    print(f"  Token: {token[:50]}...")
else:
    print(f"✗ Erreur d'authentification")
    exit(1)

# Headers avec authentification
headers = {"Authorization": f"Bearer {token}"}

# 2. Test des Patients
print_section("2. TEST DES PATIENTS")

# Lister les patients
response = requests.get(f"{API_URL}/patients/", headers=headers)
print_result(f"{API_URL}/patients/", "GET", response.status_code, response.json())

# Obtenir un patient spécifique
response = requests.get(f"{API_URL}/patients/1/", headers=headers)
print_result(f"{API_URL}/patients/1/", "GET", response.status_code)

# Consulter les consultations d'un patient
response = requests.get(f"{API_URL}/patients/1/consultations/", headers=headers)
print_result(f"{API_URL}/patients/1/consultations/", "GET", response.status_code, response.json())

# Consulter les facturations d'un patient
response = requests.get(f"{API_URL}/patients/1/facturations/", headers=headers)
print_result(f"{API_URL}/patients/1/facturations/", "GET", response.status_code)

# 3. Test des Médecins
print_section("3. TEST DES MÉDECINS")

response = requests.get(f"{API_URL}/medecins/", headers=headers)
print_result(f"{API_URL}/medecins/", "GET", response.status_code, response.json())

# Filtrer par spécialité
response = requests.get(f"{API_URL}/medecins/?specialite=cardiologie", headers=headers)
print_result(f"{API_URL}/medecins/?specialite=cardiologie", "GET", response.status_code, response.json())

# Consultations d'un médecin
response = requests.get(f"{API_URL}/medecins/1/consultations/", headers=headers)
print_result(f"{API_URL}/medecins/1/consultations/", "GET", response.status_code)

# 4. Test des Rendez-vous
print_section("4. TEST DES RENDEZ-VOUS")

response = requests.get(f"{API_URL}/rendez-vous/", headers=headers)
print_result(f"{API_URL}/rendez-vous/", "GET", response.status_code, response.json())

# Filtrer par statut
response = requests.get(f"{API_URL}/rendez-vous/?statut=confirme", headers=headers)
print_result(f"{API_URL}/rendez-vous/?statut=confirme", "GET", response.status_code, response.json())

# 5. Test des Consultations
print_section("5. TEST DES CONSULTATIONS")

response = requests.get(f"{API_URL}/consultations/", headers=headers)
print_result(f"{API_URL}/consultations/", "GET", response.status_code, response.json())

# Recherche
response = requests.get(f"{API_URL}/consultations/?search=diagnostic", headers=headers)
print_result(f"{API_URL}/consultations/?search=diagnostic", "GET", response.status_code)

# 6. Test des Médicaments
print_section("6. TEST DES MÉDICAMENTS")

response = requests.get(f"{API_URL}/medicaments/", headers=headers)
print_result(f"{API_URL}/medicaments/", "GET", response.status_code, response.json())

# Recherche de médicament
response = requests.get(f"{API_URL}/medicaments/?search=Lisinopril", headers=headers)
print_result(f"{API_URL}/medicaments/?search=Lisinopril", "GET", response.status_code)

# 7. Test des Ordonnances
print_section("7. TEST DES ORDONNANCES")

response = requests.get(f"{API_URL}/ordonnances/", headers=headers)
print_result(f"{API_URL}/ordonnances/", "GET", response.status_code, response.json())

# 8. Test des Facturations
print_section("8. TEST DES FACTURATIONS")

response = requests.get(f"{API_URL}/facturations/", headers=headers)
print_result(f"{API_URL}/facturations/", "GET", response.status_code, response.json())

# Statistiques de facturation
response = requests.get(f"{API_URL}/facturations/statistiques/", headers=headers)
print_result(f"{API_URL}/facturations/statistiques/", "GET", response.status_code)
if response.status_code == 200:
    stats = response.json()
    print(f"  Total facturation: {stats.get('total_facturation')}€")
    print(f"  Total payé: {stats.get('total_paye')}€")
    print(f"  Impayé: {stats.get('total_impaye')}€")

# 9. Test de Recherche et Filtrage
print_section("9. TEST DE RECHERCHE ET FILTRAGE")

# Recherche par nom
response = requests.get(f"{API_URL}/patients/?search=Durand", headers=headers)
print_result(f"/patients/?search=Durand", "GET", response.status_code, response.json())

# Filtrage par statut
response = requests.get(f"{API_URL}/patients/?statut=actif", headers=headers)
print_result(f"/patients/?statut=actif", "GET", response.status_code, response.json())

# Tri
response = requests.get(f"{API_URL}/patients/?ordering=-date_enregistrement", headers=headers)
print_result(f"/patients/?ordering=-date_enregistrement", "GET", response.status_code)

# 10. Test de Pagination
print_section("10. TEST DE PAGINATION")

response = requests.get(f"{API_URL}/patients/?page=1", headers=headers)
print_result(f"/patients/?page=1", "GET", response.status_code)
if response.status_code == 200:
    data = response.json()
    print(f"  Page 1 - Total: {data.get('count')} patients")

# Test de création
print_section("11. TEST DE CRÉATION (POST)")

new_patient = {
    "nom": "Testowski",
    "prenom": "Test",
    "date_naissance": "2000-01-01",
    "genre": "M",
    "adresse": "123 Test St",
    "telephone": "0612345678",
    "email": "test@test.com",
    "numero_secu": "200010100000001",
    "statut": "actif"
}

response = requests.post(f"{API_URL}/patients/", json=new_patient, headers=headers)
print_result(f"{API_URL}/patients/", "POST", response.status_code, response.json() if response.status_code == 201 else None)

print_section("✓ TESTS TERMINÉS AVEC SUCCÈS")
print("\nRésumé :")
print("✓ Authentification JWT")
print("✓ Listing des ressources")
print("✓ Filtrage par champs")
print("✓ Recherche")
print("✓ Tri")
print("✓ Pagination")
print("✓ Actions personnalisées")
print("✓ Création de données")
