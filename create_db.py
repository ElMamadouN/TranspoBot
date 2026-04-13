import sqlite3

conn = sqlite3.connect('C:/TranspoBot/transport.db')
c = conn.cursor()

c.execute('''CREATE TABLE vehicules (
    id INTEGER PRIMARY KEY,
    immatriculation TEXT UNIQUE,
    marque TEXT,
    modele TEXT,
    annee INTEGER,
    kilometrage INTEGER DEFAULT 0,
    statut TEXT DEFAULT 'actif',
    date_derniere_maintenance TEXT
)''')

c.execute('''CREATE TABLE chauffeurs (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    prenom TEXT,
    telephone TEXT,
    licence TEXT,
    date_embauche TEXT,
    statut TEXT DEFAULT 'actif'
)''')

c.execute('''CREATE TABLE lignes (
    id INTEGER PRIMARY KEY,
    numero TEXT UNIQUE,
    nom TEXT,
    debut_terminal TEXT,
    fin_terminal TEXT,
    distance_km REAL
)''')

c.execute('''CREATE TABLE tarifs (
    id INTEGER PRIMARY KEY,
    ligne_id INTEGER,
    type_tarif TEXT,
    montant REAL
)''')

c.execute('''CREATE TABLE trajets (
    id INTEGER PRIMARY KEY,
    vehicule_id INTEGER,
    chauffeur_id INTEGER,
    ligne_id INTEGER,
    date_heure_depart TEXT,
    date_heure_arrivee TEXT,
    nb_passagers INTEGER DEFAULT 0,
    statut TEXT DEFAULT 'planifie'
)''')

c.execute('''CREATE TABLE incidents (
    id INTEGER PRIMARY KEY,
    trajet_id INTEGER,
    description TEXT,
    date_incident TEXT,
    gravite TEXT
)''')

c.execute('INSERT INTO vehicules VALUES(1,"DK-9012-EF","Mercedes","Citaro",2020,78000,"maintenance",NULL)')
c.execute('INSERT INTO vehicules VALUES(2,"DK-1234-AB","Volvo","7900",2019,120000,"actif",NULL)')
c.execute('INSERT INTO vehicules VALUES(3,"DK-5678-CD","Iveco","Urbanway",2021,45000,"actif",NULL)')
c.execute('INSERT INTO vehicules VALUES(4,"DK-9012-GH","Mercedes","Citaro",2018,180000,"hors_service",NULL)')
c.execute('INSERT INTO vehicules VALUES(5,"DK-3456-IJ","Scania","N230",2022,25000,"actif",NULL)')

c.execute('INSERT INTO chauffeurs VALUES(1,"FALL","Ibrahima","771234567","B","2019-03-15","actif")')
c.execute('INSERT INTO chauffeurs VALUES(2,"DIOP","Moussa","772345678","D","2020-06-01","actif")')
c.execute('INSERT INTO chauffeurs VALUES(3,"SOW","Fatou","773456789","B","2018-01-10","actif")')
c.execute('INSERT INTO chauffeurs VALUES(4,"NDIAYE","Ousmane","774567890","D","2021-09-05","conge")')
c.execute('INSERT INTO chauffeurs VALUES(5,"SYLLA","Mamadou","775678901","B","2022-02-20","actif")')

c.execute('INSERT INTO lignes VALUES(1,"L1","Gare Routiere - Point E","Gare Routiere","Point E",15.5)')
c.execute('INSERT INTO lignes VALUES(2,"L2","Pikine - Almadies","Pikine","Almadies",22.0)')
c.execute('INSERT INTO lignes VALUES(3,"L3","Dakar Plateau - AIBD","Dakar Plateau","AIBD",35.0)')
c.execute('INSERT INTO lignes VALUES(4,"L4","Guediawaye - Place de la Nation","Guediawaye","Place de la Nation",18.5)')
c.execute('INSERT INTO lignes VALUES(5,"L5","Rufisque - Parcelles Assainies","Rufisque","Parcelles Assainies",25.0)')

c.execute('INSERT INTO tarifs VALUES(1,1,"standard",25.0)')
c.execute('INSERT INTO tarifs VALUES(2,1,"reduit",15.0)')
c.execute('INSERT INTO tarifs VALUES(3,2,"standard",30.0)')

c.execute('INSERT INTO trajets VALUES(1,1,1,1,"2026-04-07 08:00:00","2026-04-07 08:45:00",45,"termine")')
c.execute('INSERT INTO trajets VALUES(2,2,2,2,"2026-04-07 09:00:00","2026-04-07 09:50:00",38,"termine")')
c.execute('INSERT INTO trajets VALUES(3,3,3,1,"2026-04-07 10:00:00","2026-04-07 10:45:00",52,"termine")')
c.execute('INSERT INTO trajets VALUES(4,1,1,3,"2026-04-08 08:00:00","2026-04-08 09:00:00",28,"termine")')
c.execute('INSERT INTO trajets VALUES(5,2,2,2,"2026-04-08 09:00:00","2026-04-08 09:50:00",41,"termine")')
c.execute('INSERT INTO trajets VALUES(6,3,3,4,"2026-04-08 10:00:00","2026-04-08 10:40:00",35,"termine")')
c.execute('INSERT INTO trajets VALUES(7,5,5,5,"2026-04-09 08:00:00","2026-04-09 09:00:00",22,"termine")')
c.execute('INSERT INTO trajets VALUES(8,2,2,1,"2026-04-09 09:00:00","2026-04-09 09:45:00",48,"termine")')
c.execute('INSERT INTO trajets VALUES(9,3,3,3,"2026-04-10 08:00:00","2026-04-10 09:00:00",30,"termine")')
c.execute('INSERT INTO trajets VALUES(10,1,1,2,"2026-04-10 09:00:00","2026-04-10 09:50:00",44,"termine")')
c.execute('INSERT INTO trajets VALUES(11,5,5,4,"2026-04-11 08:00:00","2026-04-11 08:40:00",25,"termine")')
c.execute('INSERT INTO trajets VALUES(12,2,2,5,"2026-04-12 08:00:00","2026-04-12 09:00:00",18,"termine")')

c.execute('INSERT INTO incidents VALUES(1,1,"Retard de 10 min cause embouteillage","2026-04-07 08:30:00","legel")')
c.execute('INSERT INTO incidents VALUES(2,2,"Panne technique siege defaillant","2026-04-07 09:30:00","moyen")')
c.execute('INSERT INTO incidents VALUES(3,4,"Accident legersection, aucun bless","2026-04-08 08:15:00","grave")')
c.execute('INSERT INTO incidents VALUES(4,7,"Retard de 5 min","2026-04-09 08:10:00","legel")')
c.execute('INSERT INTO incidents VALUES(5,9,"Client difficultpayment","2026-04-10 08:30:00","legel")')

conn.commit()
conn.close()
print("OK")