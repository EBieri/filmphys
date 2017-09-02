#!/usr/bin/python

# Wenn debug = 0: Weniger Ausgaben.
debug = 1
NameFilmverzeichnis = "Filmverzeichnis"

import ModuleFilmphys as mf
import os

# Schlussendlich sollen alle Funktionen als Module augelagert werden
# Das vereinfacht die Wartung und erhöht die Übersicht.

# Test Module ModuleFilmphys
mf.saghallo()

# Übersicht Variablen:
pfadPythonscript = os.getcwd()
pfadFilmverzeichnis = pfadPythonscript + "/" + NameFilmverzeichnis
for root, dirs, files in os.walk(pfadFilmverzeichnis):
    PfadAlsListe = root.split(os.sep)
    LaengePfadAlsListe = len(PfadAlsListe)
    break

ListeMitDateienOhneEndung = []
ListeXMLDateiMitFilmDateien = []
ListeDateienOhneXML = []
ListeXMLDateienOhneFilmDateien = []

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
                if DateiUndEndung[1] == "xml":
                    for file2 in files:
                        DateiUndEndung2 = file2.split('.')
                        if DateiUndEndung[0] == DateiUndEndung2[0] and DateiUndEndung[1] != DateiUndEndung2[1]:
                            # weitere Datei vorhanden
                            weitereDateiVorhanden = 1
                            #if debug:
                            #    print(DateiUndEndung[0] + "." + DateiUndEndung[1] + "/" + DateiUndEndung2[0] + "." + DateiUndEndung2[1])
                    if weitereDateiVorhanden == 1:
                        print("NOTIEREN: " + DateiUndEndung[0] + "." + DateiUndEndung[1] + ": Es ist eine XML-Datei + weitere Datei vorhanden.")
                        ListeXMLDateiMitFilmDateien.append(root + os.sep + DateiUndEndung[0] + "." + DateiUndEndung[1])
                    else:
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
    print("Liste mit Dateien ohne Endung:")
    print(ListeMitDateienOhneEndung)
    print("")
    print("Liste mit xml-Dateien mit Film:")
    print(ListeXMLDateiMitFilmDateien)
    print("")
    print("Liste mit xml-Dateien ohne Film:")
    print(ListeXMLDateienOhneFilmDateien)
    print("")
    print("Liste mit Dateien ohne XML-Datei:")
    print(ListeDateienOhneXML)
    print("")
    print("------------")
    print("")
