#!/usr/bin/python
# coding: utf-8
#
# Librairie d'interface avec capteur ultrason HC-SR04

import RPi.GPIO as GPIO
from definition import *

def init_capteurs(capteurs):
  """
  Initialise les capteurs

  Parameters:
  -----------
  capteurs : tableau des capteurs
    capteur[TRIG]: pin pour déclencher la mesure de distance
    capteur[ECHO]: pin pour lecture de l'echo

  Returns:
  -------
  rien
  """
  # Use BCM GPIO references instead of physical pin numbers
  GPIO.setmode(GPIO.BCM)

  # Configure les pins: TRIG -> output, ECHO -> input
  for capteur in capteurs:
    GPIO.setup(capteur[TRIG], GPIO.OUT)
    GPIO.setup(capteur[ECHO], GPIO.IN)

  # Initialise pin trigger to False (Low - bas)
  for capteur in capteurs:
    GPIO.output(capteur[TRIG], False)

  # Temporisation pour laisser les capteur s'initialise
  time.sleep(0.5)


def mesure(capteur):
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
