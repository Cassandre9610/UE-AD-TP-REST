# UE-AD-A1-REST

Lien de l'exercice : https://helene-coullon.fr/pages/ue-ad-fil-25-26/tp-rest/

# Description

Ce projet est une petite application permettant de gérer une salle de cinéma, et les réservations des utilisateurs. Il s’agit d’une application jouet et peu réaliste.

Cette application est composée de 4 micro-services :

**Movie** est le micro-service responsable de la gestion des films du cinéma. Il contient et gère une petite base de données json contenant la liste des films disponibles avec quelques informations sur les films.

**Schedule** est le micro-service responsable des jours de passage des films dans le cinéma. Il contient et gère une petite base de données json contenant la liste des dates avec l’ensemble des films disponibles à cette date.

**Booking** est le micro-service responsable de la réservation des films par les utilisateurs. Il contient et gère une petite base de données json contenant une entrée par utilisateur avec la liste des dates et films réservés. Booking fait appel à Schedule pour connaître et vérifier que les créneaux réservés existent bien puisqu’il ne connait pas lui-même les créneaux des films.

**User** est le micro-service est le micro-service qui servirait typiquement à authentifier les utilisateurs. Il contient et gère une petite base de données json avec la liste des utilisateurs.

# Appels API

Les services utilisent les ports suivants :

| Service  | URL locale              |
| -------- | ----------------------- |
| Movie    | `http://localhost:3200` |
| Booking  | `http://localhost:3201` |
| Schedule | `http://localhost:3202` |
| User     | `http://localhost:3203` |

Toutes les données sont échangées au format JSON, sauf la page d'accueil des services qui retourne du HTML.

## User — port 3203

| Méthode  | Route                            | Description                                 |
| -------- | -------------------------------- | ------------------------------------------- |
| `GET`    | `/json`                          | Retourne tous les utilisateurs              |
| `GET`    | `/user/{userid}`                 | Retourne un utilisateur par son identifiant |
| `GET`    | `/user/name/{username}`          | Retourne un utilisateur par son nom exact   |
| `PUT`    | `/user/{userid}/name/{new_name}` | Modifie le nom d'un utilisateur             |
| `POST`   | `/user/{userid}`                 | Crée un utilisateur                         |
| `DELETE` | `/user/{userid}`                 | Supprime un utilisateur                     |

Objet utilisateur :

```json
{
  "id": "chris_rivers",
  "name": "Chris Rivers",
  "last_active": 1360031010
}
```

Exemples :

```bash
curl http://localhost:3203/json
curl http://localhost:3203/user/chris_rivers
curl -X DELETE http://localhost:3203/user/chris_rivers
```

## Movie — port 3200

| Méthode  | Route                                     | Description                          |
| -------- | ----------------------------------------- | ------------------------------------ |
| `GET`    | `/json`                                   | Retourne tous les films              |
| `GET`    | `/movies/movie/{movieid}`                 | Retourne un film par son identifiant |
| `GET`    | `/movies/title?title={title}`             | Retourne un film par son titre exact |
| `POST`   | `/movies/movie/{movieid}`                 | Crée un film                         |
| `PUT`    | `/movies/movie/{movieid}/rating/{rating}` | Modifie la notation d'un film        |
| `DELETE` | `/movies/movie/{movieid}`                 | Supprime un film                     |

Objet film :

```json
{
  "title": "The Good Dinosaur",
  "rating": 7.4,
  "director": "Peter Sohn",
  "id": "720d006c-3a57-4b6a-b18f-9b713b073f3c"
}
```

Exemples :

```bash
GET http://localhost:3200/json
GET http://localhost:3200/movies/title?title=The%20Martian

POST http://localhost:3200/movies/movie/0c54da52-37b8-4f7a-9b02-0d9054f40d49
{
    "title":"Test",
    "rating":1.2,
    "director":"Someone",
    "id":"0c54da52-37b8-4f7a-9b02-0d9054f40d49"
}
```

## Schedule — port 3202

| Méthode  | Route                                    | Description                                   |
| -------- | ---------------------------------------- | --------------------------------------------- |
| `GET`    | `/json`                                  | Retourne tous les emplois du temps            |
| `GET`    | `/schedule/date/{date}`                  | Retourne les films programmés à une date      |
| `GET`    | `/schedule/movie/{movie_id}`             | Retourne les dates où un film est programmé   |
| `POST`   | `/schedule/date/{date}/movie/{movie_id}` | Ajoute un film à une date                     |
| `DELETE` | `/schedule/date/{date}`                  | Supprime tous les films programmés à une date |
| `DELETE` | `/schedule/date/{date}/movie/{movie_id}` | Supprime un film d'une date                   |

Objet emploi du temps :

```json
{
  "date": "20151201",
  "movies": [
    "267eedb8-0f5d-42d5-8f43-72426b9fb3e6",
    "7daf7208-be4d-4944-a3ae-c1c2f516f3e6"
  ]
}
```

Exemples :

```bash
GET http://localhost:3202/schedule/date/20151201
GET http://localhost:3202/schedule/movie/39ab85e5-5e8e-4dc5-afea-65dc368bd7ab

POST http://localhost:3202/schedule/date/20151201/movie/267eedb8-0f5d-42d5-8f43-72426b9fb3e6
```

Lors de la création d'un emploi du temps, Schedule vérifie auprès du service Movie que l'identifiant du film existe.

## Booking — port 3201

| Méthode  | Route                                                 | Description                                               |
| -------- | ----------------------------------------------------- | --------------------------------------------------------- |
| `GET`    | `/json`                                               | Retourne toutes les réservations                          |
| `GET`    | `/bookings/user/{userid}`                             | Retourne les réservations d'un utilisateur                |
| `GET`    | `/bookings/date/{date}`                               | Retourne les réservations enregistrées à une date         |
| `GET`    | `/bookings/movie/{movieid}`                           | Retourne les utilisateurs ayant réservé un film           |
| `GET`    | `/bookings/user/{userid}/date/{date}`                 | Retourne les films réservés par un utilisateur à une date |
| `POST`   | `/bookings`                                           | Crée une réservation                                      |
| `DELETE` | `/bookings/user/{userid}`                             | Supprime toutes les réservations d'un utilisateur         |
| `DELETE` | `/bookings/user/{userid}/date/{date}/movie/{movieid}` | Supprime un film d'une réservation                        |

Objet réservation :

```json
{
  "userid": "chris_rivers",
  "dates": [
    {
      "date": "20151201",
      "movies": ["267eedb8-0f5d-42d5-8f43-72426b9fb3e6"]
    }
  ]
}
```

Création d'une réservation :

```bash
POST http://localhost:3201/bookings
{
    "userid": "chris_rivers",
    "date": "20151201",
    "movieid": "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
}
```

Booking vérifie auprès de Schedule que le film est bien prévu à la date demandée avant d'enregistrer la réservation.

## Formats et erreurs

Les erreurs sont retournées sous cette forme :

```json
{
  "error": "User ID not found"
}
```

# Aide

## Windows

```bash
python3 -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
cd .\movie\
pymon movie.py
```

## Linux

```cmd
python3 -m venv venv
source venv/Scripts/activate (ou source venv/bin/activate)
pip install -r requirements.txt
cd .\movie\
pymon movie.py
```
