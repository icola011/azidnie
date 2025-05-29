# Application de Gestion d'Entreprise

Une application web simple de gestion d'entreprise développée en Python avec FastAPI et Supabase.

## Fonctionnalités

- 💼 **Gestion des factures** : Créer, modifier, supprimer et lister les factures clients et fournisseurs
- 📁 **Gestion de projets** : Suivi des projets avec leur état et progression
- 🔧 **Liste des matériaux et charges** : Suivi des coûts pour chaque projet
- 📊 **Tableau de bord** : Vue globale des activités et statistiques

## Installation

1. Clonez ce dépôt
2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```
3. Configurez votre base de données Supabase :
   - Créez un compte sur [Supabase](https://supabase.com/)
   - Créez un nouveau projet
   - Copiez l'URL et la clé API dans le fichier `.env`

4. Lancez l'application :
   ```
   uvicorn main:app --reload
   ```

5. Accédez à l'application dans votre navigateur à l'adresse : http://localhost:8000

## Structure du projet

```
├── main.py                # Point d'entrée de l'application
├── database.py            # Configuration de la connexion à Supabase
├── models/                # Modèles de données
├── routers/               # Routes API
├── services/              # Logique métier
├── static/                # Fichiers statiques (CSS, JS)
├── templates/             # Templates Jinja2
├── utils/                 # Utilitaires (formatage, PDF, etc.)
└── requirements.txt       # Dépendances
```

## Technologies utilisées

- **Backend** : Python avec FastAPI
- **Base de données** : Supabase (PostgreSQL)
- **Frontend** : HTML/CSS avec Jinja2
- **Exportation PDF** : ReportLab

## Notes

- Toutes les valeurs sont affichées en dirham marocain (MAD)
- Aucune authentification n'est requise pour accéder à l'application