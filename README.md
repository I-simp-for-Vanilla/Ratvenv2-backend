# Backend Projet Ratven SQL

## Lancement du projet :

```bash
source .venv/bin/activate
```

```bash
uvicorn main:app --reload
```

## APIS

### LLM

### SQL

Databases > Schema > Table or View

Gestion des comptes

Get All Databases, Tables

Gestion des .MD > système de documentation (permet de stocker ses cheatsheets des commandes sql)

Endpoints à développer :

* create Database

* create Schema

* create Table

* create View

* create User

* Get all Databases

* Get all Schemas for a Database

* Get all Tables for a Schema

* Execute a sql query (get, update, create, delete)

## Connexion à la base de données

Dans un premier temps, possibilité uniquement de se connecter à une base locale (localhost avec lancement en local)

- un simple dotenv avec les host locaux, pas besoin d'authentification, afin de juste faire fonctionner localement. Scale up à faire plus tard

Dans un second temps, pousse sur le serveur distant et possibilité d'executer des requêtes sur un serveur local

Dans un troisième temps, si nécessaire, possibilité de connecter une base de données distante (cloud)

- Une superBase de données avec les `profils utilisateurs`, `scripts sql`, `discussions avec le chatbot`, etc...

- Les profils utilisateurs détiennent les informations de connexion de la bdd

## Structure du projet :

### Main

L'assemblage des différents routers

### database

L'endroit où le pool de connections est créé

### security

Fait les différents checks de sécurité. Les checks sont appelés au niveau des services

### services/

Les différentes fonctions qui communiquent à la base de données. Possibilité de les tester sans passer par API

### routers/

Les différentes routes de mon api

## ---------- Fonctionnalitées ---------- :

## Créer et gérer des bases de données :

### create database : permet de créer une base de données

`Paramètres` : Nom de la base de données

`Fonctionnement` : 

```SQL
CREATE DATABASE Ratven;
```

### get databases : récupérer toutes les bases de données

`Paramètres` : aucun

`Fonctionnement` : 

```SQL
SHOW DATABASES ;
```

### delete database : supprime une base de données

`Paramètres` : nom de la base de données

`Fonctionnement` : 

```SQL
DROP DATABASE Ratven ;
```

### create table : créé une table

`méthode` : POST

`Paramètres` : nom de la base de données

`Body` : 

```json
{
    "name": "user",
    "columns": [
        {
            "name": "id",
            "type": "int",
            "primary_key": true,
            "auto_increment": true,
            "nullable": false,
            "unique": true
        },
        {
            "name": "username",
            "type": "varchar(40)",
            "nullable": false,
            "unique": true
        },
        {
            "name": "password",
            "type": "varchar(200)",
            "nullable": false,
            "unique": false
        },
        {
            "name": "description",
            "type": "varchar(500)",
            "nullable": true,
            "unique": false,
            "default": ""
        }
    ]
}
```

`note` : possibilité d'ajouter des contraintes plus tards

`Fonctionnement` : 

```SQL
DROP DATABASE Ratven ;
```

### executer des scripts sql

### parler avec un chatbot qui a accès aux données des bases de données

### créer des skills

### importer des données via Excel, MySQL, Postgre, Snowflake (optionel parce que payant)

### paramétrer des ETLs (connexion + création de requêtes executées tous les jours)

### executer des commandes dans un terminal

connexion via websocket au backend qui execute des commandes terminal.

https://chat.mistral.ai/work/6ccb8cb1-f8d2-4635-9433-962cef25c8ba

