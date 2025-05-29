from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
from datetime import datetime, timedelta

from database import db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Récupérer les données pour le tableau de bord
    factures = db.get_factures()
    projets = db.get_projets()
    
    # Statistiques des factures
    factures_client = [f for f in factures if f["type"] == "client"]
    factures_fournisseur = [f for f in factures if f["type"] == "fournisseur"]
    
    # Calculer les totaux des factures
    total_factures_client = 0
    total_factures_fournisseur = 0
    
    for facture in factures_client:
        articles = db.get_articles_facture(facture["id"])
        for article in articles:
            montant_ht = article["quantite"] * article["prix_unitaire"]
            montant_tva = montant_ht * (article["tva"] / 100)
            total_factures_client += montant_ht + montant_tva
    
    for facture in factures_fournisseur:
        articles = db.get_articles_facture(facture["id"])
        for article in articles:
            montant_ht = article["quantite"] * article["prix_unitaire"]
            montant_tva = montant_ht * (article["tva"] / 100)
            total_factures_fournisseur += montant_ht + montant_tva
    
    # Statistiques des projets
    projets_non_demarres = [p for p in projets if p["etat"] == "non_demarre"]
    projets_en_cours = [p for p in projets if p["etat"] == "en_cours"]
    projets_termines = [p for p in projets if p["etat"] == "termine"]
    
    # Calculer le coût total des projets
    cout_total_projets = 0
    for projet in projets:
        # Coût des matériaux
        materiaux = db.get_materiaux_projet(projet["id"])
        for materiau in materiaux:
            cout_total_projets += materiau["quantite"] * materiau["cout_unitaire"]
        
        # Coût des charges
        charges = db.get_charges_projet(projet["id"])
        for charge in charges:
            cout_total_projets += charge["montant"]
    
    # Récupérer les activités récentes (factures et projets créés/modifiés récemment)
    activites_recentes = []
    
    # Ajouter les factures récentes
    for facture in factures:
        date_creation = datetime.fromisoformat(facture["date_creation"].replace("Z", "+00:00")) if facture.get("date_creation") else None
        if date_creation and date_creation > datetime.now() - timedelta(days=30):
            activites_recentes.append({
                "type": "facture",
                "action": "création",
                "objet": facture,
                "date": date_creation,
                "url": f"/factures/detail/{facture['id']}"
            })
    
    # Ajouter les projets récents
    for projet in projets:
        date_creation = datetime.fromisoformat(projet["date_creation"].replace("Z", "+00:00")) if projet.get("date_creation") else None
        if date_creation and date_creation > datetime.now() - timedelta(days=30):
            activites_recentes.append({
                "type": "projet",
                "action": "création",
                "objet": projet,
                "date": date_creation,
                "url": f"/projets/detail/{projet['id']}"
            })
    
    # Trier les activités par date (les plus récentes d'abord)
    activites_recentes.sort(key=lambda x: x["date"], reverse=True)
    
    # Limiter à 10 activités
    activites_recentes = activites_recentes[:10]
    
    return templates.TemplateResponse(
        "dashboard/index.html",
        {
            "request": request,
            "nb_factures_client": len(factures_client),
            "nb_factures_fournisseur": len(factures_fournisseur),
            "total_factures_client": total_factures_client,
            "total_factures_fournisseur": total_factures_fournisseur,
            "nb_projets": len(projets),
            "nb_projets_non_demarres": len(projets_non_demarres),
            "nb_projets_en_cours": len(projets_en_cours),
            "nb_projets_termines": len(projets_termines),
            "cout_total_projets": cout_total_projets,
            "activites_recentes": activites_recentes,
            "format_mad": request.app.state.format_mad
        }
    )