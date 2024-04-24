import random
import requests
from pprint import pprint

pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}/'

def getRandomNumber():
    return random.randint(1,150)

def getPokemon(pokemon_id):
    request = pokemon_url.format(pokemon_id)
    response = requests.get(request)
    print(response.json())

def game():
    getPokemon(getRandomNumber())

game()