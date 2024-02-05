Projet Hackathon S3
ECE B2Gr1
Gabriel Brousse
Groupe (de projet) 12
Seul membre du groupe

Carnet d'adresses, sur interface graphique Tkinter, créé sur PyCharm écrit en Python et PHP (base de données).
Sqlite3 a été utilisé dans la création de la bdd.
Le carnet d’address possède les fonctionnalités suivantes:

- Ajout d'un contact
- Recherche d'un contact
- Modification d'un contact
- Suppression  d'un contact
- Sauvegarde des ajouts et des modifications dans la bdd
- Affichage des contacts sous forme d'une liste
- Notification en cas de doublon
- Tri des contacts
- Filtrage des contacts
- Exportation de la liste des contacts sous format CSV
- Importation de contacts à partir d'un fichier CSV


---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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
