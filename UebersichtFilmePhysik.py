#!/usr/bin/python

# Wenn debug = 0: Weniger Ausgaben.
debug = 1
NameFilmverzeichnis = "Filmverzeichnis"

import ModuleFilmphys as mf
import os
from xml.dom.minidom import parse
import xml.dom.minidom
import hashlib
import csv

# Schlussendlich sollen alle Funktionen als Module augelagert werden
# Das vereinfacht die Wartung und erhöht die Übersicht.

# Test Module ModuleFilmphys
mf.saghallo()

# Übersicht Variablen:
pfadPythonscript = os.getcwd()
pfadFilmverzeichnis = pfadPythonscript + os.sep + NameFilmverzeichnis
for root, dirs, files in os.walk(pfadFilmverzeichnis):
    PfadAlsListe = root.split(os.sep)
    LaengePfadAlsListe = len(PfadAlsListe)
    break

ListeMitDateienOhneEndung = []
ListeXMLDateiMitFilmDateien = []
ListeXMLDateiMitFilmDateienNameFilm = []
ListeDateienOhneXML = []
ListeXMLDateienOhneFilmDateien = []

DatenAlleFilme = []

# diverse Ausgaben
if debug == 1:
    print("")
    print("------------")
    print("Ausgabe:")
    print("pfadPythonscript:    " + pfadPythonscript)
    print("pfadFilmverzeichnis: " + pfadFilmverzeichnis)
    print(PfadAlsListe)
    print(LaengePfadAlsListe)
    print("------------")
    print("")

# *Verzeichnis duchsuchen und Datenstruktur zurückgeben*
# Im Moment wird der Pfad zum Filmverzeichnis bestimmt durch den Pfad
# dieser Datei (durch os.getcwd() )
# (nice to have, wirklich?) Verzeichnis mit GUI auswaehlen
# Es wird davon ausgegangen, dass es immer xml/Filmdateien-Paare gibt

# 1. Verzeichnis nach Konsistenz prüfen, ohne Daten auszulesen
# -> Rückgabe sind vier (oder evtl. später) Listen:
# a) Dateien ohne Endung
# b) Liste mit den xml-Dateien, von welchen es eine gleichnamige Filmdatei gibt.
# c) Liste von xml-Dateien ohne gleichnamige Filmdatei
# d) Liste von (Film-)Dateien ohne gleichnamige xml-Datei
# Folgendes Vorgehen:
# - Enthält Pfad unerwünschte Verzeichnisse, welche ausgeschlossen werden sollen (z.B. .git)
#   -> diesen Pfad mit if not ... überspringen
# - Hat Datei eine Endung (mit file.split('.'))? -> falls ja in entsprechender Liste notieren
# - falls nein: ist es eine xml-Datei?
#           falls ja: gibt es eine Datei mit gleichem Namen aber anderer Endung?:
#                   andernfalls gibt es nur eine xml-Datei
#           falls nein: gibt es eine xml-Datei mit gleichem Namen?
#                   falls ja: Nichts machen, falls nein: notieren
# -Debug: Listen ausgeben
#           
#
# 2. Liste b) durchgehen und Datenstruktur erstellen

istXMLDateivorhanden = 0
weitereDateiVorhanden = 0

