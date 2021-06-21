# Pokemon API

This is a Django App that fetches pokemons evolution chains from the [PokeApi](https://pokeapi.co/) and stores the collected data in a local database to then use it to expose an api to fetch that pokemons data collected.

### Dependencies
- Django==3.2.4
- djangorestframework==3.12.4
- Markdown==3.3.4
- django-filter==2.4.0
- requests==2.25.1

### Installation

Install the dependencies and start the server.

```sh
$ mkdir pokemon_apí
$ cd pokemon_apí
$ python -m venv env
$ source env/bin/activate  # On Windows use `env\Scripts\activate`
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

### Fetching and Storing Pokemon Chains Data
To fetch and store the pokemons data you can use the `fetchpokemons` custom django-admin commands

```sh
$ python manage.py fetchpokemons <EVOLUTION_POKEMON_ID>
```

### How it works
his endpoint only needs the "name" parameter to get the pokemon information
```sh
http://localhost:8000/api/pokemon/<POKEMON_NAME>
http://localhost:8000/api/pokemon/2
```

### Demo
```sh
$ python manage.py fetchpokemons 2
$ http://localhost:8000/api/pokemon/charmeleon
```
### Response
The pokemons data is returned is:
````
{
  "id_pokemon": 5,
  "name": "charmeleon",
  "height": 11,
  "weight": 190,
  "stats": [
    {
      "name": "hp",
      "base_stat": 58
    },
    {
      "name": "attack",
      "base_stat": 64
    },
    {
      "name": "defense",
      "base_stat": 58
    },
    {
      "name": "special-attack",
      "base_stat": 80
    },
    {
      "name": "special-defense",
      "base_stat": 65
    },
    {
      "name": "speed",
      "base_stat": 80
    }
  ],
  "evolutions": [
    {
      "id_pokemon": "4",
      "name": "charmander",
      "detail": "pre_evolutions",
      "info": "https://pokeapi.co/api/v2/pokemon/4"
    },
    {
      "id_pokemon": "6",
      "name": "charizard",
      "detail": "evolutions_to",
      "info": "https://pokeapi.co/api/v2/pokemon/6"
    }
  ]
}
````