#!/usr/bin/python

import os
import json
from xml.dom.minidom import parse
import xml.dom.minidom
import hashlib
import csv

DatenArray = []
ListeXMLdateienOhneFilm = []
ListeAndereDateienOhneXML = []
ListeDateienOhneEndung = []
LaengePfad = 0

def PathAnalysieren(pfad,vergleichsstring):
    ausgabe = 0
    for i in pfad:
        if i == vergleichsstring:
            ausgabe = 1
    return ausgabe
    

# Daten auslesen
# Ändern: Aktuelles Verzeichnis soll Ausgangspunkt sein!
#for root, dirs, files in os.walk("/home/verwaltung/Schreibtisch/Projekte_Programmieren/filmphys/"):
for root, dirs, files in os.walk(os.getcwd()):
    LaengePfad = len(root.split(os.sep))
    break

print(LaengePfad)

for root, dirs, files in os.walk(os.getcwd()):
    path = root.split(os.sep)
    if not (PathAnalysieren(path,'.git') or PathAnalysieren(path,'json-Dateien')):
        #print("Eintritt ins .git-Verzeichnis: Abbruch!")
        #break

        for file in files:
            DateiUndEndung = file.split('.')

            #print(root)
            #print(path)
            #print(type(path[-1]))
            #print(path[-1])
            #print(files)
            #print(file + " " + DateiUndEndung[1])
            if len(DateiUndEndung) > 1:
                if DateiUndEndung[1] == "xml":
                    test = 0
                    for file2 in files:
                        DateiUndEndung2 = file2.split('.')
                        if DateiUndEndung[0] == DateiUndEndung2[0] and DateiUndEndung[1] != DateiUndEndung2[1]:
                            test = 1
                            #print("Es gibt Text- und Filmdatei: " + DateiUndEndung[0])
                            break
                        #else:
                        #    test = 0
                    if test == 1:
                        print("Es gibt XML- und Filmdatei: " + DateiUndEndung[0] + "." + DateiUndEndung2[1])
                        s = ""
                        for i in range(LaengePfad,len(path)):
                            s = s + path[i] + '/'
                        print(s + DateiUndEndung[0] + ".xml")
                        DOMTree = xml.dom.minidom.parse(s + DateiUndEndung[0] + ".xml")
                        film = DOMTree.documentElement
                        beschreibung = film.getElementsByTagName('beschreibung')[0].childNodes[0].data
                        stichworte = film.getElementsByTagName('stichworte')[0].childNodes[0].data
                        print(beschreibung)
                        print(stichworte)
                        Datenfilm = []
                        Datenfilm.append(DateiUndEndung[0] + "." + DateiUndEndung2[1])
                        Datenfilm.append(beschreibung)
                        Datenfilm.append(stichworte)

                        Datenfilm.append(s)

                        #sha1sum bestimmen
                        with open(s + DateiUndEndung[0] + "." + DateiUndEndung2[1], "rb") as f:
                            data = f.read()
                            sha1summe = hashlib.sha1()
                            sha1summe.update(data)
                            bstr = sha1summe.hexdigest()
                            #print(type(bstr))
                            #print(bstr[:8])

                        Datenfilm.append(bstr[:8])

                        DatenArray.append(Datenfilm)

                        print(DatenArray)
                        
                    else:
                        print("Es gibt NUR eine XML-Datei: " + DateiUndEndung[0])
                        if path[-1].strip() == "":
                            ListeXMLdateienOhneFilm.append(file)
                        else:
                            ListeXMLdateienOhneFilm.append(path[-1] + '/' + file)
                        ListeXMLdateienOhneFilm.sort()
                        
                else:
                    #Testen, ob es eine gleichnamige XML-Datei gibt:
                    test = 0
                    for file3 in files:
                        DateiUndEndung3 = file3.split('.')
                        if DateiUndEndung[0] == DateiUndEndung3[0] and DateiUndEndung[1] != DateiUndEndung3[1]:
                            test = 1
                            break
                    if test == 0:
                        print("Es gibt NUR eine (Nicht-XML)Datei: " + DateiUndEndung[0])
                        if path[-1].strip() == "":
                            ListeAndereDateienOhneXML.append(file)
                        else:
                            ListeAndereDateienOhneXML.append(path[-1] + '/' + file)
                        ListeAndereDateienOhneXML.sort()
                        
            elif len(DateiUndEndung) == 1:
                print("Diese Datei hat keine Endung: " + DateiUndEndung[0])
                if path[-1].strip() == "":
                    ListeDateienOhneEndung.append(file)
                else:
                    ListeDateienOhneEndung.append(path[-1] + '/' + file)
                ListeDateienOhneEndung.sort()

##print("------------------------------------------------")
##print("------------------------------------------------")
##print("------ Datenarray ---------")
##for i in range(len(DatenArray)):
##    print(DatenArray[i])
##print("Länge: " + str(len(DatenArray)) + ", Breite: " + str(len(DatenArray[0])))
##print("------------------------------------------------")
##print("------------------------------------------------")
##print("------ ListeXMLdateienOhneFilm ---------")
##for i in range(len(ListeXMLdateienOhneFilm)):
##    print(ListeXMLdateienOhneFilm[i])
##print("Länge: " + str(len(ListeXMLdateienOhneFilm)) + ", Breite: " + str(len(ListeXMLdateienOhneFilm[0])))
##print("------------------------------------------------")
##print("------------------------------------------------")
##print("------ ListeAndereDateienOhneXML ---------")
##for i in range(len(ListeAndereDateienOhneXML)):
##    print(ListeAndereDateienOhneXML[i])
##print("Länge: " + str(len(ListeAndereDateienOhneXML)) + ", Breite: " + str(len(ListeAndereDateienOhneXML[0])))
##print("------------------------------------------------")
##print("------------------------------------------------")
##print("------ ListeDateienOhneEndung ---------")
##for i in range(len(ListeDateienOhneEndung)):
##    print(ListeDateienOhneEndung[i])
##print("Länge: " + str(len(ListeDateienOhneEndung)) + ", Breite: " + str(len(ListeDateienOhneEndung[0])))

