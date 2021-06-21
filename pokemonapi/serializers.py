from rest_framework import serializers
from .models import PokemonsEvol, PokemonsStats, PokemonsData

class PokemonsStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonsStats
        fields = ('name', 'base_stat')


class PokemonsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonsData
        fields = ('id_pokemon',
                  'name',
                  'height',
                  'weight',)

class PokemonsEvolSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonsEvol
        fields = ('id_pokemon', 'name', 'detail', 'info')