for root, dirs, files in os.walk(pfadFilmverzeichnis):
    if not (mf.PfadAnalysieren(PfadAlsListe,".git")):
        for file in files:
            DateiUndEndung = file.split('.')
            if len(DateiUndEndung) < 2:
                print("NOTIEREN: " + DateiUndEndung[0] + ": Diese Datei hat keine Endung.")
                ListeMitDateienOhneEndung.append(root + os.sep + DateiUndEndung[0])
            else:
                weitereDateiVorhanden = 0
                verzeichnisVorhanden = 0
                if DateiUndEndung[1] == "xml":
                    Eintrag = []
                    for file2 in files:
                        DateiUndEndung2 = file2.split('.')
                        if DateiUndEndung[0] == DateiUndEndung2[0] and DateiUndEndung[1] != DateiUndEndung2[1]:
                            # weitere Datei vorhanden
                            weitereDateiVorhanden = 1
                            print("NOTIEREN: " + DateiUndEndung[0] + "." + DateiUndEndung[1] + ": Es ist eine XML-Datei + weitere Datei vorhanden.")
                            Eintrag.append(root + os.sep + DateiUndEndung[0] + "." + DateiUndEndung[1])
                            Eintrag.append(DateiUndEndung2[1])
                            
                            for dir in dirs:
                                if dir == DateiUndEndung[0]:
                                    verzeichnisVorhanden = 1
                                    #print(dir + '/' + file)
                            if verzeichnisVorhanden == 1:
                                Eintrag.append("JA")
                            else:
                                Eintrag.append("nein")
                            #Zuletzt noch Name eintragen (ohne Pfad)
                            Eintrag.append(DateiUndEndung[0] + "." + DateiUndEndung2[1])

                    #print(Eintrag)
                            ListeXMLDateiMitFilmDateien.append(Eintrag)

                    #if weitereDateiVorhanden == 1:
                    #    print("NOTIEREN: " + DateiUndEndung[0] + "." + DateiUndEndung[1] + ": Es ist eine XML-Datei + weitere Datei vorhanden.")
                    #    ListeXMLDateiMitFilmDateien.append(root + os.sep + DateiUndEndung[0] + "." + DateiUndEndung[1])
                    #    ListeXMLDateiMitFilmDateienNameFilm.append(root + os.sep + DateiUndEndung2[0] + "." + DateiUndEndung2[1])
                    if not weitereDateiVorhanden == 1:
                        print("NOTIEREN: " + DateiUndEndung[0] + "." + DateiUndEndung[1] + ": Es ist NUR eine XML-Datei vorhanden.")
                        ListeXMLDateienOhneFilmDateien.append(root + os.sep + DateiUndEndung[0] + "." + DateiUndEndung[1])
                else:
                    # Testen, ob es noch eine XML-Datei gibt. Falls ja: Nichts machen.
                    # Falls nein: Datei notieren.
                    DateiOhneXMLDatei = 1
                    for file2 in files:
                        DateiUndEndung2 = file2.split('.')
                        if DateiUndEndung[0] == DateiUndEndung2[0] and DateiUndEndung2[1] == "xml":
                            if debug:
                                print("Keine Aktion: " + DateiUndEndung[0] + "." + DateiUndEndung[1] + ": Keine XML-Datei, aber es ist eine gleichnamige xml-Datei vorhanden: " + DateiUndEndung2[0] + "." + DateiUndEndung2[1])
                            DateiOhneXMLDatei = 0
                    if DateiOhneXMLDatei:
                        print("NOTIEREN: " + DateiUndEndung[0] + "." + DateiUndEndung[1] + ": Keine XML-Datei, und es ist auch keine gleichnamige xml-Datei vorhanden.")
                        ListeDateienOhneXML.append(root + os.sep + DateiUndEndung[0] + "." + DateiUndEndung[1])
                        

# Übersicht Listen
if debug:
    print("")
    print("------------")
    print("*** Übersicht Dateilisten ***")
    print("Liste mit xml-Dateien mit Film:")
    print(ListeXMLDateiMitFilmDateien)
    print("")
    print("Liste mit Dateien ohne Endung:")
    print(ListeMitDateienOhneEndung)
    print("")
    print("Liste mit xml-Dateien ohne Film:")
    print(ListeXMLDateienOhneFilmDateien)
    print("")
    print("Liste mit Dateien ohne XML-Datei:")
    print(ListeDateienOhneXML)
    print("")
    print("------------")
    print("")