# HTML-Datei Daten:
Ausgabedatei = open("UebersichtFilme.html","w")
AnfangHTML = "<!DOCTYPE html>" + '\n' + '<html lang="de">' + '\n' + '<head>' + '\n' + '<meta charset="utf-8">' + '\n' + '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + '\n' + '<title> &Uuml;bersicht Filme </title>' + '\n' + '</head>' + '\n' + '<body>' + '\n'
Ausgabedatei.write(AnfangHTML)
Ausgabedatei.write('<h2> &Uuml;bersicht Filme </h2>')
AnfangTabelle = '<table border="1" width="100%">' + '\n' + '<colgroup>' + '\n' + '<col width="1*">'+ '<col width="1*">' + '\n' + '<col width="1*">' + '\n' + '<col width="1*">' + '\n' + '<col width="1*">' + '\n' + '</colgroup>' + '\n' + '<tr bgcolor="#EEEEEE">' + '\n'
Ausgabedatei.write(AnfangTabelle)
MitteTabelle = '<td> <b>Name Film</b> </td> <td> <b>Kurzbeschreibung</b> </td>' + '<td><b> Stichworte</b> </td>'+ '<td> <b>Verzeichnis</b> </td>' + '\n' + '<td> <b>Sha1</b> </td>' + '\n' + '</tr>' + '\n' 
Ausgabedatei.write(MitteTabelle)
for i in range(len(DatenArray)):
    NeueZeile = '<td> ' + DatenArray[i][0] + '</td>' + '<td> ' + DatenArray[i][1] + '</td>' + '<td> ' + DatenArray[i][2] + '</td>' + '<td> ' + DatenArray[i][3] + '</td>' + '\n' + '<td> ' + DatenArray[i][4] + '</td>' + '\n' + '</tr>' + '\n'
    Ausgabedatei.write(NeueZeile)
EndeTabelle = '<!-- usw. andere Zeilen der Tabelle -->' + '\n' + '</table>' + '\n'
Ausgabedatei.write(EndeTabelle)

EndeHTML = '</body>' + '\n' + '</html>'
Ausgabedatei.write(EndeHTML)
Ausgabedatei.close()

# HTML-Datei Kommentare:
Ausgabedatei = open("UebersichtWeitereDateien.html","w")
AnfangHTML = "<!DOCTYPE html>" + '\n' + '<html lang="de">' + '\n' + '<head>' + '\n' + '<meta charset="utf-8">' + '\n' + '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + '\n' + '<title> &Uuml;bersicht Optimierungsdaten </title>' + '\n' + '</head>' + '\n' + '<body>' + '\n'
Ausgabedatei.write(AnfangHTML)
Ausgabedatei.write('<h2> &Uuml;bersicht weitere Dateien </h2>')

Ausgabedatei.write('<br> <h4> XML-Dateien ohne Filmdatei </h4>')
for i in range(len(ListeXMLdateienOhneFilm)):
    Ausgabedatei.write(ListeXMLdateienOhneFilm[i] + '<br>')

Ausgabedatei.write('<br> <h4> Andere Dateien (Filmdateien und andere...) ohne zugehoerige XML-Datei </h4>')
for i in range(len(ListeAndereDateienOhneXML)):
    Ausgabedatei.write(ListeAndereDateienOhneXML[i] + '<br>')

Ausgabedatei.write('<br> <h4> Dateien ohne Dateiendung </h4>')
for i in range(len(ListeDateienOhneEndung)):
    Ausgabedatei.write(ListeDateienOhneEndung[i] + '<br>')

EndeHTML = '</body>' + '\n' + '</html>'
Ausgabedatei.write(EndeHTML)
Ausgabedatei.close()

# Daten als Json-Dateien speichern
if not os.path.exists('json-Dateien'):
    os.makedirs('json-Dateien')
    print("------------------------------------------------")
    print('Verzeichnis json-Dateien erstellt.')
with open('json-Dateien/DatenArray.json', 'w') as f:
    json.dump(DatenArray, f)
    print("------------------------------------------------")
    print('DatenArray.json geschrieben.')
with open('json-Dateien/ListeXMLdateienOhneFilm.json', 'w') as f:
    json.dump(ListeXMLdateienOhneFilm, f)
with open('json-Dateien/ListeAndereDateienOhneXML.json', 'w') as f:
    json.dump(ListeAndereDateienOhneXML, f)
with open('json-Dateien/ListeDateienOhneEndung.json', 'w') as f:
    json.dump(ListeDateienOhneEndung, f)

# DatenArray als csv-Datei speichern:
if not os.path.exists('csv-Dateien'):
    os.makedirs('csv-Dateien')
    print("------------------------------------------------")
    print('Verzeichnis csv-Dateien erstellt.')
csv_Datei = open("csv-Dateien/UebersichtFilme.csv", "w")
csv_writer = csv.writer(csv_Datei)
for row in DatenArray:
    print(row)
    csv_writer.writerow(row)
csv_Datei.close()
