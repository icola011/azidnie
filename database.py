import os
import json
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class SupabaseClient:
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Content-Type": "application/json"
        }
    
    def _build_url(self, table, path=""):
        return f"{self.url}/rest/v1/{table}{path}"
    
    # Méthodes pour les factures
    def get_factures(self, type_facture=None):
        url = self._build_url("factures")
        params = {}
        if type_facture:
            params["type"] = f"eq.{type_facture}"
        response = requests.get(url, headers=self.headers, params=params)
        return response.json() if response.status_code == 200 else []
    
    def get_facture(self, facture_id):
        url = self._build_url("factures", f"?id=eq.{facture_id}")
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data[0] if data else None
    
    def create_facture(self, facture_data):
        url = self._build_url("factures")
        response = requests.post(url, headers=self.headers, json=facture_data)
        return response.json() if response.status_code == 201 else None
    
    def update_facture(self, facture_id, facture_data):
        url = self._build_url("factures", f"?id=eq.{facture_id}")
        response = requests.patch(url, headers=self.headers, json=facture_data)
        return response.status_code == 204
    
    def delete_facture(self, facture_id):
        url = self._build_url("factures", f"?id=eq.{facture_id}")
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204
    
    # Méthodes pour les articles de facture
    def get_articles_facture(self, facture_id):
        url = self._build_url("articles_facture", f"?facture_id=eq.{facture_id}")
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def create_article_facture(self, article_data):
        url = self._build_url("articles_facture")
        response = requests.post(url, headers=self.headers, json=article_data)
        return response.json() if response.status_code == 201 else None
    
    def delete_articles_facture(self, facture_id):
        url = self._build_url("articles_facture", f"?facture_id=eq.{facture_id}")
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204
    
    # Méthodes pour les projets
    def get_projets(self):
        url = self._build_url("projets")
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def get_projet(self, projet_id):
        url = self._build_url("projets", f"?id=eq.{projet_id}")
        response = requests.get(url, headers=self.headers)
        data = response.json()
        return data[0] if data else None
    
    def create_projet(self, projet_data):
        url = self._build_url("projets")
        response = requests.post(url, headers=self.headers, json=projet_data)
        return response.json() if response.status_code == 201 else None
    
    def update_projet(self, projet_id, projet_data):
        url = self._build_url("projets", f"?id=eq.{projet_id}")
        response = requests.patch(url, headers=self.headers, json=projet_data)
        return response.status_code == 204
    
    def delete_projet(self, projet_id):
        url = self._build_url("projets", f"?id=eq.{projet_id}")
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204
    
    # Méthodes pour les matériaux
    def get_materiaux_projet(self, projet_id):
        url = self._build_url("materiaux", f"?projet_id=eq.{projet_id}")
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def create_materiau(self, materiau_data):
        url = self._build_url("materiaux")
        response = requests.post(url, headers=self.headers, json=materiau_data)
        return response.json() if response.status_code == 201 else None
    
    def update_materiau(self, materiau_id, materiau_data):
        url = self._build_url("materiaux", f"?id=eq.{materiau_id}")
        response = requests.patch(url, headers=self.headers, json=materiau_data)
        return response.status_code == 204
    
    def delete_materiau(self, materiau_id):
        url = self._build_url("materiaux", f"?id=eq.{materiau_id}")
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204
    
    # Méthodes pour les charges
    def get_charges_projet(self, projet_id):
        url = self._build_url("charges", f"?projet_id=eq.{projet_id}")
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def create_charge(self, charge_data):
        url = self._build_url("charges")
        response = requests.post(url, headers=self.headers, json=charge_data)
        return response.json() if response.status_code == 201 else None
    
    def update_charge(self, charge_id, charge_data):
        url = self._build_url("charges", f"?id=eq.{charge_id}")
        response = requests.patch(url, headers=self.headers, json=charge_data)
        return response.status_code == 204
    
    def delete_charge(self, charge_id):
        url = self._build_url("charges", f"?id=eq.{charge_id}")
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204
    
    # Méthodes pour les tâches de projet
    def get_taches_projet(self, projet_id):
        url = self._build_url("taches", f"?projet_id=eq.{projet_id}")
        response = requests.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def create_tache(self, tache_data):
        url = self._build_url("taches")
        response = requests.post(url, headers=self.headers, json=tache_data)
        return response.json() if response.status_code == 201 else None
    
    def update_tache(self, tache_id, tache_data):
        url = self._build_url("taches", f"?id=eq.{tache_id}")
        response = requests.patch(url, headers=self.headers, json=tache_data)
        return response.status_code == 204
    
    def delete_tache(self, tache_id):
        url = self._build_url("taches", f"?id=eq.{tache_id}")
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204

# Créer une instance du client Supabase
db = SupabaseClient()