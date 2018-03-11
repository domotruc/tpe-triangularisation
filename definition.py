#!/usr/bin/python
# coding: utf-8

# Clefs pour définir les caractéristiques d'un capteur de distance
NAME = "NAME"   # Nom du capteur
TRIG = "TRIG"   # Pin pour déclencher la mesure de distance
ECHO = "ECHO"   # Pin pour lecture de l'echo
X = "X"         # Coordonnée X du capteur (en cm)
Y = "Y"         # Coordonnée Y du capteur (en cm)

# Speed of sound in cm/s at temperature
temperature = 20
speedSound = 33100 + (0.6*temperature)

# Dimension caractéristique de l'objet (en cm)
dimCaracteristique = 5

# Dimension max mesurable par un capteur (en cm)
# sqrt(2m) pour un carré de 1m de côté
maxDistance = 150
