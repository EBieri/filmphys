#!/usr/bin/python

import os

def saghallo():
    print("hallo!")

def PfadAnalysieren(pfadalsliste,vergleichsstring):
    # pfadalsliste: Pfad in Listenform
    # vergleichsstring: String, nach welchem gesucht wird.
    ausgabe = 0
    for i in pfadalsliste:
        if i == vergleichsstring:
            ausgabe = 1
    return ausgabe
