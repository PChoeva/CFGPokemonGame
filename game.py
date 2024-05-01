import random
import requests
from pprint import pprint

pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}/'
stats = ["name", "id", "height", "weight", "num_moves"]

def getRandomNumber():
    return random.randint(1,150)

def getPokemon(pokemon_id):
    request = pokemon_url.format(pokemon_id)
    response = requests.get(request)
    json = response.json()

    # how to get a pokemon photo
    # print(json["sprites"])
    num_moves = len(json['moves'])
    print(num_moves)

    pokemon = {"id": json["id"], "height": json["height"], "weight": json["weight"], "name": json["name"], "num_moves": num_moves}
    print(pokemon)
    return pokemon

def game():

    while True:
        selectStat = input("\nLet's play!\nPlease select which stat you would like to fight with (id/height/weight/number of moves (num_moves)/q -> quit):")


        if selectStat == "q":
            print("Thank you for playing. See you next time!")
            break
        if selectStat not in stats:
            print("Please select a stat from the provided list: id/weight/height/number of moves(num_moves).")
            continue

        player1Pokemon = getPokemon(getRandomNumber())
        player2Pokemon = getPokemon(getRandomNumber())

        if player1Pokemon[selectStat] > player2Pokemon[selectStat]:
            print(f"Player 1's {player1Pokemon["name"]} won over Player 2's {player2Pokemon["name"]} - category: {selectStat}")
        elif player1Pokemon[selectStat] < player2Pokemon[selectStat]:
            print(f"Player 2's {player2Pokemon["name"]} won over Player 1's {player1Pokemon["name"]} - category: {selectStat}")
        else:
            print(f"It's a Draw! Player 1's {player1Pokemon["name"]} and Player 2's {player2Pokemon["name"]} have the same {selectStat}")

game()