# Projet IA Harmonie

![Version Python](https://img.shields.io/badge/python-3.5-blue.svg)


## Groupe

* ANDO Antoine
* PARE Raphaël
* CREACH Matthias

## Dependences

```
mido
midiutil
pygame
music21
```

## Utilisation

Placer les fichiers midi d'apprentissage dans le dossier ```music``` puis lancer la commande

```
python read.py [preset]
```

[presets]
* metalProg
* metal
* slayer
* megalovania
* mozart
* bach
* all


## Consignes

### 2. Des algorithmes bien artistiques

La musique est régie par des règles d’harmonie. La génération d’un morceau par l’ordinateur en utilisant ces règles d’harmonie est donc possible. 

Pour apprendre les règles, vous pouvez vous baser sur le site suivant par exemple. http://michelbaron.phpnet.us/harmonie.htm  
Vous pourrez vous contenter des règles de quinte dans un premier temps puis augmenter le nombre de règles.  

Pour jouer la musique, le lien https://wiki.python.org/moin/PythonInMusic peut être utile.

Une construction en temps réel est attendue. Pensée par bloc de notes ou note à note, selon la méthode choisie, le résultat devra sera enregistrable si possible et écoutable en direct à minima.