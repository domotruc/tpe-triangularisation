#!/usr/bin/python
# coding: utf-8
#
# Librairie d'interface avec capteur ultrason HC-SR04

import RPi.GPIO as GPIO

def measure(capteur):
  """
  Réalise la mesure du capteur passé en argument et renvoie la distance (en cm)

  Parameters:
  -----------
  capteur : définit les pins du capteur
    capteur[TRIG]: pin pour déclencher la mesure de distance
    capteur[ECHO]: pin pour lecture de l'echo
A
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

