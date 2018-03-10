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
from hc_sr04_simul import *


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

  distance1=mesure(capteur)
  time.sleep(0.1)
  distance2=mesure(capteur)
  time.sleep(0.1)
  distance3=mesure(capteur)
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance


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
    p1[X]=(d2**2-d1**2-c2[X]**2-c1[X]**2)/(2*(c1[X]-c2[X]))
    A=1
    B=-2*c2[Y]
    C=c2[X]**2+p1[X]**2-2*c2[X]*p1[X]+c2[Y]**2-d2**2
    Disc=B**2-4*A*C

    if Disc>0:
      p1[Y]=(-B+sqrt(Disc))/(2*A)
      p2[Y]=(-B-sqrt(Disc))/(2*A)
      p2[X]=p1[X]
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
      print("X: {: 4.1f}  Y: {: 4.1f}".format(p[X], p[Y]))


# ------------------------------------------------------------------------------
#    Programme principal
# ------------------------------------------------------------------------------


# Speed of sound in cm/s at temperature
temperature = 20
speedSound = 33100 + (0.6*temperature)

print("Vitesse du son prise en compte:", speedSound/100, "m/s at ", temperature, "deg")

capteurs = [
  {NAME: "X0Y0", TRIG: 23, ECHO: 24, X: 0,   Y: 0},
  {NAME: "X1Y1", TRIG: 5,  ECHO: 6,  X: 100, Y: 100},
  {NAME: "X1Y0", TRIG: 7,  ECHO : 8, X: 100,  Y: 0}
]

# Initialise les capteurs
init_capteurs(capteurs)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
d=range(3)
try:
  while True:
    for i in range(len(capteurs)):
      d[i] = measure_average(capteurs[i])
      print("Distance {:s}: {:5.1f}".format(capteurs[i][NAME], d[i]))

    P1 = calcule_position(capteurs[0], capteurs[1], d[0], d[1])
    print_position(P1)
    P2 = calcule_position(capteurs[0], capteurs[2], d[0], d[2])
    print_position(P2)

    time.sleep(1)
    print("")

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()
