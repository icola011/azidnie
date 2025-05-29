from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from datetime import datetime, date
import json

from database import db
from models.models import Projet, Tache, Materiau, Charge, EtatProjet

router = APIRouter(prefix="/projets", tags=["projets"])
templates = Jinja2Templates(directory="templates")

# Liste des projets
@router.get("/", response_class=HTMLResponse)
async def liste_projets(request: Request, etat: Optional[str] = None):
    projets = db.get_projets()
    
    # Filtrer par état si spécifié
    if etat:
        projets = [p for p in projets if p["etat"] == etat]
    
    # Pour chaque projet, calculer la progression basée sur les tâches
    for projet in projets:
        taches = db.get_taches_projet(projet["id"])
        if taches:
            projet["progression"] = int((sum(1 for t in taches if t["terminee"]) / len(taches)) * 100)
        else:
            projet["progression"] = projet.get("progression", 0)
    
    return templates.TemplateResponse(
        "projets/liste.html",
        {
            "request": request,
            "projets": projets,
            "etat_filtre": etat
        }
    )

# Formulaire de création de projet
@router.get("/creer", response_class=HTMLResponse)
async def formulaire_projet(request: Request):
    return templates.TemplateResponse(
        "projets/formulaire.html",
        {
            "request": request,
            "projet": None,
            "mode": "creation",
            "etats": ["non_demarre", "en_cours", "termine"]
        }
    )

# Création d'un projet
@router.post("/creer")
async def creer_projet(request: Request):
    form_data = await request.form()
    
    # Récupérer les données du formulaire
    projet_data = {
        "nom": form_data.get("nom"),
        "description": form_data.get("description"),
        "date_debut": form_data.get("date_debut"),
        "date_fin": form_data.get("date_fin") or None,
        "etat": form_data.get("etat"),
        "progression": int(form_data.get("progression", 0)),
        "date_creation": datetime.now().isoformat(),
        "date_modification": datetime.now().isoformat()
    }
    
    # Créer le projet dans la base de données
    projet = db.create_projet(projet_data)
    
    if not projet:
        raise HTTPException(status_code=500, detail="Erreur lors de la création du projet")
    
    # Récupérer les tâches du formulaire
    taches_data = json.loads(form_data.get("taches_json", "[]"))
    
    # Ajouter l'ID du projet à chaque tâche
    for tache in taches_data:
        tache["projet_id"] = projet["id"]
        db.create_tache(tache)
    
    return RedirectResponse(url=f"/projets/detail/{projet['id']}", status_code=status.HTTP_303_SEE_OTHER)

# Détail d'un projet
@router.get("/detail/{projet_id}", response_class=HTMLResponse)
async def detail_projet(request: Request, projet_id: int):
    projet = db.get_projet(projet_id)
    
    if not projet:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    taches = db.get_taches_projet(projet_id)
    materiaux = db.get_materiaux_projet(projet_id)
    charges = db.get_charges_projet(projet_id)
    
    # Calculer la progression basée sur les tâches
    if taches:
        progression = int((sum(1 for t in taches if t["terminee"]) / len(taches)) * 100)
    else:
        progression = projet.get("progression", 0)
    
    # Calculer les coûts
    cout_materiaux = sum(m["quantite"] * m["cout_unitaire"] for m in materiaux)
    cout_charges = sum(c["montant"] for c in charges)
    cout_total = cout_materiaux + cout_charges
    
    return templates.TemplateResponse(
        "projets/detail.html",
        {
            "request": request,
            "projet": projet,
            "taches": taches,
            "materiaux": materiaux,
            "charges": charges,
            "progression": progression,
            "cout_materiaux": cout_materiaux,
            "cout_charges": cout_charges,
            "cout_total": cout_total,
            "format_mad": request.app.state.format_mad
        }
    )

# Formulaire de modification de projet
@router.get("/modifier/{projet_id}", response_class=HTMLResponse)
async def formulaire_modifier_projet(request: Request, projet_id: int):
    projet = db.get_projet(projet_id)
    
    if not projet:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    taches = db.get_taches_projet(projet_id)
    
    return templates.TemplateResponse(
        "projets/formulaire.html",
        {
            "request": request,
            "projet": projet,
            "taches": taches,
            "mode": "modification",
            "etats": ["non_demarre", "en_cours", "termine"]
        }
    )

