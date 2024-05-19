import random
import requests
from pathlib import Path

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
    num_moves = len(json['moves']) # [{}, {}, {}] --> 3
    print(num_moves)

    pokemon = {"id": json["id"], "height": json["height"], "weight": json["weight"], "name": json["name"], "num_moves": num_moves}
    print(pokemon) # TODO remove
    return pokemon

wins = {
    "player1": 0,
    "player2": 0
}


def updateScoresheet():
    # with open("scoresheet.txt", "r+") as scoresheet:
    #     curr_score = scoresheet.read()
    #     print(f"Recorded high score - player 1: {curr_score["player1"]}")
    #     print(f"Recorded high score - player 2: {curr_score["player2"]}")

    print("Current score:")
    print(f"PLayer 1 -> {wins["player1"]}\nPlayer 2 -> {wins["player2"]}")

    player1_curr_high_score = wins["player1"]
    player2_curr_high_score = wins["player2"]

    if Path("./scoresheet.txt").exists():

        with open("./scoresheet.txt", "r") as scoresheet:
            high_score_player1 = int(scoresheet.readline().split(":")[1]) ["player", "2"]
            high_score_player2 = int(scoresheet.readline().split(":")[1])
            print(f"high score1: {high_score_player1}")
            print(f"high score2: {high_score_player2}")

            # compare recorded high score with curr score
            if player1_curr_high_score < high_score_player1:
                player1_curr_high_score = high_score_player1
            if player2_curr_high_score < high_score_player2:
                player2_curr_high_score = high_score_player2


    with open("./scoresheet.txt", "w") as scoresheet:
        scoresheet.write("player1:"+str(player1_curr_high_score))
        scoresheet.write("\nplayer2:"+str(player2_curr_high_score))


# Record high scores for players and store them in a file


def game():

    while True:
        selectStat = input("\nLet's play!\nPlease select which stat you would like to fight with (id/height/weight/number of moves (num_moves)/q -> quit):")


        if selectStat == "q":
            print("Thank you for playing. See you next time!")
            print(wins)
            updateScoresheet()
            break
        if selectStat not in stats:
            print("Please select a stat from the provided list: id/weight/height/number of moves(num_moves).")
            continue

        player1Pokemon = getPokemon(getRandomNumber())
        player2Pokemon = getPokemon(getRandomNumber())

        if player1Pokemon[selectStat] > player2Pokemon[selectStat]:
            print(f"Player 1's {player1Pokemon["name"]} won over Player 2's {player2Pokemon["name"]} - category: {selectStat}")
            wins["player1"] += 1
        elif player1Pokemon[selectStat] < player2Pokemon[selectStat]:
            print(f"Player 2's {player2Pokemon["name"]} won over Player 1's {player1Pokemon["name"]} - category: {selectStat}")
            wins["player2"] += 1
        else:
            print(f"It's a Draw! Player 1's {player1Pokemon["name"]} and Player 2's {player2Pokemon["name"]} have the same {selectStat}")

game()
