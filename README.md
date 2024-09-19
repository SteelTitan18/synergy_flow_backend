# SynergyFlow

## Description

Baskend d'une Mini plateforme de gestion de projets collaborations

## Prérequis

- python 3.9

## Installation

- Cloner le projet
  `git clone https://github.com/SteelTitan18/synergy_flow_backend.git`

- Créer un environnement virtuel avec python
  `python3 -m venv .venv`

- Actuver l'environnement
  `source .venv/bin/activate`

- Accéder au dossier /synergy_flow et installer les dépendances
  `cd synergy_flow`
  `pip install -r requirements.txt`

- Installer postgresql ni ce n'est pas encore fait et créer la base de données 'synergy_flow'

- Migrer les changements dans la base de données
  `python manage.py makemigratons`
  `python manage.py migrate`

- Créez un fichier .env qui ne sera pas ajouté au git. À l'intérieur, définissez les variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`,
  `DB_HOST` et `DB_PORT` en fonction de vos configurations postgresql

  ## Exécution

- Création d'un superutilisateur pour accéder à django-admin site `python manage.py createsuperuser`

- Création des autres utilisateurs sur django-admin site

- Installer Redis sur votre machine et lancer le serveur Redis (`sudo systemctl start redis` sur Linux)

- Lancer le serveur `python manage.py runserver`
