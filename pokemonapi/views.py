from django.http.response import JsonResponse

from .models import PokemonsData, PokemonsEvol, PokemonsStats
from .serializers import PokemonsDataSerializer, PokemonsEvolSerializer, PokemonsStatsSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
def pokemon_find(request, name):
    if request.method == 'GET':
        try:
            pokemon = PokemonsData.objects.filter(name=name)
            if pokemon:
                pokemon_serializer = PokemonsDataSerializer(pokemon, many=True)
                response = pokemon_serializer.data
                idpk = response[0]['id_pokemon']
                print("idpk", idpk)

                species = PokemonsEvol.objects.filter(id_evol=idpk)
                species_serializer = PokemonsEvolSerializer(species, many=True)
                parse_species = species_serializer.data
                # print("parse_species",parse_species)

                stats = PokemonsStats.objects.filter(pokemon=idpk)
                stats_serializer = PokemonsStatsSerializer(stats, many=True)
                stats_serializer = stats_serializer.data
                print("stats_serializer", stats_serializer)

                json_response ={
                    **response[0],
                    "stats": stats_serializer,
                    "evolutions" : parse_species
                }

                return JsonResponse(json_response, safe=False)
            else:
                json_response = {
                    "detail": "Pokemon not found"
                }
                return JsonResponse(json_response, safe=False)
        except:
            json_response = {
                "error": "handled error"
            }
            return JsonResponse(json_response, safe=False)