Projet Hackathon S3
ECE B2Gr1
Gabriel Brousse
Groupe (de projet) 12
Seul membre du groupe



Si la base de données ne fonctionne pas, voici le code SQL pour la base de données "Carnet_a.sqlite":

CREATE TABLE Address (
Address_ID INTEGER PRIMARY KEY,
NumeroEtRue TEXT,
Ville TEXT,
CodePostal INTEGER
);

CREATE TABLE DateDeNaissance (
DateDeNaissance_ID INTEGER PRIMARY KEY,
Jour INTEGER,
Mois INTEGER,
Annee INTEGER
);

CREATE TABLE Contact (
Contact_ID INTEGER PRIMARY KEY,
Nom TEXT,
Prenom TEXT,
DateDeNaissance_ID INTEGER REFERENCES DateDeNaissance (DateDeNaissance_ID),
AddressEmail TEXT,
NumeroDeTelephone INTEGER,
Address_ID INTEGER REFERENCES Address (Address_ID)
);
