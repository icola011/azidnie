-- Script d'initialisation de la base de données pour l'application de gestion d'entreprise
-- À exécuter dans l'éditeur SQL de Supabase

-- Table des factures
CREATE TABLE factures (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('client', 'fournisseur')),
    nom_client_fournisseur VARCHAR(255) NOT NULL,
    notes TEXT,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des articles de facture
CREATE TABLE articles_facture (
    id SERIAL PRIMARY KEY,
    facture_id INTEGER NOT NULL REFERENCES factures(id) ON DELETE CASCADE,
    nom VARCHAR(255) NOT NULL,
    quantite DECIMAL(10, 2) NOT NULL,
    prix_unitaire DECIMAL(10, 2) NOT NULL,
    tva DECIMAL(5, 2) NOT NULL DEFAULT 20.0
);

-- Table des projets
CREATE TABLE projets (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    date_debut DATE NOT NULL,
    date_fin DATE,
    etat VARCHAR(20) NOT NULL CHECK (etat IN ('non_demarre', 'en_cours', 'termine')),
    progression INTEGER NOT NULL DEFAULT 0 CHECK (progression >= 0 AND progression <= 100),
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table des tâches de projet
CREATE TABLE taches (
    id SERIAL PRIMARY KEY,
    projet_id INTEGER NOT NULL REFERENCES projets(id) ON DELETE CASCADE,
    description VARCHAR(255) NOT NULL,
    terminee BOOLEAN NOT NULL DEFAULT FALSE
);

-- Table des matériaux de projet
CREATE TABLE materiaux (
    id SERIAL PRIMARY KEY,
    projet_id INTEGER NOT NULL REFERENCES projets(id) ON DELETE CASCADE,
    nom VARCHAR(255) NOT NULL,
    quantite DECIMAL(10, 2) NOT NULL,
    cout_unitaire DECIMAL(10, 2) NOT NULL
);

-- Table des charges de projet
CREATE TABLE charges (
    id SERIAL PRIMARY KEY,
    projet_id INTEGER NOT NULL REFERENCES projets(id) ON DELETE CASCADE,
    description VARCHAR(255) NOT NULL,
    montant DECIMAL(10, 2) NOT NULL,
    type VARCHAR(50) NOT NULL
);

-- Créer des politiques RLS (Row Level Security) pour permettre l'accès public
-- Cela est nécessaire car nous n'utilisons pas d'authentification

-- Politique pour les factures
ALTER TABLE factures ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Accès public aux factures" ON factures FOR ALL USING (true);

-- Politique pour les articles de facture
ALTER TABLE articles_facture ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Accès public aux articles de facture" ON articles_facture FOR ALL USING (true);

-- Politique pour les projets
ALTER TABLE projets ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Accès public aux projets" ON projets FOR ALL USING (true);

-- Politique pour les tâches
ALTER TABLE taches ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Accès public aux tâches" ON taches FOR ALL USING (true);

-- Politique pour les matériaux
ALTER TABLE materiaux ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Accès public aux matériaux" ON materiaux FOR ALL USING (true);

-- Politique pour les charges
ALTER TABLE charges ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Accès public aux charges" ON charges FOR ALL USING (true);

-- Créer des déclencheurs pour mettre à jour automatiquement la date de modification

-- Fonction pour mettre à jour la date de modification
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_modification = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Déclencheur pour les factures
CREATE TRIGGER update_factures_modtime
BEFORE UPDATE ON factures
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Déclencheur pour les projets
CREATE TRIGGER update_projets_modtime
BEFORE UPDATE ON projets
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

-- Insérer quelques données d'exemple

-- Factures clients
INSERT INTO factures (numero, date, type, nom_client_fournisseur, notes)
VALUES 
('FC-2023-001', '2023-01-15', 'client', 'Société ABC', 'Première facture client'),
('FC-2023-002', '2023-02-20', 'client', 'Entreprise XYZ', 'Deuxième facture client');

-- Articles des factures clients
INSERT INTO articles_facture (facture_id, nom, quantite, prix_unitaire, tva)
VALUES 
(1, 'Consultation', 10, 500, 20),
(1, 'Développement', 5, 800, 20),
(2, 'Maintenance', 20, 300, 20),
(2, 'Formation', 2, 1500, 20);

-- Factures fournisseurs
INSERT INTO factures (numero, date, type, nom_client_fournisseur, notes)
VALUES 
('FF-2023-001', '2023-01-10', 'fournisseur', 'Fournisseur Matériel', 'Achat de matériel'),
('FF-2023-002', '2023-02-05', 'fournisseur', 'Fournisseur Services', 'Services externes');

-- Articles des factures fournisseurs
INSERT INTO articles_facture (facture_id, nom, quantite, prix_unitaire, tva)
VALUES 
(3, 'Ordinateurs', 3, 5000, 20),
(3, 'Imprimantes', 2, 1200, 20),
(4, 'Hébergement', 12, 100, 20),
(4, 'Maintenance serveurs', 1, 2000, 20);

-- Projets
INSERT INTO projets (nom, description, date_debut, date_fin, etat, progression)
VALUES 
('Refonte site web', 'Refonte complète du site web de l\'entreprise', '2023-01-01', '2023-03-31', 'termine', 100),
('Développement application mobile', 'Création d\'une application mobile pour les clients', '2023-02-15', '2023-06-30', 'en_cours', 60),
('Mise à jour infrastructure', 'Mise à jour des serveurs et de l\'infrastructure réseau', '2023-04-01', NULL, 'non_demarre', 0);

-- Tâches des projets
INSERT INTO taches (projet_id, description, terminee)
VALUES 
(1, 'Maquettes graphiques', TRUE),
(1, 'Intégration HTML/CSS', TRUE),
(1, 'Développement backend', TRUE),
(1, 'Tests et déploiement', TRUE),
(2, 'Conception UX/UI', TRUE),
(2, 'Développement frontend', TRUE),
(2, 'Développement backend', FALSE),
(2, 'Tests et publication', FALSE),
(3, 'Audit de l\'infrastructure actuelle', FALSE),
(3, 'Achat de matériel', FALSE),
(3, 'Installation et configuration', FALSE);

-- Matériaux des projets
INSERT INTO materiaux (projet_id, nom, quantite, cout_unitaire)
VALUES 
(1, 'Licence template', 1, 1500),
(1, 'Plugins premium', 3, 500),
(2, 'Licence SDK', 1, 3000),
(2, 'Services API', 5, 200),
(3, 'Serveurs', 2, 15000),
(3, 'Switches réseau', 4, 2500);

-- Charges des projets
INSERT INTO charges (projet_id, description, montant, type)
VALUES 
(1, 'Hébergement annuel', 1200, 'services externes'),
(1, 'Consultant SEO', 5000, 'services externes'),
(2, 'Publication App Store', 99, 'services externes'),
(2, 'Publication Play Store', 25, 'services externes'),
(3, 'Transport matériel', 1500, 'transport'),
(3, 'Installation par prestataire', 8000, 'main-d\'œuvre');