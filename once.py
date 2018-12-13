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

def variable():
    gl.t_touch = 0
    gl.touch = 0
    
    # Phase possible = jeu, fin
    gl.phase = 'jeu'
    gl.result = ''
    gl.temps = time()

    # retard en ms de la 2ème balle
    gl.retard = 0
    gl.bille_001_dynamic = 1
    
def tempo():
    tempo_liste = [('fin', 120)]
    gl.tempo = Tempo(tempo_liste)

def main():
    """Lancé une seule fois à la 1ère frame au début du jeu par main_once."""

    print('Initialisation des scripts lancée un seule fois au début du jeu.')
    
    variable()
    tempo()
    
    # Pour les mondoshawan
    print("Pour l'honneur des Mondoshawan, ")
