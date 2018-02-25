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
import RPi.GPIO as GPIO
from math import *

def measure(capteur):
  """
  Réalise la mesure du capteur passé en argument et renvoie la distance (en cm)

  Parameters:
  -----------
  capteur : définit les pins du capteur
    capteur[TRIG]: pin pour déclencher la mesure de distance
    capteur[ECHO]: pin pour lecture de l'echo

  Returns:
  --------
  float : distance en cm
  """
  # This function measures a distance
  GPIO.output(capteur[TRIG], True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(capteur[TRIG], False)
  start = time.time()
  
  while GPIO.input(capteur[ECHO])==0:
    start = time.time()

  while GPIO.input(capteur[ECHO])==1:
    stop = time.time()

  elapsed = stop - start
  distance = (elapsed * speedSound)/2

  return distance


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

  distance1=measure(capteur)
  time.sleep(0.1)
  distance2=measure(capteur)
  time.sleep(0.1)
  distance3=measure(capteur)
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

  # Pour calculer une racine carrée, utiliser sqrt(). Exemple: sqrt(2)
  
  return (p1, p2)


# -----------------------
# Main Script
# -----------------------

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Clefs pour définir les caractéristiques d'un capteur de distance
TRIG = "TRIG"   # Pin pour déclencher la mesure de distance
ECHO = "ECHO"   # Pin pour lecture de l'echo
X = "X"         # Coordonnée X du capteur (en cm)
Y = "Y"         # Coordonnée Y du capteur (en cm)

# Speed of sound in cm/s at temperature
temperature = 20
speedSound = 33100 + (0.6*temperature)

print("Ultrasonic Measurement")
print("Speed of sound is", speedSound/100, "m/s at ", temperature, "deg")

capteurs = [ {TRIG: 23, ECHO: 24}, {TRIG: 5, ECHO: 6} ]

# Configure les pins: TRIG -> output, ECHO -> input
for capteur in capteurs:
  GPIO.setup(capteur[TRIG], GPIO.OUT)
  GPIO.setup(capteur[ECHO], GPIO.IN)

# Set trigger to False (Low)
for capteur in capteurs:
  GPIO.output(capteur[TRIG], False)

# Allow module to settle
time.sleep(0.5)


# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.
try:
  while True:
    for i in range(len(capteurs)):
      distance = measure_average(capteurs[i])
      print("Distance {0:1d}: {1:5.1f}".format(i, distance))
      time.sleep(1)
    print("")

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()
