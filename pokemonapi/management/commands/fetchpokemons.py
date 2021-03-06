from django.core.management.base import BaseCommand
from pokemonapi.models import PokemonsData, PokemonsStats, PokemonsEvol
import json
import requests

class Command(BaseCommand):
    help = 'get and store data for pokemons'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **options):
        try:
            array_pokemon = []
            def find_all_evol(arg):
                global new_process, number_evolution
                new_process = arg['chain']['evolves_to']
                number_evolution = 2
                def find_evo(arg):
                    if len(arg) > 0:
                        for x in arg:
                            array_pokemon.append({
                                "name" : "{}".format(x['species']['name']),
                                "id" : number_evolution,
                                "evol_id": x['species']['url'].split("/")[6:7][0]
                            })
                            return (x['evolves_to'])
                while True:
                    evo_find = find_evo(new_process)
                    if len(evo_find) > 0:
                        number_evolution = number_evolution + 1
                        new_process = evo_find
                        pass
                    else:
                        break
            self.stdout.write(self.style.SUCCESS('get pokémon data from pokeapi.co id: {}'.format(options['id'])))
            response = requests.get('https://pokeapi.co/api/v2/evolution-chain/{}'.format(options['id']))
            response = json.loads(response.content)
            name = response['chain']['species']['name']
            array_pokemon.append({
                "name": "{}".format(name),
                "id": 1,
                "evol_id": response['chain']['species']['url'].split("/")[6:7][0]
            })
            find_all_evol(response)
            for d in array_pokemon:
                beging = PokemonMain()
                beging.parsing_data(d['name'], d['evol_id'], array_pokemon)
                beging.fetch_pokemons_data()
                beging.store_pokemon_data()

        except Exception as e:
            self.stdout.write(self.style.ERROR('except_handle: {}'.format(e)))


class PokemonMain(Command):
    """
    Process for fetch and store pokemon info
    with stats, id, evolutions
    """
    def parsing_data(self, name, id_of_pokemon,evolutions):
        self.name = name
        self.evolutions = evolutions
        self.id_of_pokemon = id_of_pokemon

    def process_stats(self, arg):
        stats = []
        for f in arg['stats']:
            json_stats = {
                "base_stat": f['base_stat'],
                "name": f['stat']['name']
            }
            stats.append(json_stats)
        return stats

    def fetch_pokemons_data(self):
        try:
            response = requests.get('https://pokeapi.co/api/v2/pokemon/{}'.format(self.name))
            response = json.loads(response.content)
            self.json_data_pokemon = {
                "pokemon_id": response['id'],
                "name": response['name'],
                "height": response['height'],
                "weight": response['weight'],
                "stats": self.process_stats(response),
                "evolutions": self.pre_or_next_evolutions()
            }
            # print(self.json_data_pokemon)
        except Exception as e:
            self.stdout.write(self.style.SUCCESS('error_in_fetch_pokemons_data: {}'.format(e)))

    def pre_or_next_evolutions(self):
        try:
            find_pokemon = [x for x in self.evolutions if x['name'] == self.name]
            id = find_pokemon[0]['id']
            data = []
            for g in self.evolutions:
                if g['id'] == id:
                    pass
                else:
                    if id < g['id']:
                        data.append({
                            "name": g['name'],
                            "position": g['id'],
                            "detail": "evolutions_to",
                            "evol_id": g['evol_id'],
                        })
                    else:
                        data.append({
                            "name": g['name'],
                            "position" : g['id'],
                            "detail": "pre_evolutions",
                            "evol_id": g['evol_id'],
                        })
            # print(data)
            return data
        except Exception as e:
            self.stdout.write(self.style.ERROR('pre_or_next_evolutions: {}'.format(e)))

    def store_pokemon_data(self):
        try:
            pokemon = PokemonsData.objects.filter(id_pokemon=self.json_data_pokemon['pokemon_id'])
            if not pokemon:
                pokemon = PokemonsData(
                    id_pokemon=self.json_data_pokemon['pokemon_id'],
                    name=self.json_data_pokemon['name'],
                    height=self.json_data_pokemon['height'],
                    weight=self.json_data_pokemon['weight']
                )
                pokemon.save()

                for stats in self.json_data_pokemon['stats']:
                    stats_pokemon = PokemonsStats(
                        pokemon=self.json_data_pokemon['pokemon_id'],
                        name=stats['name'],
                        base_stat=stats['base_stat']
                    )
                    stats_pokemon.save()

                for evol in self.json_data_pokemon['evolutions']:
                    evol_pokemon = PokemonsEvol(
                        id_evol = self.json_data_pokemon['pokemon_id'],
                        id_pokemon=evol['evol_id'],
                        name=evol['name'],
                        position=evol['position'],
                        detail = evol['detail'],
                        info= "http://127.0.0.1:8000/api/pokemon/{}".format(evol['name']),
                    )
                    evol_pokemon.save()
                self.stdout.write(self.style.SUCCESS('Registered Pokémon: {}'.format(self.name)))
            else:
                self.stdout.write(self.style.ERROR('The Pokemon is already registered'))

            return pokemon

        except Exception as e:
            self.stdout.write(self.style.ERROR("error_in_store_pokemon_data".format(e)))
