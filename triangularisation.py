#!/usr/bin/python
# coding: utf-8

#
# Calcule de la position d'un objet à partir des mesures de distance fournies
# par plusieurs capteurs ultrason.
#
# Matériel: Raspberry 3, capteurs ultrason HC-SR04

# Import des librairies requises
from __future__ import print_function
import time
from math import *
from definition import *
#from hc_sr04_simul import *
from hc_sr04 import *


# ------------------------------------------------------------------------------
#    Fonctions
# ------------------------------------------------------------------------------

def measure_average(capteur):
  """
  Réalise plusieurs mesures de distance pour le capteur passé en argument et
  retourne la valeur moyennée.

  Parameters:
  -----------
  capteur : voir fonction measure


  Returns:
  --------
  float : distance en cm
  """

  dist = 0
  n = 0
  for i in range(0,5):
    d = mesure(capteur)
    print("{:s}: {:3.1f}".format(capteur[NAME], d))
    if d < maxDistance:
      dist = dist + d
      n = n + 1
    time.sleep(0.2)

  if n > 0:
    return dist / n
  else:
    return 0


def calcule_position(c1, c2, d1, d2):
  """
  Calcule les 2 positions possibles de l'objet à partir des mesures de distance
  fournies par chacun des 2 capteurs passés en argument.

  Parameters:
  -----------
  c1 : {X, Y}
     capteur 1
     c1[X] : coordonnée X du capteur 1 (en cm)
     c1[Y] : coordonnée Y du capteur 1 (en cm)
  c2 :
    capteur 2, voir c1
  d1 : distance mesurée par capteur 1 (en cm)
  d2 : distance mesurée par capteur 2 (en cm)

  Returns:
  --------
  tableau : (p1, p2)
    tableau contenant les 2 positions possibles
    p1[X]: coordonnée X du point 1 (en cm)
    p1[Y]: coordonnée Y du point 1 (en cm)
    p2[X]: coordonnée X du point 2 (en cm)
    p2[Y]: coordonnée Y du point 2 (en cm)
  """

  if c1[Y] != c2[Y] :
    N=(d2**2-d1**2-c2[X]**2+c1[X]**2-c2[Y]**2+c1[Y]**2)/(2*(c1[Y]-c2[Y]))
    A=((c1[X]-c2[X])/(c1[Y]-c2[Y]))**2+1
    B=2*c1[Y]*((c1[X]-c2[X])/(c1[Y]-c2[Y]))-2*N*((c1[X]-c2[X])/(c1[Y]-c2[Y]))-2*c1[X]
    C=c1[X]**2+c1[Y]**2+N**2-d1**2-2*c1[Y]*N
    Disc=B**2-4*A*C

    if Disc>0:
      p1={}
      p2={}
      p1[X]=(-B+sqrt(Disc))/(2*A)
      p2[X]=(-B-sqrt(Disc))/(2*A)
      p1[Y]=N-p1[X]*((c1[X]-c2[X])/(c1[Y]-c2[Y]))
      p2[Y]=N-p2[X]*((c1[X]-c2[X])/(c1[Y]-c2[Y]))
      return (p1, p2)

    if Disc==0:
      p1={}
      p2={}
      p1[X]=-B/(2*A)
      p1[Y]=N-p1[X]*((c1[X]-c2[X])/(c1[Y]-c2[Y]))
      return (p1)

    if Disc<0:
      return None

  else :
    p1={}
    p2={}
    p1[X]=(d2**2-d1**2-c2[X]**2+c1[X]**2)/(2*(c1[X]-c2[X]))
    p2[X]=p1[X]
    A=1
    B=-2*c2[Y]
    C=c2[X]**2+p1[X]**2-2*c2[X]*p1[X]+c2[Y]**2-d2**2
    Disc=B**2-4*A*C

    if Disc>0:
      p1[Y]=(-B+sqrt(Disc))/(2*A)
      p2[Y]=(-B-sqrt(Disc))/(2*A)
      return (p1, p2)

    if Disc==0:
      p1[Y]=-B/(2*A)
      return (p1)

    if Disc<0:
      return None


def print_position(P):
  """
  Affiche le tableau des position retourné par calcule_position

  Parameters:
  -----------
  P : tableau des positions retournées par calcule_position, voir cette fonction

  Returns:
  --------
  rien
  """

  if P == None:
    print(P)
  else:
    for p in P:
      print("X: {: 5.1f}  Y: {: 5.1f}".format(p[X], p[Y]))


# ------------------------------------------------------------------------------
#    Programme principal
# ------------------------------------------------------------------------------


print("Vitesse du son prise en compte:", speedSound/100, "m/s at ", temperature, "deg")

capteurs = [
  {NAME: "X0Y0", TRIG: 23, ECHO: 24, X:   0, Y:   0},
  {NAME: "X0Y1", TRIG: 20, ECHO: 21, X:   0, Y: 100},
  {NAME: "X1Y1", TRIG: 12, ECHO: 13, X: 100, Y: 100},
  {NAME: "X1Y0", TRIG:  5, ECHO:  6, X: 100, Y:   0}
]

# Nombre de capteurs
nb_capteurs = len(capteurs)

# Initialise les capteurs
init_capteurs(capteurs)

# Allocation du tableau de mesure des distances
d = range(nb_capteurs)

# Mesure des distances par les capteurs
for i in range(nb_capteurs):
  d[i] = measure_average(capteurs[i]) + dimCaracteristique
  print("Distance {:s}: {:5.1f}".format(capteurs[i][NAME], d[i]))

# Intersection des cercles
for i in range(nb_capteurs):
  prev_i = (i - 1) % nb_capteurs
  next_i = (i + 1) % nb_capteurs
  print("prev_i=", prev_i, ", i=", i, ", next_i=", next_i)
  Pprev = calcule_position(capteurs[prev_i], capteurs[i], d[prev_i], d[i])
  Pnext = calcule_position(capteurs[i], capteurs[next_i], d[i], d[next_i])
  print_position(Pprev)
  print_position(Pnext)

print("")

fin_capteurs(capteurs)