# Liste ListeXMLDateiMitFilmDateien durchgehen und Daten aus XML-Dateien auslesen:
listeMitEintraegen = ['titel', 'beschreibung', 'stichworte']
for datei in ListeXMLDateiMitFilmDateien:
    print("datei[0]")
    print(datei)
    print("HIER")
    print(type(datei[0]))
    print(datei[0])
    print(datei[0][:-4] + '.' + datei[1])
    DOMTree = xml.dom.minidom.parse(datei[0])
    film = DOMTree.documentElement
    
    DatenEinzelnerFilm = []
    for eintrag in listeMitEintraegen:
        # Falls kein Eintrag vorhanden, gibt es eine Fehlermeldung:
        if eintrag == 'titel':
            try:
                s = film.getElementsByTagName(eintrag)[0].childNodes[0].data
            except:
                #s = datei[0].split('/')[-1:][0][:-4]
                s = datei[3]
                #print(s)
        else:
            try:
                s = film.getElementsByTagName(eintrag)[0].childNodes[0].data
            except:
                s = ""
                #print(s)
        
        DatenEinzelnerFilm.append(s)
        
    #Film-Verzeichnis auslesen:
    #print("Filmverzeichnis:")
    #print(datei[len(pfadFilmverzeichnis):-4])
    link = '<a href="' + "file://" + datei[0][:-4] + '.' + datei[1] + '"> ' + datei[0][len(pfadFilmverzeichnis)+1:-4] + '.' + datei[1] + '</a> '
    print("/".join(link.split('\\')))
    #DatenEinzelnerFilm.append(datei[0][len(pfadFilmverzeichnis)+1:-4] + '.' + datei[1])
    DatenEinzelnerFilm.append("/".join(link.split('\\')))

    #Hashsumme (sha1sum) Datei bestimmen:
    with open(datei[0][:-4] + '.' + datei[1], "rb") as f:
        data = f.read()
        sha1summe = hashlib.sha1()
        sha1summe.update(data)
        bstr = sha1summe.hexdigest()
        #print(bstr[:8])
        
    DatenEinzelnerFilm.append(bstr[:8])

    #Hat es Material?
    if datei[2] == 'JA':
        s = '<a href="' + "file://" + datei[0][:-4] + '"> ' + datei[2] + '</a> '
        DatenEinzelnerFilm.append("/".join(s.split('\\')))
    else:
        DatenEinzelnerFilm.append(datei[2])

    DatenAlleFilme.append(DatenEinzelnerFilm)

    print("DatenAllerFilme")
    print(DatenAlleFilme)
        
# HTML-Datei Daten:
HTMLString = ""
NameHTMLDatei = "UebersichtFilme2.html"
TitelHTMLDatei = '&Uuml;bersicht Filme'
AnzahlKategorien = len(DatenAlleFilme[0])
SpaltenNamen = listeMitEintraegen
SpaltenNamen.append('verzeichnis (ausgehend von ' + NameFilmverzeichnis + ')')
SpaltenNamen.append('hash')
SpaltenNamen.append('m')
AnzahlSpaltenNamen = len(SpaltenNamen)
print(str(AnzahlSpaltenNamen) + '/' + str(AnzahlKategorien))
if AnzahlSpaltenNamen != AnzahlKategorien:
    print("Die Anzahl Spalten und Anzahl Kategorien stimmt nicht überein, ABRUCH!")
    exit

Ausgabedatei = open(NameHTMLDatei,"w")
AnfangHTML = "<!DOCTYPE html>" + '\n' + '<html lang="de">' + '\n' + '<head>' + '\n' + '<meta charset="utf-8">' + '\n' + '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + '\n' + '<title> ' + TitelHTMLDatei + ' </title>' + '\n' + '</head>' + '\n' + '<body>' + '\n'
#Ausgabedatei.write(AnfangHTML)
HTMLString = HTMLString + AnfangHTML
#Ausgabedatei.write('<h2> ' + TitelHTMLDatei + ' </h2>')
HTMLString = HTMLString + '<h2> ' + TitelHTMLDatei + ' </h2>'
AnfangTabelle = '<table border="1" width="100%">' + '\n' + '<colgroup>' + '\n'
s = ""
for i in range(0,AnzahlSpaltenNamen):
    s = s + '<col width="1*">'
