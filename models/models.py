from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

# Énumération pour les types de factures
class TypeFacture(str, Enum):
    CLIENT = "client"
    FOURNISSEUR = "fournisseur"

# Énumération pour les états de projet
class EtatProjet(str, Enum):
    NON_DEMARRE = "non_demarre"
    EN_COURS = "en_cours"
    TERMINE = "termine"

# Modèle pour les articles de facture
class ArticleFacture(BaseModel):
    id: Optional[int] = None
    facture_id: Optional[int] = None
    nom: str
    quantite: float
    prix_unitaire: float
    tva: float = 20.0  # TVA par défaut à 20%
    
    @property
    def montant_ht(self) -> float:
        return self.quantite * self.prix_unitaire
    
    @property
    def montant_tva(self) -> float:
        return self.montant_ht * (self.tva / 100)
    
    @property
    def montant_ttc(self) -> float:
        return self.montant_ht + self.montant_tva

# Modèle pour les factures
class Facture(BaseModel):
    id: Optional[int] = None
    numero: str
    date: date
    type: TypeFacture
    nom_client_fournisseur: str
    articles: List[ArticleFacture] = []
    notes: Optional[str] = None
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    
    @property
    def total_ht(self) -> float:
        return sum(article.montant_ht for article in self.articles)
    
    @property
    def total_tva(self) -> float:
        return sum(article.montant_tva for article in self.articles)
    
    @property
    def total_ttc(self) -> float:
        return sum(article.montant_ttc for article in self.articles)

# Modèle pour les tâches de projet
class Tache(BaseModel):
    id: Optional[int] = None
    projet_id: Optional[int] = None
    description: str
    terminee: bool = False

# Modèle pour les matériaux de projet
class Materiau(BaseModel):
    id: Optional[int] = None
    projet_id: Optional[int] = None
    nom: str
    quantite: float
    cout_unitaire: float
    
    @property
    def cout_total(self) -> float:
        return self.quantite * self.cout_unitaire

# Modèle pour les charges de projet
class Charge(BaseModel):
    id: Optional[int] = None
    projet_id: Optional[int] = None
    description: str
    montant: float
    type: str  # transport, services externes, main-d'œuvre, etc.

# Modèle pour les projets
class Projet(BaseModel):
    id: Optional[int] = None
    nom: str
    description: Optional[str] = None
    date_debut: date
    date_fin: Optional[date] = None
    etat: EtatProjet = EtatProjet.NON_DEMARRE
    progression: Optional[int] = 0  # Pourcentage de progression
    taches: List[Tache] = []
    materiaux: List[Materiau] = []
    charges: List[Charge] = []
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    
    @property
    def cout_total_materiaux(self) -> float:
        return sum(materiau.cout_total for materiau in self.materiaux)
    
    @property
    def cout_total_charges(self) -> float:
        return sum(charge.montant for charge in self.charges)
    
    @property
    def cout_total(self) -> float:
        return self.cout_total_materiaux + self.cout_total_charges
    
    @property
    def progression_taches(self) -> int:
        if not self.taches:
            return 0
        return int((sum(1 for tache in self.taches if tache.terminee) / len(self.taches)) * 100)