# Modification d'un projet
@router.post("/modifier/{projet_id}")
async def modifier_projet(request: Request, projet_id: int):
    form_data = await request.form()
    
    # Récupérer les données du formulaire
    projet_data = {
        "nom": form_data.get("nom"),
        "description": form_data.get("description"),
        "date_debut": form_data.get("date_debut"),
        "date_fin": form_data.get("date_fin") or None,
        "etat": form_data.get("etat"),
        "progression": int(form_data.get("progression", 0)),
        "date_modification": datetime.now().isoformat()
    }
    
    # Mettre à jour le projet dans la base de données
    success = db.update_projet(projet_id, projet_data)
    
    if not success:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification du projet")
    
    # Gérer les tâches
    taches_data = json.loads(form_data.get("taches_json", "[]"))
    
    # Supprimer toutes les tâches existantes
    taches_existantes = db.get_taches_projet(projet_id)
    for tache in taches_existantes:
        db.delete_tache(tache["id"])
    
    # Ajouter les nouvelles tâches
    for tache in taches_data:
        tache["projet_id"] = projet_id
        db.create_tache(tache)
    
    return RedirectResponse(url=f"/projets/detail/{projet_id}", status_code=status.HTTP_303_SEE_OTHER)

# Suppression d'un projet
@router.get("/supprimer/{projet_id}")
async def supprimer_projet(projet_id: int):
    # Supprimer d'abord les éléments liés au projet
    taches = db.get_taches_projet(projet_id)
    for tache in taches:
        db.delete_tache(tache["id"])
    
    materiaux = db.get_materiaux_projet(projet_id)
    for materiau in materiaux:
        db.delete_materiau(materiau["id"])
    
    charges = db.get_charges_projet(projet_id)
    for charge in charges:
        db.delete_charge(charge["id"])
    
    # Puis supprimer le projet
    success = db.delete_projet(projet_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du projet")
    
    return RedirectResponse(url="/projets", status_code=status.HTTP_303_SEE_OTHER)

# Gestion des matériaux
@router.post("/materiaux/ajouter/{projet_id}")
async def ajouter_materiau(request: Request, projet_id: int):
    form_data = await request.form()
    
    materiau_data = {
        "projet_id": projet_id,
        "nom": form_data.get("nom"),
        "quantite": float(form_data.get("quantite")),
        "cout_unitaire": float(form_data.get("cout_unitaire"))
    }
    
    db.create_materiau(materiau_data)
    
    return RedirectResponse(url=f"/projets/detail/{projet_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/materiaux/supprimer/{materiau_id}")
async def supprimer_materiau(materiau_id: int, projet_id: int):
    db.delete_materiau(materiau_id)
    return RedirectResponse(url=f"/projets/detail/{projet_id}", status_code=status.HTTP_303_SEE_OTHER)

# Gestion des charges
@router.post("/charges/ajouter/{projet_id}")
async def ajouter_charge(request: Request, projet_id: int):
    form_data = await request.form()
    
    charge_data = {
        "projet_id": projet_id,
        "description": form_data.get("description"),
        "montant": float(form_data.get("montant")),
        "type": form_data.get("type")
    }
    
    db.create_charge(charge_data)
    
    return RedirectResponse(url=f"/projets/detail/{projet_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/charges/supprimer/{charge_id}")
async def supprimer_charge(charge_id: int, projet_id: int):
    db.delete_charge(charge_id)
    return RedirectResponse(url=f"/projets/detail/{projet_id}", status_code=status.HTTP_303_SEE_OTHER)

# Gestion des tâches
@router.post("/taches/toggle/{tache_id}")
async def toggle_tache(tache_id: int, projet_id: int):
    tache = db.get_tache(tache_id)
    if tache:
        db.update_tache(tache_id, {"terminee": not tache["terminee"]})
    
    return RedirectResponse(url=f"/projets/detail/{projet_id}", status_code=status.HTTP_303_SEE_OTHER)