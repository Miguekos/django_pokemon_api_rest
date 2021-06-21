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
            self.stdout.write(self.style.SUCCESS('get pokémon data from pokeapi.co id: {}'.format(options['id'])))
            response = requests.get('https://pokeapi.co/api/v2/evolution-chain/{}'.format(options['id']))
            response = json.loads(response.content)
            beging = PokemonMain()
            beging.parsing_data(response)
            beging.fetch_pokemons_data()
            beging.store_pokemon_data()

        except Exception as e:
            self.stdout.write(self.style.ERROR('except_handle: {}'.format(e)))


class PokemonMain(Command):
    """
    Process for fetch and store pokemon info
    with stats, id, evolutions
    """
    def parsing_data(self, objects):
        self.name = objects['chain']['species']['name']
        self.evolutions = objects
        self.id_pokemon = objects['id']

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
        except Exception as e:
            self.stdout.write(self.style.SUCCESS('error_in_fetch_pokemons_data: {}'.format(e)))

    def pre_or_next_evolutions(self):
        try:
            global new_process, number_evolution, name_pokemon_fetch
            new_process = self.evolutions['chain']['evolves_to']
            number_evolution = 1
            data_evo = []

            def find_evo(arg):
                if len(arg) > 0:
                    for x in arg:
                        data_evo.append({
                            "name": "{}".format(x['species']['name']),
                            "min_lvl": "{}".format(x['evolution_details'][0]['min_level']),
                            "id": number_evolution,
                            "evol_id" : x['species']['url'].split("/")[6:7][0]
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
            return data_evo
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
                        min_lvl=evol['min_lvl'],
                        detail= "https://pokeapi.co/api/v2/pokemon/{}".format(evol['evol_id']),
                        evolution_chain=self.id_pokemon
                    )
                    evol_pokemon.save()
                self.stdout.write(self.style.SUCCESS('Registered Pokémon'))
            else:
                self.stdout.write(self.style.ERROR('The Pokemon is already registered'))

            return pokemon

        except Exception as e:
            self.stdout.write(self.style.ERROR("error_in_store_pokemon_data".format(e)))
