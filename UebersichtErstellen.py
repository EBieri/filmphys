#!/usr/bin/python

import os
import json

DatenArray = []
ListeTextdateienOhneFilm = []
ListeAndereDateienOhneText = []
ListeDateienOhneEndung = []

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
    path = root.split(os.sep)
    if not PathAnalysieren(path,'.git'):
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
                if DateiUndEndung[1] == "txt":
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
                        print("Es gibt Text- und Filmdatei: " + DateiUndEndung[0])
                        DateiZumAuslesen = open(root + '/' + file,"r")
                        Inhalt = DateiZumAuslesen.read()
                        Datenfilm = Inhalt.strip(' \n').split('\n\n')
                        Datenfilm.insert(0, file[:-4])
                        Datenfilm.append(path[-1])
                        DatenArray.append(Datenfilm)
                        print(DatenArray)
                        DateiZumAuslesen.close()
                    else:
                        print("Es gibt NUR eine Textdatei: " + DateiUndEndung[0])
                        if path[-1].strip() == "":
                            ListeTextdateienOhneFilm.append(file)
                        else:
                            ListeTextdateienOhneFilm.append(path[-1] + '/' + file)
                        ListeTextdateienOhneFilm.sort()
                        
                else:
                    #Testen, ob es eine gleichnamige Textdatei gibt:
                    test = 0
                    for file3 in files:
                        DateiUndEndung3 = file3.split('.')
                        if DateiUndEndung[0] == DateiUndEndung3[0] and DateiUndEndung[1] != DateiUndEndung3[1]:
                            test = 1
                            break
                    if test == 0:
                        print("Es gibt NUR eine (Nichttext)datei: " + DateiUndEndung[0])
                        if path[-1].strip() == "":
                            ListeAndereDateienOhneText.append(file)
                        else:
                            ListeAndereDateienOhneText.append(path[-1] + '/' + file)
                        ListeAndereDateienOhneText.sort()
                        
            elif len(DateiUndEndung) == 1:
                print("Diese Datei hat keine Endung: " + DateiUndEndung[0])
                if path[-1].strip() == "":
                    ListeDateienOhneEndung.append(file)
                else:
                    ListeDateienOhneEndung.append(path[-1] + '/' + file)
                ListeDateienOhneEndung.sort()
                    

print("------------------------------------------------")
print("------------------------------------------------")
print("------ Datenarray ---------")
for i in range(len(DatenArray)):
    print(DatenArray[i])
print("Länge: " + str(len(DatenArray)) + ", Breite: " + str(len(DatenArray[0])))
print("------------------------------------------------")
print("------------------------------------------------")
print("------ ListeTextdateienOhneFilm ---------")
for i in range(len(ListeTextdateienOhneFilm)):
    print(ListeTextdateienOhneFilm[i])
print("Länge: " + str(len(ListeTextdateienOhneFilm)) + ", Breite: " + str(len(ListeTextdateienOhneFilm[0])))
print("------------------------------------------------")
print("------------------------------------------------")
print("------ ListeAndereDateienOhneText ---------")
for i in range(len(ListeAndereDateienOhneText)):
    print(ListeAndereDateienOhneText[i])
print("Länge: " + str(len(ListeAndereDateienOhneText)) + ", Breite: " + str(len(ListeAndereDateienOhneText[0])))
print("------------------------------------------------")
print("------------------------------------------------")
print("------ ListeDateienOhneEndung ---------")
for i in range(len(ListeDateienOhneEndung)):
    print(ListeDateienOhneEndung[i])
print("Länge: " + str(len(ListeDateienOhneEndung)) + ", Breite: " + str(len(ListeDateienOhneEndung[0])))

# Nun HTML-Datei erstellen:
Ausgabedatei = open("UebersichtFilme.html","w")
AnfangHTML = "<!DOCTYPE html>" + '\n' + '<html lang="de">' + '\n' + '<head>' + '\n' + '<meta charset="utf-8">' + '\n' + '<meta name="viewport" content="width=device-width, initial-scale=1.0">' + '\n' + '<title> Übersicht Filme </title>' + '\n' + '</head>' + '\n' + '<body>' + '\n'
Ausgabedatei.write(AnfangHTML)
Ausgabedatei.write('<h2> &Uuml;bersicht Filme </h2>')
AnfangTabelle = '<table border="1" width="100%">' + '\n' + '<colgroup>' + '\n' + '<col width="1*">'+ '<col width="1*">' + '\n' + '<col width="1*">' + '\n' + '<col width="1*">' + '\n' + '</colgroup>' + '\n' + '<tr bgcolor="#EEEEEE">' + '\n'
Ausgabedatei.write(AnfangTabelle)
MitteTabelle = '<td> <b>Name Film</b> </td> <td> <b>Kurzbeschreibung</b> </td>' + '<td><b> Stichworte</b> </td>'+ '<td> <b>Verzeichnis</b> </td>' + '\n' + '</tr>' + '\n' 
Ausgabedatei.write(MitteTabelle)
for i in range(len(DatenArray)):
    NeueZeile = '<td> ' + DatenArray[i][0] + '</td>' + '<td> ' + DatenArray[i][1] + '</td>' + '<td> ' + DatenArray[i][2] + '</td>' + '<td> ' + DatenArray[i][3] + '</td>' + '\n' + '</tr>' + '\n'
    Ausgabedatei.write(NeueZeile)
EndeTabelle = '<!-- usw. andere Zeilen der Tabelle -->' + '\n' + '</table>' + '\n'
Ausgabedatei.write(EndeTabelle)

Ausgabedatei.write('<br> <br> <br> <br> <br> <br> <br> <br> <br> ')

Ausgabedatei.write('<br> <h3> Folgende Angaben dienen der Optimierung </h3>')
Ausgabedatei.write('<br> <h4> Textdateien ohne Filmdatei </h4>')
for i in range(len(ListeTextdateienOhneFilm)):
    Ausgabedatei.write(ListeTextdateienOhneFilm[i] + '<br>')

Ausgabedatei.write('<br> <h4> Andere Dateien (Filmdateien und andere...) ohne zugehoerige Textdatei </h4>')
for i in range(len(ListeAndereDateienOhneText)):
    Ausgabedatei.write(ListeAndereDateienOhneText[i] + '<br>')

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
with open('json-Dateien/ListeTextdateienOhneFilm.json', 'w') as f:
    json.dump(ListeTextdateienOhneFilm, f)
with open('json-Dateien/ListeAndereDateienOhneText.json', 'w') as f:
    json.dump(ListeAndereDateienOhneText, f)
with open('json-Dateien/ListeDateienOhneEndung.json', 'w') as f:
    json.dump(ListeDateienOhneEndung, f)
