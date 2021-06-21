from django.db import models

# Create your models here.
class PokemonsData(models.Model):
    id_pokemon = models.IntegerField()
    name = models.CharField(max_length=15, unique=True)
    height = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return self.name

class PokemonsStats(models.Model):
    pokemon = models.IntegerField()
    name = models.CharField(max_length=15)
    base_stat = models.IntegerField()

    def __str__(self):
        return self.name


class PokemonsEvol(models.Model):
    id_evol = models.IntegerField()
    id_pokemon = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    min_lvl = models.CharField(max_length=15)
    detail = models.CharField(max_length=15)
    evolution_chain = models.IntegerField()

    def __str__(self):
        return self.name