AnfangTabelle = AnfangTabelle + '\n' + '</colgroup>' + '\n' + '<tr bgcolor="#EEEEEE">' + '\n'
#Ausgabedatei.write(AnfangTabelle)
HTMLString = HTMLString + AnfangTabelle

MitteTabelle = ""
for i in range(0,AnzahlSpaltenNamen):
    #print(i)
    #print(SpaltenNamen[i])
    MitteTabelle = MitteTabelle + '<td> <b> ' + SpaltenNamen[i] + '</b> </td>'
MitteTabelle = MitteTabelle + '\n' + '</tr>' + '\n'
#Ausgabedatei.write(MitteTabelle)
HTMLString = HTMLString + MitteTabelle

print(len(DatenAlleFilme))
#for i in range(0,2):
for i in range(len(DatenAlleFilme)):
    NeueZeile = "<tr>"
    for j in range(0,AnzahlSpaltenNamen):
        NeueZeile = NeueZeile + '<td> ' + str(DatenAlleFilme[i][j]) + '</td>'
    NeueZeile = NeueZeile + '\n' + '</tr>' + '\n'
    #Ausgabedatei.write(NeueZeile)
    HTMLString = HTMLString + NeueZeile

EndeTabelle = '<!-- usw. andere Zeilen der Tabelle -->' + '\n' + '</table>' + '\n'
#Ausgabedatei.write(EndeTabelle)
HTMLString = HTMLString + EndeTabelle

EndeHTML = '</body>' + '\n' + '</html>'
#Ausgabedatei.write(EndeHTML)
HTMLString = HTMLString + EndeHTML
#Umlaute in HTML-Version umschreiben
HTMLString = HTMLString.replace("ü","&uuml;")
HTMLString = HTMLString.replace("Ü","&Uuml;")
HTMLString = HTMLString.replace("ö","&ouml;")
HTMLString = HTMLString.replace("Ö","&Ouml;")
HTMLString = HTMLString.replace("ä","&auml;")
HTMLString = HTMLString.replace("Ä","&Auml;")
Ausgabedatei.write(HTMLString)
Ausgabedatei.close()

# DatenAlleFilme als csv-Datei speichern:
if not os.path.exists('csv-Dateien'):
    os.makedirs('csv-Dateien')
    print("------------------------------------------------")
    print('Verzeichnis csv-Dateien erstellt.')
csv_Datei = open("csv-Dateien/UebersichtFilme.csv", "w")
csv_writer = csv.writer(csv_Datei)
print('---------------------------------')
for row in DatenAlleFilme:
    row2 = []
    for i in row:
        print(i.find('<a href="file://'))
        print(i.find('>'))
        if i.find('<a href="file://') != -1 and i.find('">') != -1:
            a = i.find('<a href="file://') + len('<a href="file://')
            b = i.find('">')
            i = i[a:b]
            print("*" + i)
        row2.append(i)
    print(row2)
    csv_writer.writerow(row2)
csv_Datei.close()

#Ausgabe Fehler
if not os.path.exists('Log-Dateien'):
    os.makedirs('Log-Dateien')
    print("------------------------------------------------")
    print('Verzeichnis Log-Dateien erstellt.')
Dout = open("Log-Dateien/ListeMitDateienOhneEndung.txt","w")
s = ""
for i in ListeMitDateienOhneEndung:
    s = s + str(i) + '\n'
Dout.write(s)
Dout.close()

Dout = open("Log-Dateien/ListeXMLDateienOhneFilmDateien.txt","w")
s = ""
for i in ListeXMLDateienOhneFilmDateien:
    s = s + str(i) + '\n'
Dout.write(s)
Dout.close()

Dout = open("Log-Dateien/ListeDateienOhneXML.txt","w")
s = ""
for i in ListeDateienOhneXML:
    s = s + str(i) + '\n'
Dout.write(s)
Dout.close()
