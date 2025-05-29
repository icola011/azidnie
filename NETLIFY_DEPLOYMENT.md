# Déploiement sur Netlify

## Configuration actuelle

Cette application est configurée pour un déploiement statique sur Netlify avec une fonction serverless pour gérer les requêtes API. Cependant, il est important de noter que **Netlify ne prend pas en charge l'exécution de serveurs Python comme FastAPI en production**.

## Fichiers de configuration

Plusieurs fichiers de configuration sont fournis pour Netlify :

- `netlify.toml` - Configuration principale au format TOML
- `netlify.yaml` - Configuration alternative au format YAML
- `netlify.json` - Configuration alternative au format JSON

## Structure du déploiement

### Partie statique

Le répertoire `static/` est publié comme site statique et contient :

- Une page d'accueil statique (`index.html`)
- Les fichiers CSS et JavaScript
- Le favicon

### Fonction serverless

Le répertoire `functions/` contient :

- `api.js` - Une fonction serverless qui affiche une page d'information sur l'application

## Redirections

Les redirections suivantes sont configurées :

1. `/api/*` → `/.netlify/functions/api` - Redirige les requêtes API vers la fonction serverless
2. `/*` → `/index.html` - Redirige toutes les autres requêtes vers la page d'accueil (pour le routage côté client)

## En-têtes de sécurité

Les en-têtes de sécurité suivants sont configurés :

- `X-Frame-Options: DENY` - Empêche le site d'être affiché dans un iframe
- `X-XSS-Protection: 1; mode=block` - Active la protection XSS du navigateur
- `Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:` - Définit une politique de sécurité du contenu
- `X-Content-Type-Options: nosniff` - Empêche le navigateur de deviner le type MIME

## Limitations

### Pas de backend Python

Netlify ne prend pas en charge l'exécution de serveurs Python comme FastAPI en production. Le déploiement actuel est une version statique de l'application avec une fonction serverless pour afficher une page d'information.

### Pas de base de données

La connexion à Supabase fonctionne normalement depuis le navigateur, mais les opérations qui nécessitent le backend Python ne fonctionneront pas.

## Alternatives pour un déploiement complet

Pour déployer l'application complète avec le backend Python, envisagez :

1. **Render** - Prend en charge les applications Python
2. **Heroku** - Prend en charge les applications Python
3. **Railway** - Plateforme moderne pour les applications Python
4. **DigitalOcean App Platform** - Prend en charge les applications Python
5. **AWS Elastic Beanstalk** - Pour un déploiement plus robuste

## Exécution locale

Pour exécuter l'application complète localement :

1. Installez les dépendances : `pip install -r requirements.txt`
2. Configurez Supabase selon les instructions dans `SUPABASE_SETUP.md`
3. Lancez l'application : `uvicorn main:app --reload`
4. Accédez à l'application via `http://localhost:8000`