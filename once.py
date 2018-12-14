#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier lss variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.
"""


from time import time
from bge import logic as gl
from blendertempo import Tempo
import datetime

def variable():
    gl.t_touch = 0
    gl.touch = 0
    
    # Phase possible = jeu, fin
    gl.phase = 'jeu'
    gl.result = ''
    gl.temps = time()

    # retard en ms de la 2ème balle
    gl.retard = 0.00
    gl.bille_001_dynamic = 1

    # Pour écriture fichier
    gl.current_dir = gl.expandPath("//")

def write(data):
    fichier = gl.current_dir + '/result.txt'
    write_data_in_file(data, fichier)
    print(data)

def write_data_in_file(data, fichier):
    """Ecrit des data de type string dans le fichier, écrase l'existant."""

    with open(fichier, 'a') as fd:
        fd.write(data)
    fd.close()

def write_date_time():
    data = '\n'
    t = datetime.datetime.now().strftime("Date: %y %m %d à %H:%M:%S")
    data += t + '\n'
    write(data)
    
def tempo():
    tempo_liste = [('fin', 120)]
    gl.tempo = Tempo(tempo_liste)

def main():
    """Lancé une seule fois à la 1ère frame au début du jeu par main_once."""

    print('Initialisation des scripts lancée un seule fois au début du jeu.')
    
    variable()
    tempo()
    write_date_time()
    # Pour les mondoshawan
    print("Pour l'honneur des Mondoshawan, ")
