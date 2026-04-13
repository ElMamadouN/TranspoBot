-- TranspoBot - Gestion de Transport Urbain
-- Schema MySQL

DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS tarifs;
DROP TABLE IF EXISTS trajets;
DROP TABLE IF EXISTS lignes;
DROP TABLE IF EXISTS chauffeurs;
DROP TABLE IF EXISTS vehicules;

CREATE TABLE vehicules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    immatriculation VARCHAR(20) UNIQUE NOT NULL,
    marque VARCHAR(50),
    modele VARCHAR(50),
    annee INT,
    kilometrage INT DEFAULT 0,
    statut ENUM('actif', 'maintenance', 'hors_service') DEFAULT 'actif',
    date_derniere_maintenance DATE
);

CREATE TABLE chauffeurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(20),
    licence VARCHAR(20),
    date_embauche DATE,
    statut ENUM('actif', 'conge', 'inactif') DEFAULT 'actif'
);

CREATE TABLE lignes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) UNIQUE NOT NULL,
    nom VARCHAR(100),
    debut_terminal VARCHAR(100),
    fin_terminal VARCHAR(100),
    distance_km DECIMAL(10,2)
);

CREATE TABLE tarifs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ligne_id INT,
    type_tarif VARCHAR(50),
    montant DECIMAL(10,2),
    FOREIGN KEY (ligne_id) REFERENCES lignes(id)
);

CREATE TABLE trajets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicule_id INT,
    chauffeur_id INT,
    ligne_id INT,
    date_heure_depart DATETIME,
    date_heure_arrivee DATETIME,
    nb_passagers INT DEFAULT 0,
    statut ENUM('planifie', 'en_cours', 'termine', 'annule') DEFAULT 'planifie',
    FOREIGN KEY (vehicule_id) REFERENCES vehicules(id),
    FOREIGN KEY (chauffeur_id) REFERENCES chauffeurs(id),
    FOREIGN KEY (ligne_id) REFERENCES lignes(id)
);

CREATE TABLE incidents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trajet_id INT,
    description TEXT,
    date_incident DATETIME,
    gravite ENUM('legel', 'moyen', 'grave'),
    FOREIGN KEY (trajet_id) REFERENCES trajets(id)
);

-- Donnees de test
INSERT INTO vehicules (immatriculation, marque, modele, annee, kilometrage, statut) VALUES
('DK-9012-EF', 'Mercedes', 'Citaro', 2020, 78000, 'maintenance'),
('DK-1234-AB', 'Volvo', '7900', 2019, 120000, 'actif'),
('DK-5678-CD', 'Iveco', 'Urbanway', 2021, 45000, 'actif'),
('DK-9012-GH', 'Mercedes', 'Citaro', 2018, 180000, 'hors_service'),
('DK-3456-IJ', 'Scania', 'N230', 2022, 25000, 'actif');

INSERT INTO chauffeurs (nom, prenom, telephone, licence, date_embauche, statut) VALUES
('FALL', 'Ibrahima', '771234567', 'B', '2019-03-15', 'actif'),
('DIOP', 'Moussa', '772345678', 'D', '2020-06-01', 'actif'),
('SOW', 'Fatou', '773456789', 'B', '2018-01-10', 'actif'),
('NDIAYE', 'Ousmane', '774567890', 'D', '2021-09-05', 'conge'),
('SYLLA', 'Mamadou', '775678901', 'B', '2022-02-20', 'actif');

INSERT INTO lignes (numero, nom, debut_terminal, fin_terminal, distance_km) VALUES
('L1', 'Gare Routiere - Point E', 'Gare Routiere', 'Point E', 15.5),
('L2', 'Pikine - Almadies', 'Pikine', 'Almadies', 22.0),
('L3', 'Dakar Plateau - AIBD', 'Dakar Plateau', 'AIBD', 35.0),
('L4', 'Guediawaye - Place de la Nation', 'Guediawaye', 'Place de la Nation', 18.5),
('L5', 'Rufisque - Parcelles Assainies', 'Rufisque', 'Parcelles Assainies', 25.0);

INSERT INTO tarifs (ligne_id, type_tarif, montant) VALUES
(1, 'standard', 25.00),
(1, 'reduit', 15.00),
(2, 'standard', 30.00),
(2, 'reduit', 20.00),
(3, 'standard', 50.00),
(3, 'reduit', 30.00);

INSERT INTO trajets (vehicule_id, chauffeur_id, ligne_id, date_heure_depart, date_heure_arrivee, nb_passagers, statut) VALUES
(1, 1, 1, '2026-04-07 08:00:00', '2026-04-07 08:45:00', 45, 'termine'),
(2, 2, 2, '2026-04-07 09:00:00', '2026-04-07 09:50:00', 38, 'termine'),
(3, 3, 1, '2026-04-07 10:00:00', '2026-04-07 10:45:00', 52, 'termine'),
(1, 1, 3, '2026-04-08 08:00:00', '2026-04-08 09:00:00', 28, 'termine'),
(2, 2, 2, '2026-04-08 09:00:00', '2026-04-08 09:50:00', 41, 'termine'),
(3, 3, 4, '2026-04-08 10:00:00', '2026-04-08 10:40:00', 35, 'termine'),
(5, 5, 5, '2026-04-09 08:00:00', '2026-04-09 09:00:00', 22, 'termine'),
(2, 2, 1, '2026-04-09 09:00:00', '2026-04-09 09:45:00', 48, 'termine'),
(3, 3, 3, '2026-04-10 08:00:00', '2026-04-10 09:00:00', 30, 'termine'),
(1, 1, 2, '2026-04-10 09:00:00', '2026-04-10 09:50:00', 44, 'termine'),
(5, 5, 4, '2026-04-11 08:00:00', '2026-04-11 08:40:00', 25, 'termine'),
(2, 2, 5, '2026-04-12 08:00:00', '2026-04-12 09:00:00', 18, 'termine');

INSERT INTO incidents (trajet_id, description, date_incident, gravite) VALUES
(1, 'Retard de 10 min cause embouteillage', '2026-04-07 08:30:00', 'legel'),
(2, 'Panne technique siege defaillant', '2026-04-07 09:30:00', 'moyen'),
(4, 'Accident legersection, aucun bless', '2026-04-08 08:15:00', 'grave'),
(7, 'Retard de 5 min', '2026-04-09 08:10:00', 'legel'),
(9, 'Client difficultpayment', '2026-04-10 08:30:00', 'legel');