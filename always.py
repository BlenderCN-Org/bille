#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


"""
Lancé à chaque frame durant tout le jeu.
"""

from time import time

from bge import logic as gl
from blendergetobject import get_all_objects


RETARD = 0.01666


def main():
    gl.tempo.update()
    all_obj = get_all_objects()
    
    if gl.phase == 'jeu':
        jeu(all_obj)

    if gl.phase == 'fin':
        fin(all_obj)
        
def jeu(all_obj):
    # Départ décalé de la 2ème bille
    if time() - gl.temps > gl.retard and not gl.bille_001_dynamic:
        restore_bille_001_dynamics(all_obj)
        gl.bille_001_dynamic = 1

    dist = get_distance_entre_bille(all_obj)
    gl.touch = collision(dist)

    # Temps écoulé depuis lancement 1ère bille
    t = time() - gl.temps
    all_obj['Text.001']['Text'] = str(round(t, 3))
    
    if gl.touch or t > 40:
        gl.phase = 'fin'
        gl.result = time() - gl.temps
        gl.touch = 0
        gl.tempo['fin'].reset()
    
def fin(all_obj):
        
    set_ball_origin(all_obj)
    display_time(all_obj)

    if gl.tempo['fin'].tempo == 120:
        rd = str(round(gl.retard, 3))
        rt = str(round(gl.result, 3))
        data = 'Retard: ' + rd +' --> Résultat: ' + rt + '\n'
        write(data)
        gl.retard += RETARD
        gl.phase = 'jeu'
        gl.result = ''
        gl.temps = time()
        gl.bille_001_dynamic = 0
        restore_bille_dynamics(all_obj)

def write(data):
    fichier = gl.current_dir + '/result.txt'
    write_data_in_file(data, fichier)
    print(data)

def write_data_in_file(data, fichier):
    """Ecrit des data de type string dans le fichier, écrase l'existant."""

    with open(fichier, 'a') as fd:
        fd.write(data)
    fd.close()
        
def set_ball_origin(all_obj):
    # Fixe
    all_obj['bille'].suspendDynamics()
    all_obj['bille.001'].suspendDynamics()
    
    all_obj['bille'].worldPosition[0] = 1.87
    all_obj['bille'].worldPosition[1] = 0
    all_obj['bille'].worldPosition[2] = 1.55
    
    all_obj['bille.001'].worldPosition[0] = 0
    all_obj['bille.001'].worldPosition[1] = 1.87
    all_obj['bille.001'].worldPosition[2] = 1.55

def restore_bille_dynamics(all_obj):
    all_obj['bille'].restoreDynamics()

def restore_bille_001_dynamics(all_obj):    
    all_obj['bille.001'].restoreDynamics()
    
def get_distance_entre_bille(all_obj):
    """diamètre bille = 0.120
    Les billes se touchent si distance entre bille = diamètre bille
    """
    vect = all_obj['bille'].worldPosition - all_obj['bille.001'].worldPosition
    dist = (vect[0]*vect[0] + vect[1]*vect[1] + vect[2]*vect[2])**0.5
    return dist

def collision(dist):
    if dist <= 0.122:
        touch = 1
    else:
        touch = 0
    return touch

def display_time(all_obj):
    all_obj['Text'].resolution = 64
    result = round(gl.result, 3)
    retard = round(gl.retard, 3)
    all_obj['Text']['Text'] = 'Temps' + '\n    ' + str(result) + '\nDécalage' + '\n    ' + str(retard)
