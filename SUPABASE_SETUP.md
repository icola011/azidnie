# Configuration de Supabase pour l'application de gestion d'entreprise

Ce guide vous explique comment configurer Supabase pour l'application de gestion d'entreprise.

## Étape 1 : Créer un compte Supabase

1. Rendez-vous sur [https://supabase.com/](https://supabase.com/)
2. Cliquez sur "Start your project" ou "Sign up"
3. Créez un compte en utilisant GitHub, GitLab, ou une adresse e-mail

## Étape 2 : Créer un nouveau projet

1. Une fois connecté, cliquez sur "New Project"
2. Donnez un nom à votre projet (par exemple, "gestion-entreprise")
3. Définissez un mot de passe pour la base de données
4. Choisissez la région la plus proche de vous
5. Cliquez sur "Create new project"

## Étape 3 : Récupérer les informations de connexion

1. Dans le tableau de bord de votre projet, allez dans "Settings" > "API"
2. Notez les informations suivantes :
   - **URL** : `https://[votre-id-projet].supabase.co`
   - **anon/public key** : Clé d'API publique

## Étape 4 : Configurer le fichier .env

1. Ouvrez le fichier `.env` à la racine du projet
2. Remplacez les valeurs par défaut par vos informations de connexion :

```
SUPABASE_URL=https://[votre-id-projet].supabase.co
SUPABASE_KEY=votre-cle-api-publique
```

## Étape 5 : Initialiser la base de données

1. Dans le tableau de bord Supabase, allez dans "SQL Editor"
2. Cliquez sur "New Query"
3. Copiez le contenu du fichier `init_database.sql` fourni dans ce projet
4. Cliquez sur "Run" pour exécuter le script SQL

Ce script va créer toutes les tables nécessaires et ajouter quelques données d'exemple.

## Étape 6 : Vérifier la configuration

1. Dans le tableau de bord Supabase, allez dans "Table Editor"
2. Vous devriez voir les tables suivantes :
   - `factures`
   - `articles_facture`
   - `projets`
   - `taches`
   - `materiaux`
   - `charges`

## Étape 7 : Configurer les politiques de sécurité (RLS)

Les politiques de sécurité sont déjà configurées dans le script d'initialisation pour permettre un accès public à toutes les tables, puisque l'application n'utilise pas d'authentification.

Si vous souhaitez modifier ces politiques :

1. Dans le tableau de bord Supabase, allez dans "Authentication" > "Policies"
2. Vous pouvez modifier les politiques existantes ou en créer de nouvelles

## Étape 8 : Lancer l'application

Une fois Supabase configuré, vous pouvez lancer l'application :

```
uvicorn main:app --reload
```

L'application devrait maintenant être connectée à votre base de données Supabase et fonctionner correctement.

## Remarques importantes

- Cette configuration est destinée à un environnement de développement ou de démonstration
- Pour un environnement de production, vous devriez mettre en place des mesures de sécurité supplémentaires
- Les clés API sont sensibles, ne les partagez pas et ne les exposez pas dans votre code source public