from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from datetime import datetime, date
import json

from database import db
from models.models import Facture, ArticleFacture, TypeFacture
from utils.pdf_generator import generate_facture_pdf

router = APIRouter(prefix="/factures", tags=["factures"])
templates = Jinja2Templates(directory="templates")

# Liste des factures
@router.get("/", response_class=HTMLResponse)
async def liste_factures(request: Request, type: Optional[str] = None):
    factures = db.get_factures(type)
    return templates.TemplateResponse(
        "factures/liste.html",
        {
            "request": request,
            "factures": factures,
            "type_filtre": type,
            "format_mad": request.app.state.format_mad
        }
    )

# Formulaire de création de facture
@router.get("/creer", response_class=HTMLResponse)
async def formulaire_facture(request: Request, type: str = Query(..., regex="^(client|fournisseur)$")):
    return templates.TemplateResponse(
        "factures/formulaire.html",
        {
            "request": request,
            "facture": None,
            "type": type,
            "mode": "creation"
        }
    )

# Création d'une facture
@router.post("/creer")
async def creer_facture(request: Request):
    form_data = await request.form()
    
    # Récupérer les données du formulaire
    facture_data = {
        "numero": form_data.get("numero"),
        "date": form_data.get("date"),
        "type": form_data.get("type"),
        "nom_client_fournisseur": form_data.get("nom_client_fournisseur"),
        "notes": form_data.get("notes"),
        "date_creation": datetime.now().isoformat(),
        "date_modification": datetime.now().isoformat()
    }
    
    # Créer la facture dans la base de données
    facture = db.create_facture(facture_data)
    
    if not facture:
        raise HTTPException(status_code=500, detail="Erreur lors de la création de la facture")
    
    # Récupérer les articles du formulaire
    articles_data = json.loads(form_data.get("articles_json", "[]"))
    
    # Ajouter l'ID de la facture à chaque article
    for article in articles_data:
        article["facture_id"] = facture["id"]
        db.create_article_facture(article)
    
    return RedirectResponse(url=f"/factures/detail/{facture['id']}", status_code=status.HTTP_303_SEE_OTHER)

# Détail d'une facture
@router.get("/detail/{facture_id}", response_class=HTMLResponse)
async def detail_facture(request: Request, facture_id: int):
    facture = db.get_facture(facture_id)
    
    if not facture:
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    
    articles = db.get_articles_facture(facture_id)
    facture["articles"] = articles
    
    # Calculer les totaux
    total_ht = sum(article["quantite"] * article["prix_unitaire"] for article in articles)
    total_tva = sum(article["quantite"] * article["prix_unitaire"] * (article["tva"] / 100) for article in articles)
    total_ttc = total_ht + total_tva
    
    return templates.TemplateResponse(
        "factures/detail.html",
        {
            "request": request,
            "facture": facture,
            "articles": articles,
            "total_ht": total_ht,
            "total_tva": total_tva,
            "total_ttc": total_ttc,
            "format_mad": request.app.state.format_mad
        }
    )

# Formulaire de modification de facture
@router.get("/modifier/{facture_id}", response_class=HTMLResponse)
async def formulaire_modifier_facture(request: Request, facture_id: int):
    facture = db.get_facture(facture_id)
    
    if not facture:
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    
    articles = db.get_articles_facture(facture_id)
    facture["articles"] = articles
    
    return templates.TemplateResponse(
        "factures/formulaire.html",
        {
            "request": request,
            "facture": facture,
            "type": facture["type"],
            "mode": "modification"
        }
    )

# Modification d'une facture
@router.post("/modifier/{facture_id}")
async def modifier_facture(request: Request, facture_id: int):
    form_data = await request.form()
    
    # Récupérer les données du formulaire
    facture_data = {
        "numero": form_data.get("numero"),
        "date": form_data.get("date"),
        "type": form_data.get("type"),
        "nom_client_fournisseur": form_data.get("nom_client_fournisseur"),
        "notes": form_data.get("notes"),
        "date_modification": datetime.now().isoformat()
    }
    
    # Mettre à jour la facture dans la base de données
    success = db.update_facture(facture_id, facture_data)
    
    if not success:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification de la facture")
    
    # Supprimer les anciens articles
    db.delete_articles_facture(facture_id)
    
    # Récupérer les nouveaux articles du formulaire
    articles_data = json.loads(form_data.get("articles_json", "[]"))
    
    # Ajouter l'ID de la facture à chaque article
    for article in articles_data:
        article["facture_id"] = facture_id
        db.create_article_facture(article)
    
    return RedirectResponse(url=f"/factures/detail/{facture_id}", status_code=status.HTTP_303_SEE_OTHER)

# Suppression d'une facture
@router.get("/supprimer/{facture_id}")
async def supprimer_facture(facture_id: int):
    # Supprimer d'abord les articles liés à la facture
    db.delete_articles_facture(facture_id)
    
    # Puis supprimer la facture
    success = db.delete_facture(facture_id)
    
    if not success:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression de la facture")
    
    return RedirectResponse(url="/factures", status_code=status.HTTP_303_SEE_OTHER)

# Génération de PDF
@router.get("/pdf/{facture_id}")
async def generer_pdf_facture(facture_id: int):
    facture = db.get_facture(facture_id)
    
    if not facture:
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    
    articles = db.get_articles_facture(facture_id)
    facture["articles"] = articles
    
    # Calculer les totaux
    total_ht = sum(article["quantite"] * article["prix_unitaire"] for article in articles)
    total_tva = sum(article["quantite"] * article["prix_unitaire"] * (article["tva"] / 100) for article in articles)
    total_ttc = total_ht + total_tva
    
    # Générer le PDF
    pdf_path = generate_facture_pdf(facture, articles, total_ht, total_tva, total_ttc)
    
    # Retourner le fichier PDF
    return FileResponse(
        path=pdf_path,
        filename=f"facture_{facture['numero']}.pdf",
        media_type="application/pdf"
    )