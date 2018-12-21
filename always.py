#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
Lancé à chaque frame durant tout le jeu.
"""

from time import time

from bge import logic as gl
from blendergetobject import get_all_objects
            

def start(all_obj):
    print('Start ....\n')
    gl.phase='début du jeu'
    
def debut_jeu(all_obj):
    print('Début du jeu')
    restore_bille_000_dynamics(all_obj)
    gl.tempo['always'].reset()
    gl.result = 0
    gl.temps = time()
    gl.retard += 1
    gl.phase ="jeu avant retard"
    print('Retard de', gl.retard, 'frames')
    
def jeu_avant_retard(all_obj):
    display_time(all_obj)
    # Jeu avant lancement de la 2ème bille
    if gl.retard == gl.tempo['always'].tempo:
        gl.phase='retard'
        #gl.retard_temps = time() - gl.temps
        gl.retard_temps = gl.retard * 0.016666
        
def retard(all_obj):
    print('Lancement de la 2ème bille')
    display_time(all_obj)
    restore_bille_001_dynamics(all_obj)
    gl.phase='jeu après retard'
    
def jeu_apres_retard(all_obj):
    display_time(all_obj)

    # Limitation du temps à 40 secondes
    if time() - gl.temps > 40:
        gl.phase='fin de jeu'
    
    # Jeu après lancement de la 2ème bille
    coll = collision(all_obj)
    if coll:
        gl.phase='fin de jeu'
    
def fin_jeu(all_obj):
    print('Collision')
    gl.result = time() - gl.temps
    gl.phase='début de fin'
    
def debut_fin(all_obj):
    print('Début de fin')
    set_ball_origin(all_obj)
    gl.tempo['fin'].reset()
    gl.phase='fin'
    
def fin(all_obj):
    #print('Affichage du score')
    display_result(all_obj)
    if gl.tempo['fin'].tempo > 240:
        print("Fin de l'affichage")
        gl.phase='fin de fin'
        
def fin_de_fin(all_obj):
    write()
    gl.phase='début du jeu'


STATES = {  'P': start,
            'début du jeu': debut_jeu,
            'jeu avant retard': jeu_avant_retard,
            'retard': retard,
            'jeu après retard': jeu_apres_retard,
            'fin de jeu': fin_jeu,
            'début de fin': debut_fin,
            'fin': fin,
            'fin de fin': fin_de_fin }


def main():
    global STATES
    
    # Mise à jour des tempos
    gl.tempo.update()

    # Pour appels sur les objets
    all_obj = get_all_objects()

    for state, action in STATES.items():
        if gl.phase == state:
            action.__call__(all_obj)

def display_time(all_obj):
    # Temps écoulé depuis lancement 1ère bille
    t = time() - gl.temps
    all_obj['Text.001'].resolution = 64
    all_obj['Text.001']['Text'] = 'Temps écoulé\n  ' + str(round(t, 3))
    
def restore_bille_000_dynamics(all_obj):
    all_obj['bille.000'].restoreDynamics()

def restore_bille_001_dynamics(all_obj):    
    all_obj['bille.001'].restoreDynamics()

def get_distance_entre_billes(all_obj):
    """diamètre bille = 0.120
    Les billes se touchent si distance entre bille = diamètre bille
    """
    vect = all_obj['bille.000'].worldPosition - all_obj['bille.001'].worldPosition
    dist = (vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])**0.5
    return dist

def collision(all_obj):
    dist = get_distance_entre_billes(all_obj)
    if dist <= 0.122:
        touch = 1
    else:
        touch = 0
    return touch

def set_ball_origin(all_obj):
    # Fixe
    all_obj['bille.000'].suspendDynamics()
    all_obj['bille.001'].suspendDynamics()
    
    all_obj['bille.000'].worldPosition[0] = 1.87
    all_obj['bille.000'].worldPosition[1] = 0
    all_obj['bille.000'].worldPosition[2] = 1.55
    
    all_obj['bille.001'].worldPosition[0] = 0
    all_obj['bille.001'].worldPosition[1] = 1.87
    all_obj['bille.001'].worldPosition[2] = 1.55

def display_result(all_obj):
    all_obj['Text'].resolution = 64
    
    result = round(gl.result, 3)
    retard = round(gl.retard_temps, 3)
    
    all_obj['Text']['Text'] = 'Temps:' + '\n    ' + str(result) +\
                              '\nRetard en secondes:' + '\n    ' + str(retard) + \
                              '\nRetard en frames:' + '\n    ' + str(gl.retard)

def write():
    rd = str(round(gl.retard_temps, 3))
    rt = str(round(gl.result, 3))
    data = 'Retard: ' + rd +' --> Résultat: ' + rt + '\n'
    fichier = gl.current_dir + '/result.txt'
    write_data_in_file(data, fichier)
    print(data)

def write_data_in_file(data, fichier):
    """Ecrit des data de type string dans le fichier, écrase l'existant."""

    with open(fichier, 'a') as fd:
        fd.write(data)
    fd.close()
