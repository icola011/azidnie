from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import uuid

# Importer les routers
from routers import factures, projets, dashboard

# Charger les variables d'environnement
load_dotenv()

# Créer l'application FastAPI
app = FastAPI(title="Gestion d'Entreprise", description="Application de gestion d'entreprise")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monter les fichiers statiques
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les templates
templates = Jinja2Templates(directory="templates")

# Inclure les routers
app.include_router(factures.router)
app.include_router(projets.router)
app.include_router(dashboard.router)

# Fonction pour formater les montants en MAD
def format_mad(amount):
    if amount is None:
        return "0,00 MAD"
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",") + " MAD"

# Ajouter la fonction de formatage aux templates Jinja2
app.state.format_mad = format_mad

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Point d'entrée pour exécuter l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)