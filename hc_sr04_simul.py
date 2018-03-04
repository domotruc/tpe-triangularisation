#!/usr/bin/python
# coding: utf-8
#
# Simule les valeurs retournées par le capteur ultrason HC-SR04
# afin de tester/debugger le programme avant de l'utiliser avec le vrai capteur

from random import *
from math import *

# Clefs pour définir les caractéristiques d'un capteur de distance
TRIG = "TRIG"   # Pin pour déclencher la mesure de distance
ECHO = "ECHO"   # Pin pour lecture de l'echo
X = "X"         # Coordonnée X du capteur (en cm)
Y = "Y"         # Coordonnée Y du capteur (en cm)

# Position simulée du véhicule (en cm)
POS_VHCL = { X: 20, Y: 30 }

# sigma du bruit de mesure (en cm)
SIGMA = 1


def mesure(capteur):
  """
  Simule la mesure du capteur passé en argument et renvoie la distance (en cm)

  Parameters:
  -----------
  capteur : définit les pins du capteur
    capteur[TRIG]: pin pour déclencher la mesure de distance
    capteur[ECHO]: pin pour lecture de l'echo
    capteur[X]: coordonnée X du capteur (en cm)
    capteur[Y]: coordonnée Y du capteur (en cm)

  Returns:
  --------
  tableau : d
    distance entre le capteur et le véhicule (en cm)
  """

  return sqrt ((POS_VHCL[X] + gauss(0, SIGMA) - capteur[X])**2 + (POS_VHCL[Y] + gauss(0, SIGMA) - capteur[Y])**2)
