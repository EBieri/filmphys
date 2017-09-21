#!/usr/bin/python

# Laden der Module:
import Filmphys as ff
import os
from xml.dom.minidom import parse
import xml.dom.minidom
import hashlib
import sqlite3
from pathlib import Path
#import csv

# Definitionen / Variablen
# Wenn debug = 0: Weniger Ausgaben.
debug = 0

sNameFilmverzeichnis = "Filmverzeichnis"
listeMitEintraegen = ['titel', 'stichworte', 'beschreibung', 'laenge', 'klassenstufe', 'thema', 'bemerkungen']
sPfadPythonscript = os.getcwd()
sPfadFilmverzeichnis = sPfadPythonscript + os.sep + sNameFilmverzeichnis
sNameSQLliteDB = "filmeDB.db"
listeFilme = []
# iID = 0

# Verbindung zu Datenbank erzeugen
connection = sqlite3.connect(sNameSQLliteDB)

# Falls es noch keine Tabelle hat -> anlegen:
#filepathobj = Path(sPfadPythonscript + os.sep + sNameSQLliteDB)
#if not filepathobj.exists():

# Datensatucursor erzeugen
cursor = connection.cursor()
# Tabelle erzeugen
sql = "CREATE TABLE IF NOT EXISTS filme(" \
        "titel TEXT, " \
        "stichworte TEXT, " \
        "beschreibung TEXT, " \
        "laenge INTEGER, "\
        "klassenstufe TEXT, "\
        "thema TEXT, "\
        "bemerkungen TEXT, "\
        "pfad TEXT, "\
        "hash TEXT PRIMARY KEY)"
print(sql)
cursor.execute(sql)      

for root, dirs, files in os.walk(sPfadFilmverzeichnis):
    sPfadAlsListe = root.split(os.sep)
    iLaengePfadAlsListe = len(sPfadAlsListe)
    
    for file in files:
        if debug:
            print(file)
            #print(file.split(".")[0])
            #print(file.split(".")[1])
        if file.split(".")[1] == "xml":
            ListeEintraegeFilm = []
            # iID = iID + 1
            # ListeEintraegeFilm.append(iID)
            
            datei = root + os.sep + file
            if debug:
                print(type(datei))
                print(datei)
            # Falls XML-Datei formal inkosistent -> Fehlermeldung
            try:
                DOMTree = xml.dom.minidom.parse(datei)
            except:
                print(" ----------------- ACHTUNG! ABBRUCH ----------------- ")
                print("Fehler in der XML-Datei: ")
                print(datei)
                print("Die Ausführung des Skriptes wurde abgebrochen.")
                print(" ---------------------------------------------------- ")
                break

            film = DOMTree.documentElement
            for eintrag in listeMitEintraegen:
                s = film.getElementsByTagName(eintrag)[0].childNodes[0].data
                ListeEintraegeFilm.append(s)

            #Name der gleichnamigen Filmdatei bestimmen:
            #print(file.split("."))
            for filmfile in files:
                if file.split(".")[0] == filmfile.split(".")[0] and file.split(".")[1] != filmfile.split(".")[1]:
                    # Pfad als Liste speichern: Verhindert speichern von
                    # OS-abhängigem Pfadseparator:
                    pfad = root + os.sep + filmfile
                    ListeEintraegeFilm.append(pfad)
                    #Filmdatei einlesen und haswert bestimmen:
                    with open(root + os.sep + filmfile, "rb") as f:
                        data = f.read()
                        sha1summe = hashlib.sha1()
                        sha1summe.update(data)
                        bstr = sha1summe.hexdigest()
                        #print(bstr[:8])
                        ListeEintraegeFilm.append(bstr[:8])

            listeFilme.append(ListeEintraegeFilm)
            #print(ListeEintraegeFilm)

# Datensaetze einlesen:
for film in listeFilme:
    print(film)
    sql = "INSERT INTO filme VALUES('"
    for index, eintrag in enumerate(film):
        #print(index)
        # Maskierung von Hochzeichen bei SQL-Lite
        eintrag = eintrag.replace("'","''") 
        if index == 0:
            sql = sql + eintrag
        else:
            sql = sql + "', '" + eintrag
    sql = sql + "')"
    print(sql)
    cursor.execute(sql)
    connection.commit()

#Verbindung beenden
connection.close()
