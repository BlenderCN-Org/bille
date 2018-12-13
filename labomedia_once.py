#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Ne jamais modifier ce script.

Les scripts:
- labomedia_once.py
- labomedia_always.py
sont les seuls scripts importés directement dans Blender.

Les autres scripts sont importés en temps que modules.

Il est alors possible de les modifier dans un éditeur externe
sans avoir à les recharger dans Blender.
"""

# imports locaux
import once


def main():
    """Fonction lancée à chaque frame dans blender en temps que module."""

    once.main()
